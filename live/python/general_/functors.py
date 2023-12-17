import threading as th
from typing_extensions import Any


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
        self.__lock: th.Lock = th.Lock()
        self.res: Any | None = res
        self.x = x
        self.y = y

    def set(self, x: Any, y: Any) -> None:
        with self.__lock:
            self.x = x
            self.y = y

    def __call__(self) -> Any:
        self.update()

    def update(self):
        res = my_sum(self.x, self.y)
        with self.__lock:
            self.res = res

    def __str__(self) -> str:
        return f"<SumFunctor({self.x}, {self.y}) -> {self.res}>"
