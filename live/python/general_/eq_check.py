log: bool = True
newline: bool = True
UnknownEqCheck = NotImplemented


class _M:
    eq: tuple[type["_M"], ...] | type["_M"]

    def __init__(self, v: object) -> None:
        self.v = v

    def __eq__(self, o: object):
        if log:
            print(f"{self}.__eq__({o})  | {self} is {o} = {self is o}")
        return isinstance(o, self.eq) and self.v == o.v or UnknownEqCheck

    def __str__(self) -> str:
        return "%s(%r)" % (self.__class__.__name__, self.v)


class A(_M):
    @property
    def eq(self):
        return A


class B(_M):
    @property
    def eq(self):
        return B


class C(_M):
    @property
    def eq(self):
        return C, B


class D(_M):
    @property
    def eq(self):
        return _M  # A, B, C, D


def cmp(a: object, b: object, new_line: bool | None = None) -> bool:
    r: bool = a == b
    new_line = newline if new_line is None else new_line
    end = "\n" if new_line else ""
    print(f"{a} == {b} = {r}{end}")
    return r


class Type1:
    def __init__(self, value) -> None:
        self.value = value

    def __add__(self, other: "Type1") -> "Type1":
        if isinstance(other, Type1):
            return Type1(self.value + other.value)
        return NotImplemented


class Type2:
    def __init__(self, value) -> None:
        self.value = value

    def __add__(self, other: "Type2") -> "Type2":
        if isinstance(other, Type2):
            return Type2(self.value + other.value)
        return NotImplemented


def main():
    global UnknownEqCheck, log, newline
    # UnknownEqCheck = False
    # newline = False
    # log = False
    a1, a2, a3 = map(A, [1, 2, 2])
    b1, b2, b3 = map(B, [1, 2, 2])
    c1, c2, c3 = map(C, [1, 2, 2])
    d1, d2, d3 = map(D, [1, 2, 2])
    cmp(a1, a1)
    cmp(a2, a3)
    cmp(a1, a2)
    cmp(a1, b1)
    cmp(b1, a1)
    cmp(a1, d1)
    cmp(d1, a1)
    cmp(b1, c1)
    cmp(c1, b1)
    cmp(d1, c1)
    cmp(c1, d1)
    try:
        a, b = Type1(10), Type2(20)
        # Raises TypeError since a.__add__(b) and b.__radd__(a)
        # both return NotImplemented object.
        print(a + b) # type: ignore
    except TypeError as e:
        print(str(e))


if __name__ == "__main__":
    main()
