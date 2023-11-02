from itertools import zip_longest
from typing import Any, Iterable

from typing_extensions import Self


class groupinto:
    def __init__(self: Self, iterable: Iterable, size: int = 1) -> None:
        size = int(size)
        self.iobj = iter(iterable)
        self.size = size if size > 0 else 1

    def __iter__(self):
        return self

    def __next__(self):
        for group in zip_longest(*[self.iobj for _ in range(self.size)]):
            return group
        raise StopIteration


class NumberSpliter:
    def __init__(self: Self, grpcnt: int = 3, isep: str = "") -> None:
        self.isep = isep
        self.grpcnt = grpcnt

    def split(self, number: str | int) -> str:
        _var: Any = reversed(str(number))
        _var = list(
            reversed([list(reversed(var)) for var in groupinto(_var, self.grpcnt)])
        )
        _clean = lambda vals: ["0" if val == None else val for val in vals]
        _var = [self.isep.join(_clean(var)) for var in _var]
        return _var
