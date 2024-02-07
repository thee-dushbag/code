from mpack.logging import logger, Level


class _ValStr:
    val: str

    def __str__(self) -> str:
        clsname = self.__class__.__name__
        value = getattr(self, self.val, NotImplemented)
        return f"{clsname}({self.val}={value!r})"

    __repr__ = __str__


class A(_ValStr):
    val = "_a"

    def __init__(self, a: int) -> None:
        self._a = a

    def __add__(self, other: "A") -> "A":
        logger.info(f"A.__add__(self={self}, other={other})")
        if isinstance(other, A):
            return A(self._a + other._a)
        return NotImplemented

    def __radd__(self, other: int) -> "A":
        logger.info(f"A.__radd__(self={self}, other={other})")
        if isinstance(other, int):
            return A(self._a + other)
        return NotImplemented


class B(_ValStr):
    val = "_b"

    def __init__(self, b: int) -> None:
        self._b = b

    def _add(self, other: "A | B"):
        match other:
            case A(_a=value) | B(_b=value):
                return B(self._b + value)
            case _:
                return NotImplemented

    def __add__(self, other: "A | B"):
        logger.warn(f"B.__add__(self={self}, other={other})")
        return self._add(other)

    def __radd__(self, other: "A | B") -> "B":
        logger.warn(f"B.__radd__(self={self}, other={other})")
        return self._add(other)


class mint(int):
    def __add__(self, other: int | B) -> int:
        logger.warn(f"mint.__add__(self={self}, other={other})")
        match other:
            case B(_b=value) | (int() as value):
                return super().__add__(value)
            case _:
                return NotImplemented


def main():
    a, b = A(5), B(10)
    c, d = A(7), B(15)
    print(a, b, c, d)
    print(a + b)
    print(b + a)
    print(5 + a)
    print(mint(5) + a)
    print(mint(100) + d)
    print(a + c)


if __name__ == "__main__":
    logger.turnon(Level.INFO)
    logger.turnon(Level.WARN)
    logger.mute()
    main()
