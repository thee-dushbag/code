import typing as ty, time as _time
from collections import deque

_T = ty.TypeVar("_T")
_P = ty.ParamSpec("_P")

Coroutine = ty.Generator[ty.Any, ty.Any, _T]
Awaitable = ty.Union["Future", "Task"]
Async = ty.Callable[_P, Coroutine[_T]]


class Error(Exception):
    ...


class CancelledError(Error):
    ...


class Future(ty.Generic[_T]):
    def __init__(self) -> None:
        self._result: _T = ty.cast(_T, None)
        self._exception: Exception | None = None
        self._done: bool = False

    def _set_done(self):
        self._done = True

    def set_result(self, result: _T, /):
        self._result = result
        self._set_done()

    def set_exception(self, exception: Exception, /):
        self._exception = exception
        self._set_done()

    def cancel(self):
        self.set_exception(CancelledError())

    @property
    def done(self) -> bool:
        return self._done

    @property
    def result(self) -> _T:
        if not self._done:
            raise Error
        if self._exception is not None:
            raise self._exception
        return self._result

    def __iter__(self):
        return self

    def __next__(self):
        if self._done:
            if self._exception is not None:
                raise self._exception
            raise StopIteration(self._result)


class Task(Future[_T]):
    def __init__(self, coro: ty.Generator) -> None:
        super().__init__()
        self._coro = coro

    def set_result(self, result: _T):
        raise NotImplementedError("Cannot set result of a Task.")

    def __next__(self):
        try:
            if self._done:
                raise StopIteration(self.result)
            return next(self._coro)
        except StopIteration as e:
            Future.set_result(self, e.value)
            raise e
        except Exception as e:
            self.set_exception(e)
            raise e


class EventLoop:
    def __init__(self) -> None:
        self._tasks = deque()
        self._running = False

    def time(self):
        return _time.time()

    def run(self, main):
        self._tasks.append(main)
        self.run_until_complete()

    def run_until_complete(self):
        while self._tasks:
            self.step()

    def step(self):
        task = self._tasks.popleft()
        try:
            next(task)
            self._tasks.append(task)
        except Exception:
            ...


loop: EventLoop | None = None


def create_task(task):
    if loop is None:
        raise Error("No Event loop Running")
    loop._tasks.append(task)
    return task


def coroutine(generator: Async[_P, _T]):
    def getargs(*args: _P.args, **kwargs: _P.kwargs) -> Task[_T]:
        return Task(generator(*args, **kwargs))

    return getargs


def set_event_loop(new_loop: EventLoop):
    global loop
    loop = new_loop


def get_event_loop() -> EventLoop:
    global loop
    if loop is None:
        loop = EventLoop()
    return loop


@coroutine
def sleep(delay: float, result=None):
    if delay <= 0:
        yield
    else:
        loop = get_event_loop()
        stop = loop.time() + delay
        while loop.time() <= stop:
            yield
    return result


@coroutine
def gather(*tasks):
    results = {}
    count, stopat = 0, len(tasks)

    @coroutine
    def callback(task):
        try:
            result = yield from task
            results[id(task)] = result
        finally:
            nonlocal count
            count += 1

    for task in tasks:
        create_task(callback(task))

    while count < stopat:
        yield

    return [results[id(task)] for task in tasks]


def as_completed(*tasks):
    que = Queue()

    @coroutine
    def callback(task):
        value = yield from task
        que.put(value)

    for task in tasks:
        create_task(callback(task))

    for _ in tasks:
        yield que.get()


@coroutine
def wait(task, delay: float):
    @coroutine
    def _waiter(timer):
        result = yield from task
        timer.cancel()
        return result

    @coroutine
    def notify():
        yield from sleep(delay)
        raise TimeoutError

    timer = create_task(notify())
    waiter = create_task(_waiter(timer))
    yield from gather(timer, waiter)
    if timer._exception is not None:
        waiter.cancel()
    return waiter.result


