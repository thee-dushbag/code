from typing import TypeVar

T = TypeVar("T")
U = TypeVar("U")


class mSet(set[T]):
    def __mul__(self, other: set[U]):
        # Cartesian Product
        return mSet((a, b) for a in self for b in other)

    def __str__(self) -> str:
        return "{" + ", ".join(repr(v) for v in sorted(self)) + "}"  # type: ignore

    __repr__ = __str__

    def __and__(self, other: set[U]):  # type: ignore
        return mSet(super().__and__(other))

    def __or__(self, other: set[U]):  # type: ignore
        return mSet(super().__or__(other))


A = mSet({1, 2, 3})
B = mSet({"a", "b"})
C = mSet({"a", "c"})
T = mSet({1, 2})

print(f"{A * B = }")
print(f"{B * A = }")
print()
print(f"{T * B = }")
print(f"{A * C = }")
print()
print(f"{A * (B & C)       = }")
print(f"{(A * B) & (A * C) = }")
print()
print(f"{A * (B | C)       = }")
print(f"{(A * B) | (A * C) = }")
print()
print(f"{A * (B - C)       = }")
print(f"{(A * B) - (A * C) = }")
