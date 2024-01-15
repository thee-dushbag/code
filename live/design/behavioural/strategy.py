import typing as ty

T = ty.TypeVar("T")

Operator = ty.Callable[[ty.Any, ty.Any], ty.Any]

add = lambda a, b: a + b
sub = lambda a, b: a - b
div = lambda a, b: a / b
mul = lambda a, b: a * b


class Binary:
    def __init__(self, first: T, second: T, /) -> None:
        self.first = first
        self.second = second
        self.computer: Operator = add

    def compute(self):
        return self.computer(self.first, self.second)


data = Binary(12, 4)
operators: list[Operator] = [add, mul, sub, div]

for operator in operators:
    data.computer = operator
    print(data.compute())
