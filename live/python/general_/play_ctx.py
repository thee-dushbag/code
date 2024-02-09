from typing import ParamSpec, Callable, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


class Context:
    def __init__(self, enter=None, exit=None) -> None:
        self._enter = enter or self._enter
        self._exit = exit or self._exit

    @staticmethod
    def _enter():
        raise NotImplementedError

    @staticmethod
    def _exit(type, value, traceback):
        raise NotImplementedError

    def __enter__(self):
        return self._enter()

    def __exit__(self, type, value, traceback):
        return self._exit(type, value, traceback)


class ContextDec(Context):
    def __call__(self, func: Callable[P, T]) -> Callable[P, T]:
        def _inner(*args: P.args, **kwargs: P.kwargs) -> T:
            with self:
                return func(*args, **kwargs)

        return _inner


def test_ctx():
    try:
        with Context(lambda: print("Hello"), lambda *_: not print("Python", _)):
            print("From")
            raise SystemError
    except SystemError:
        print("Exception was unhandled, ignoring it!")
    else:
        print("Exception handled successfully!")


@ContextDec(
    lambda: print("Hello", end=" "), lambda *_: not print(", how was your day?")
)
def say_hi_to(name: str):
    print(name, end="")


say_hi_to("Simon Nganga")
