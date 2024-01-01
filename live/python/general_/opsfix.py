# Represents no value
none = object()


class BiPartialOp:
    def __init__(self, func, one=None, two=None):
        self._one = none if one is None else one
        self._two = none if two is None else two
        self._value = none
        self._func = func

    @property
    def one(self):
        return self._one

    @property
    def two(self):
        return self._two

    def __ror__(self, value):
        if self._one is none:
            self._one = value
        else:
            raise ValueError("Already filled in first operand")
        if self._two is not none:
            return self._call()
        return self

    def __or__(self, value):
        if self._two is none:
            self._two = value
        else:
            raise ValueError("Already filled in second operand")
        if self._one is not none:
            return self._call()
        return self

    def _call(self):
        return self._func(self.one, self.two)

    def __str__(self):
        return (
            f"{self.__class__.__name__}(one={self._one is not none}"
            f", two={self._two is not none}, "
            f"value={self._value is not none})"
        )

    __repr__ = __str__


class UnPrefixOp(BiPartialOp):
    def __init__(self, func, one=None):
        super().__init__(func, one, none)
    
    def _call(self):
        if self._one is not none:
            return self._func(self._one)
        return none

    def __ror__(self, value):
        raise NotImplementedError

class UnPostfixOp(BiPartialOp):
    def __init__(self, func, two=None):
        super().__init__(func, none, two)
    
    def _call(self):
        if self._two is not none:
            return self._func(self._two)
        return none

    def __or__(self, value):
        raise NotImplementedError


class Operation:
    def __init__(self, operator) -> None:
        self.operator = operator

    def __ror__(self, other):
        return BiPartialOp(self.operator, one=other)

    def __or__(self, other):
        return BiPartialOp(self.operator, two=other)

    def __add__(self, other):
        return UnPrefixOp(self.operator, other)._call()

    def __radd__(self, other):
        return UnPostfixOp(self.operator, other)._call()

@Operation
def op(a, b):
    return a**2 + b


@Operation
def contains(a, b):
    return b in a

@Operation
def fact(a):
    f = 1
    for v in range(1, a + 1):
        f *= v
    return f

print("string" | contains | "i")
print(3 | op | 10)
print(fact + 4)


class Filter:
    def __init__(self, test):
        self.test = test

    def __ror__(self, other):
        for value in other:
            if self.test(value):
                yield value


class Transform:
    def __init__(self, func) -> None:
        self.transformer = func

    def __ror__(self, other):
        for value in other:
            yield self.transformer(value)


class Take:
    def __init__(self, size) -> None:
        self.size = size

    def __ror__(self, other):
        for index, value in enumerate(other):
            if index >= self.size:
                yield value


class ForEach:
    def __init__(self, func) -> None:
        self.func = func

    def __ror__(self, other):
        for value in other:
            self.func(value)


@Filter
def iseven(value):
    return not (value & 1)


@Transform
def plus3(value):
    return value + 3


values = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
# values | iseven | plus3 | ForEach(print)  # type: ignore
