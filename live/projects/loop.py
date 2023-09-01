from functools import wraps
from itertools import count
from time import time
from typing import Any, Callable

class CancelledError(Exception):
    ...

class Future:
    def __init__(self) -> None:
        self._done = False
        self._current_result = None
        self._running = False
        self._done_callback: Any = None
        self._exception = None
    
    def set_exception(self, exc):
        self._exception = exc
    
    def set_result(self, result):
        if not self._done:
            self._current_result = result
            self._done = True
    
    @property
    def done(self): return self._done
    
    def __await__(self):
        while not self._done: yield
        if self._exception: raise self._exception
        return self._current_result

    def _step(self): ...
    def _cancel(self): self.set_result(None)

def is_future(obj):
    return isinstance(obj, Future)

class Task(Future):
    def __init__(self, coro) -> None:
        super().__init__()
        self._coro = coro

    def _cancel(self):
        try:
            self._coro.throw(CancelledError)
        except CancelledError: ...
        super()._cancel()

    def _step(self):
        if self.done: return
        try:
            self._coro.send(None)
        except StopIteration as e:
            self.set_result(e.value)
        except Exception as e:
            self.set_exception(e)
        except BaseException as e:
            self.set_exception(e)
            raise

class _TaskWrapper:
    def __init__(self, loop, tid, task: Future) -> None:
        self._value = task._current_result
        self._task = task
        self._task._running = True
        self._alive = True
        self._tid = tid
        self._loop = loop
    
    def __hash__(self) -> int: return self._tid
    
    def _step(self):
        if not self._alive: return
        self._task._step()
        if self._task.done:
            self._alive = False
            self._value = self._task._current_result
            if self._task._done_callback:
                self._task._done_callback(self._value)
    
    def cancel(self):
        self._alive = False
        self._task._cancel()

class EventLoop:
    def __init__(self) -> None:
        self._tasks = []
        self._tid_keeper = count(1)
        self._time = time()
        self._running = False
        self._alive = 0
    
    @property
    def _tid(self): return next(self._tid_keeper)
    
    def create_task(self, coro) -> Task:
        task = coro if isinstance(coro, Task) else Task(coro)
        if task._running: return task
        taskwrapper = _TaskWrapper(self, self._tid, task)
        self._tasks.append(taskwrapper)
        return task
    
    def _step_all(self):
        for task in self._tasks:
            task._step()
    
    def _update_constants(self):
        self._time = time()
        self._alive = sum(t._alive for t in self._tasks)

    def run_until_complete(self):
        self._update_constants()
        while self._alive:
            self._update_constants()
            self._step_all()

    def run(self, coro):
        task = self.create_task(coro)
        self.run_until_complete()
        return task._current_result

    def run_forever(self):
        while self._running:
            self._update_constants()
            self._step_all()
    
    def shutdown(self):
        self._running = False

_loop: EventLoop = None # type:ignore

def get_event_loop() -> EventLoop:
    global _loop
    if _loop is None:
        _loop = EventLoop()
    return _loop

def run(coro):
    loop = get_event_loop()
    return loop.run(coro)

def coroutine(func) -> Callable[..., Task]:
    def _get_args(*args, **kwargs) -> Task:
        loop = get_event_loop()
        return loop.create_task(func(*args, **kwargs))
    return _get_args

def _sleep(delay, result):
    if delay <= 0: yield
    else:
        loop = get_event_loop()
        end_time = loop._time + delay
        while end_time > loop._time: yield
    return result

def _gather(loop, *coros):
    tasks = [loop.create_task(coro) for coro in coros]
    finished = 0
    total = len(coros)
    def _done_callback(value):
        nonlocal finished
        finished += 1
    for task in tasks: task._done_callback = _done_callback
    while finished < total: yield
    return [t._current_result for t in tasks]

def gather(*coros):
    loop = get_event_loop()
    return loop.create_task(_gather(loop, *coros))


def sleep(delay, result = None):
    loop = get_event_loop()
    return loop.create_task(_sleep(delay, result))