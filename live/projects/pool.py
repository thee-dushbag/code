from threading import Thread, Lock
from collections import deque
import typing as ty, time


WorkType = ty.Callable[[], ty.Any | None]
WorkGen = ty.Callable[[], WorkType]
P = ty.ParamSpec("P")
T = ty.TypeVar("T")
CoroutineType = ty.Callable[P, T]
NOOP = lambda *_, **__: None


class Waiter(ty.Generic[T]):
    "A simple synchronization mechanism for the Thread EventPool."
    def __init__(self) -> None:
        self._data: T = ty.cast(T, None)
        self._flag = Lock()
        self._flag.acquire()
        self.notified = False

    def wait(self) -> T:
        with self._flag:
            return self._data

    def notify(self, task: T):
        self._flag.release()
        self._data = task
        self.notified = True

    def __del__(self):
        if self._flag.locked():
            raise RuntimeWarning("Waiter was never notified. %r" % self)


class Worker:
    def __init__(self, work_gen: WorkGen) -> None:
        self._get_work = work_gen
        self._runner: Thread = ty.cast(Thread, None)
        self._running: bool = False

    @property
    def alive(self) -> bool:
        return self._running

    def _start(self):
        if self._running:
            return
        self._running = True
        self._runner = Thread(target=self._work)
        self._runner.start()

    def _stop(self):
        "Does some pre stop operations then returns a wait stop callback."
        if not self._running:
            return NOOP
        self._running = False

        def wait():
            self._runner.join()
            self._runner = ty.cast(Thread, None)

        return wait

    def _work(self):
        while self._running:
            self._get_work()()


class Pool:
    def __init__(self, size: int = 3) -> None:
        self._workers: list[Worker] = [Worker(self._get) for _ in range(size)]
        self._waiters: deque[Waiter[WorkType]] = deque()
        self._tasks: deque[WorkType] = deque()

    def put(self, work: WorkType):
        if self._waiters:
            waiter = self._waiters.popleft()
            return waiter.notify(work)
        self._tasks.append(work)

    def _get(self) -> WorkType:
        if self._tasks:
            return self._tasks.popleft()
        waiter = Waiter()
        self._waiters.append(waiter)
        return waiter.wait()

    def _start(self):
        for worker in self._workers:
            worker._start()

    def _stop(self):
        waiters = [w._stop() for w in self._workers]
        while self._waiters:
            self.put(NOOP)
        for wait in waiters:
            wait()

    def breakpoint(self):
        waiter: Waiter[None] = Waiter()
        self.put(lambda: waiter.notify(None))
        waiter.wait()

    def clear(self):
        tasks = self._tasks
        self._tasks = deque()
        return tasks

    def __enter__(self):
        self._start()
        return self

    def __exit__(self, type, value, traceback):
        self.breakpoint()
        self._stop()


class Task(ty.Generic[T]):
    def __init__(
        self, coroutine: CoroutineType[P, T], *args: P.args, **kwargs: P.kwargs
    ) -> None:
        self._result: T = ty.cast(T, None)
        self._event: Waiter[None] = Waiter()
        self._function = coroutine
        self._callback = []
        self._kwargs = kwargs
        self._args = args

    def __call__(self):
        if self.complete:
            raise Exception("Task Already complete")
        self._result = self._function(*self._args, **self._kwargs)
        self._event.notify(None)
        for callback in self._callback:
            callback(self._result)

    def add_callback(self, callback: ty.Callable[[T], ty.Any]):
        if self.complete:
            callback(self._result)
        self._callback.append(callback)

    @property
    def complete(self) -> bool:
        return self._event.notified

    @property
    def result(self) -> T:
        if not self.complete:
            raise Exception("Task has not completed yet")
        return self._result

    def wait(self) -> T:
        self._event.wait()
        return self._result


class Queue(ty.Generic[T]):
    "Asynchronous Queue."

    def __init__(self) -> None:
        self._data: deque[T] = deque()
        self._waiters: deque[Waiter[T]] = deque()

    def put(self, data: T):
        if self._waiters:
            waiter = self._waiters.popleft()
            return waiter.notify(data)
        self._data.append(data)

    def get(self) -> T:
        if self._data:
            return self._data.popleft()
        waiter: Waiter[T] = Waiter()
        self._waiters.append(waiter)
        return waiter.wait()


def as_completed(*tasks: Task):
    queue = Queue()

    for task in tasks:
        task.add_callback(queue.put)

    for _ in tasks:
        yield queue.get()


def gather(*tasks: Task):
    return [task.wait() for task in tasks]


def sayhi(name: str, delay: float = 0.5):
    print(f"Hello {name}, how was your day?")
    time.sleep(delay)
    print(f"Goodbye {name}! Greeted you {delay} seconds ago.")
    return delay


def main():
    tasks: list[tuple[str, float]] = [
        ("Simon Nganga", 0.5),
        ("Faith Njeri", 0.4),
        ("Lydia Wanjiru", 1),
        ("Sophia Njeri", 2),
        ("Darius Kimani", 0.2),
        ("Harrison Kariuki", 1.5)
    ]

    print("START")
    with Pool(4) as pool:
        ntasks: list[Task[float]] = [Task(sayhi, name, delay) for name, delay in tasks]
        for task in ntasks: pool.put(task)
        for delay in as_completed(*ntasks): print(delay)
    print("DONE")


if __name__ == "__main__":
    main()
