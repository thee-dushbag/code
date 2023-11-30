class Vector(list[float]):
    @property
    def size(self) -> int:
        return self.__len__()

    @property
    def magnitude(self) -> float:
        from math import sqrt

        return sqrt(sum(x * x for x in self))

    def __str__(self) -> str:
        return f'Vector<{self.size}>' + '{' + ", ".join(str(x) for x in self) + '}'


def dot_product_algebraic(v: Vector, u: Vector, /) -> float:
    assert (
        v.size == u.size
    ), f"dot_product on vectors without a common size, v<{v.size}> != u<{u.size}>"
    return sum(a * b for a, b in zip(v, u))


def dot_product_geometric(angle: float, mag_v: float, mag_u: float, /) -> float:
    import math

    return mag_u * mag_v * math.cos(angle)


def vector_angle(v: Vector, u: Vector, /) -> float:
    from math import acos

    return acos(dot_product_algebraic(v, u) / (v.magnitude * u.magnitude))