class Queue:
    def __init__(self, size=None) -> None:
        self._maxlen = -1 if size is None or size <= 0 else size
        self._waiters = deque()
        self._pushers = deque()
        self._store = deque()
        self._pushable = True
        self._waitable = True

    def empty(self):
        return len(self._store) == 0

    def full(self):
        if self._maxlen <= 0:
            return False
        return len(self._store) >= self._maxlen

    def put(self, value):
        pusher = Future()
        if not self._pushable:
            pusher.set_exception(Error("Queue closed from pushing."))
        elif self._waiters:
            pusher.set_result(None)
            waiter = self._waiters.popleft()
            waiter.set_result(value)
        elif self.full():
            self._pushers.append((pusher, value))
        else:
            self._store.append(value)
            pusher.set_result(None)
        return pusher

    def get(self):
        waiter = Future()
        if not self._waitable:
            waiter.set_exception(Error("Queue closed from waiting."))
        elif self._pushers:
            pusher, value = self._pushers.popleft()
            waiter.set_result(value)
            pusher.set_result(None)
        elif self._store:
            value = self._store.popleft()
            waiter.set_result(value)
        else:
            self._waiters.append(waiter)
        return waiter

    def drain(self):
        self.drain_pushers()
        self.drain_waiters()

    def drain_pushers(self):
        self._pushable = False
        while self._pushers:
            pusher, _ = self._pushers.popleft()
            pusher.set_exception(Error("No value takers forever."))

    def drain_waiters(self):
        self._waitable = False
        while self._waiters:
            waiter = self._waiters.popleft()
            waiter.set_exception(Error("No value puters forever."))


class Semaphore:
    def __init__(self, count: int) -> None:
        self._waiters = deque()
        self._count = count

    def __enter__(self):
        return self._gain()

    def __exit__(self, *_):
        self._release()

    def _gain(self):
        waiter = Future()
        if self._count > 0:
            self._count -= 1
            waiter.set_result(None)
        else:
            self._waiters.append(waiter)
        return waiter

    def _release(self):
        if self._waiters:
            waiter = self._waiters.popleft()
            waiter.set_result(None)
        else:
            self._count += 1


class Lock(Semaphore):
    def __init__(self) -> None:
        super().__init__(1)

    @property
    def locked(self):
        return self._count == 0


class Event:
    def __init__(self) -> None:
        self._waiter = Future()

    @coroutine
    def wait(self):
        yield from self._waiter

    def set(self):
        self._waiter.set_result(None)

    reset = __init__

from random import random


@coroutine
def setname(fut: Future):
    yield from sleep(random())
    fut.set_result("Simon Nganga")


@coroutine
def getnamei(iid: int):
    future = Future()
    create_task(setname(future))
    name = yield from future
    print(f"Hello {name}?")
    return iid


@coroutine
def runme(task):
    name = yield from task
    print(name, task.result)


def main():
    tasks = [
        create_task(sleep(i, n))
        for i, n in (
            (0.5, "Simon"),
            (1, "Nganga"),
            (0.7, "Faith"),
            (2, "Lydia"),
            (0, "Njeri"),
            (0.2, "Wanjiru"),
        )
    ]

    que = Queue()
    others = [feed(que), eat(que), *[getnamei(i) for i in range(1, 6)]]
    task = create_task(gather(*others))
    for future in as_completed(*tasks):
        value = yield from future
        print(f"Value: {value}")
    results = yield from task
    print(results)


@coroutine
def feed(que: Queue):
    for i in range(100, 110):
        yield from sleep(random())
        que.put(i)


@coroutine
def eat(que: Queue):
    for _ in range(10):
        value = yield from que.get()
        print(f"Found: {value}")


@coroutine
def worker(wid, que: Queue, lock: Lock):
    while True:
        with lock as waiter:
            yield from waiter
            value = yield from que.get()
            if value is None:
                create_task(que.put(value))
                break
            print(f"[{wid}]: Processing: {value}")
            yield from sleep(0.5)
            print(f"[{wid}]: Finished: {value}")


@coroutine
def manager(que: Queue, start, stop):
    for current in range(start, stop):
        yield from que.put(current)
    yield from que.put(None)


@coroutine
def work():
    que, lock = Queue(), Lock()
    tasks = [worker(wid, que, lock) for wid in range(1, 4)]
    pub = create_task(manager(que, 1, 21))
    yield from gather(*tasks, pub)


@coroutine
def anotherone():
    try:
        name = yield from wait(sleep(5, "Simon Nganga"), 3)
        print(name)
    except TimeoutError:
        print("Getting name took too long.")


loop = EventLoop()
loop.run(anotherone())
