import functools as ft
import operator as op

class Number:
    def __init__(self, value: float) -> None:
        self._value = value

    def __add__(self, other: object):
        return (
            Number(self._value + other._value)
            if isinstance(other, Number)
            else NotImplemented
        )

numbers = [Number(number) for number in range(1, 101)]
result: Number = ft.reduce(op.add, numbers, Number(0))
print(result._value)
print(sum(numbers, Number(0))._value)
