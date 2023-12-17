class long_func2:
    def __new__(
        cls,
        n: int,
        /,
        *,
        POW1: int = 2,
        POW2: int = 3,
        PLUS: int = 4,
        DIV: int = 4,
        MOD: int = 6,
    ) -> int:
        cls.__n: int = n
        return cls.powX(POW1).plusX(PLUS).divX(DIV).powX(POW2).modX(MOD).__n

    @classmethod
    def plusX(cls, X: int = 5, /):
        cls.__n += X
        return cls

    @classmethod
    def divX(cls, X: int = 4, /):
        cls.__n = round(cls.__n / X)
        return cls

    @classmethod
    def powX(cls, X: int = 3, /):
        cls.__n **= X
        return cls

    @classmethod
    def modX(cls, X: int = 6, /):
        cls.__n %= X
        return cls


def long_func(n: int, /) -> int:
    n = n**2
    n = n + 5
    n = round(n / 4)
    n = n**3
    n = n % 6
    return n


val = long_func(90)
val2 = long_func2(90)
print(val, val2, sep="\n")
