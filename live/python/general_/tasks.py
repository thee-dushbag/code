import threading as th
import time
from typing import Any, Callable


class TaskState:
    Started: int = 0
    Done: int = 1
    Waiting: int = 2


class LaunchPolicy:
    ExecuteImmediately: int = 0
    PendForFire: int = 1


class Task:
    def __init__(self, hook, func, *args, **kwargs) -> None:
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.hook = hook
        self.hook.state = TaskState.Waiting
        self.worker = th.Thread(target=self._get)
        self._s = False
        if self.hook.exec_policy == LaunchPolicy.ExecuteImmediately:
            self.worker.start()
            self._s = True

    def get(self):
        print("Starting")
        if not self._s:
            self.worker.start()
            self._s = True
        if self.worker.is_alive():
            self.worker.join()

    def _get(self):
        self.hook.state = TaskState.Started
        self.hook.result = self.func(*self.args, **self.kwargs)
        self.hook.state = TaskState.Done


class PackagedTask:
    def __init__(self, pol: int, func: Callable, *args: Any, **kwargs: Any) -> None:
        self.result = None
        self._state = None
        self.exec_policy = pol
        self.task = Task(self, func, *args, **kwargs)
        self.callback = None

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, val):
        self._state = val
        if self.is_done() and self.callback:
            self.callback(self.result)

    def get(self) -> Any:
        self.task.get()
        return self.result

    def is_done(self):
        return self.state == TaskState.Done

    def then(self, callback):
        self.callback = callback
