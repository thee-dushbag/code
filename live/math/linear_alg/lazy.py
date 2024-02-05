import typing as ty
import math, functools as ft


class Expr(ty.Protocol):
    def __eval__(self) -> ty.Any:
        ...


def evaluate(expr: Expr | float):
    if isinstance(expr, (float, int)):
        return expr
    return expr.__eval__()


class Binary(Expr):
    lsymbol: str = ""
    rsymbol: str = ""
    symbol: str = "<NONE>"

    def __init__(self, left, right) -> None:
        self.right = right
        self.left = left

    def operate(self, left, right):
        raise NotImplementedError

    def __eval__(self):
        left = evaluate(self.left)
        right = evaluate(self.right)
        return self.operate(left, right)

    def __eq__(self, value: ty.Any) -> bool:
        if isinstance(value, Binary):
            left = self.left == value.left
            right = self.right == value.right
            return left and right
        return False

    def __str__(self) -> str:
        return f"{self.lsymbol}{self.left!s}{self.symbol}{self.right!s}{self.rsymbol}"

    __repr__ = __str__


class Unary(Expr):
    left: str = "<LEFT>"
    right: str = "<RIGHT>"

    def __init__(self, middle) -> None:
        self.middle = middle

    def operate(self, expr):
        raise NotImplementedError

    def __eval__(self):
        middle = evaluate(self.middle)
        return self.operate(middle)

    def __eq__(self, value: ty.Any) -> bool:
        if isinstance(value, Unary):
            return self.middle == value.middle
        return False

    def __str__(self) -> str:
        return f"{self.left}{self.middle!s}{self.right}"

    __repr__ = __str__


def binary(op_symbol: str, lsym: str | None = None, rsym: str | None = None, /):
    def capture(operator: ty.Callable[[ty.Any, ty.Any], ty.Any]):
        class _Binary(Binary):
            symbol = op_symbol
            lsymbol = lsym or ""
            rsymbor = rsym or ""

            def operate(self, left, right):
                return operator(left, right)

        return _Binary

    return capture


def unary(op_left: str, op_right: str | None = None, /):
    def capture(operator: ty.Callable[[ty.Any], ty.Any]):
        class _Unary(Unary):
            left = op_left
            right = op_left if op_right is None else op_right

            def operate(self, middle):
                return operator(middle)

        return _Unary

    return capture


@binary(" + ")
def add(left, right):
    return left + right


@binary(" * ")
def mul(left, right):
    return left * right


@binary(" - ")
def sub(left, right):
    return left - right


@binary(" / ")
def div(left, right):
    return left / right


@unary("-", "")
def inverse(value):
    return -value


@unary("")
def number(value):
    return value


@unary("|")
def absolute(value):
    return evaluate(abs(value))


def BFunction(function: ty.Callable[[ty.Any, ty.Any], ty.Any], /):
    name = function.__name__
    left, right = f"{name}(", ")"
    return binary(", ", left, right)(function)


def UFunction(function: ty.Callable[[ty.Any], ty.Any], /):
    name = function.__name__
    left, right = f"{name}(", ")"
    return unary(left, right)(function)


sin = UFunction(math.sin)
cos = UFunction(math.cos)
acos = UFunction(math.acos)
sqrt = UFunction(math.sqrt)


@UFunction
def sqr(value):
    return value * value


class Vector(list[Expr]):
    def dimension(self):
        return self.__len__()

    dim = dimension

    def _magnitude(self):
        return ft.reduce(add, map(sqr, self))  # type: ignore

    def magnitude(self):
        return sqrt(self._magnitude())

    def unit(self):
        mag = absolute(self)
        return Vector(map(lambda x: div(x, mag), self))

    def dot(self, other: "Vector"):
        assert self.dim() == other.dim()
        return ft.reduce(add, map(mul, self, other))

    def dot_geo(self, other: "Vector"):
        assert self.dim() == other.dim()
        mag_a = absolute(self)
        mag_b = absolute(self)
        return mul(mul(mag_a, mag_b), cos(self.angle(other)))

    def angle(self, other: "Vector"):
        assert self.dim() == other.dim()
        mag = mul(absolute(self), absolute(self))
        return acos(div(self.dot(other), mag))

    def cross(self, other: "Vector"):
        assert self.dim() == 3 and other.dim() == 3
        m, n, o = self
        x, y, z = other
        i = sub(mul(n, z), mul(o, y))
        j = sub(mul(o, x), mul(m, z))
        k = sub(mul(m, y), mul(n, x))
        return Vector([i, j, k])

 