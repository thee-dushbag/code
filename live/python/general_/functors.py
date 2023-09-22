import threading as th
from typing import Callable

from typing_extensions import Any, Self


def my_sum(x: Any, y: Any) -> Any:
    print(f"{x} + {y} = {x + y}")
    return x + y


def my_sub(x: Any, y: Any) -> Any:
    print(f"{x} - {y} = {x - y}")
    return x - y


def my_mul(x: Any, y: Any) -> Any:
    print(f"{x} * {y} = {x * y}")
    return x * y


def my_div(x: Any, y: Any) -> Any:
    print(f"{x} / {y} = {x / y}")
    return x / y


class SumFunctor:
    def __init__(self, x: Any = 0, y: Any = 0, res: Any | None = None) -> None:
        self.x = x
        self.y = y
        self.res: Any | None = res
        self.__lock: th.Lock = th.Lock()

    def set(self, x: Any, y: Any) -> None:
        self.__lock.acquire()
        self.x = x
        self.y = y
        self.__lock.release()

    def __call__(self) -> Any:
        res = my_sum(self.x, self.y)
        self.__lock.acquire()
        self.res = res
        self.__lock.release()

    def __str__(self) -> str:
        return f"<SumFunctor({self.x}, {self.y}) -> {self.res}>"
