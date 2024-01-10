import typing as ty
from collections import deque
from time import sleep

P = ty.ParamSpec("P")
T = ty.TypeVar("T")


class Task(ty.Generic[T]):
    def __init__(self, task: ty.Generator[ty.Any, ty.Any, T]) -> None:
        self._task = task
        self._done = False
        self._result: T = None  # type: ignore
        self._exc: BaseException | None = None

    @property
    def done(self) -> bool:
        return self._done

    @property
    def result(self) -> T:
        if self._exc is not None:
            raise self._exc
        return self._result

    def _step(self, thing=None):
        try:
            self._task.send(thing)
        except StopIteration as e:
            self._done = True
            self._result = e.value
        except Exception as e:
            self._exc = e


class GenLoop:
    def __init__(self) -> None:
        self.tasks: deque[Task] = deque()
        self.waiters: dict[Task, Task] = {}

    def run(self):
        while self.tasks:
            task = self.tasks.popleft()
            task._step()
            if not task.done:
                self.tasks.append(task)

    def coroutine(
        self, genfunc: ty.Callable[P, ty.Generator[ty.Any, ty.Any, T]]
    ) -> ty.Callable[P, Task[T]]:
        def getargs(*args: P.args, **kwargs: P.kwargs) -> Task[T]:
            task: Task[T] = Task(genfunc(*args, **kwargs))
            self.tasks.append(task)
            return task

        return getargs


loop = GenLoop()


@loop.coroutine
def progress(count: int, name: str, template: str):
    for current in range(1, count + 1):
        print(template % dict(current=current, name=name))
        yield sleep(0.3)
    raise Exception


@loop.coroutine
def add(x: float, y: float):
    yield sleep(0.5)
    yield sleep(0.5)
    yield sleep(0.5)
    return x + y


greeter = "[%(current)s]: Hello %(name)s, how was your day?"
countdown = "[%(current)s]: %(current)s seconds to %(name)s landing."

tasks = [
    # progress(10, "Boeing737", countdown),
    progress(6, "Simon Nganga", greeter),
    # progress(8, "Apollo2", countdown),
    progress(4, "Faith Njeri", greeter),
    # progress(6, "StarTrek", countdown),
    progress(2, "Lydia Wanjiru", greeter),
    # progress(4, "GoogleBard", countdown),
    add(7, 8),
]

loop.run()
