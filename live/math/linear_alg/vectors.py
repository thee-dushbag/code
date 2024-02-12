import typing as ty, math


class Vector(list[float]):
    @property
    def size(self) -> int:
        return self.__len__()

    @property
    def _magnitude(self) -> float:
        return sum(x**2 for x in self)

    @property
    def magnitude(self) -> float:
        from math import sqrt

        return sqrt(self._magnitude)

    def __str__(self) -> str:
        return f"Vector<{self.size}>" + "{" + ", ".join(str(x) for x in self) + "}"

    def __sub__(self, other: "Vector") -> "Vector":
        assert self.size == other.size
        return Vector(self[i] - other[i] for i in range(self.size))

    def __mul__(self, scalar: float) -> "Vector":
        return Vector(x * scalar for x in self)

    def __rmul__(self, scalar: float) -> "Vector":
        return self * scalar

    def unit(self) -> "Vector":
        mag = self.magnitude
        return Vector(x / mag for x in self)


def _assert_dim(a: Vector, dim: int):
    assert a.size == dim, f"Expected vector {a} to be of dimension {dim}"


def _assert_same(a: Vector, b: Vector):
    _assert_dim(b, a.size)


def dot_product_algebraic(v: Vector, u: Vector, /) -> float:
    _assert_same(v, u)
    return sum(a * b for a, b in zip(v, u))


def dot_product_geometric(a: Vector, b: Vector, /) -> float:
    _assert_same(a, b)
    angle = vector_angle(a, b)
    mag_a = a.magnitude
    mag_b = b.magnitude
    return mag_a * mag_b * math.cos(angle)


def vector_angle(v: Vector, u: Vector, /) -> float:
    dot = dot_product_algebraic(v, u)
    mag = v.magnitude * u.magnitude
    return math.degrees(math.acos(dot / mag))


def _assert3d(a: Vector, b: Vector):
    _assert_dim(a, 3)
    _assert_dim(b, 3)


def cross_product_algebraic(a: Vector, b: Vector):
    _assert3d(a, b)
    m, n, o = a
    x, y, z = b
    i = n * z - o * y
    j = o * x - m * z
    k = m * y - n * x
    return Vector([i, j, k])


@ty.overload
def cross_product_geometric(a: Vector, b: Vector) -> float:
    ...


@ty.overload
def cross_product_geometric(a: Vector, b: Vector, d: Vector) -> Vector:
    ...


def cross_product_geometric(a: Vector, b: Vector, d: Vector | None = None):
    _assert3d(a, b)
    angle = vector_angle(a, b)
    mag_ab = a.magnitude * b.magnitude
    mag = mag_ab * math.sin(angle)
    return mag if d is None else d * mag


def perpendicular(a: Vector, w: Vector) -> Vector:
    dot_aw = dot_product_algebraic(w, a)
    scalar = dot_aw / a._magnitude
    scaled = a * scalar
    return w - scaled


def is_parallel(a: Vector, b: Vector):
    return a.unit() == b.unit()


def project(a: Vector, b: Vector):
    return abs(dot_product_algebraic(a, b) / b.magnitude)


def is_perpendicular(a: Vector, b: Vector) -> bool:
    return dot_product_algebraic(a, b) == 0


def matvecmul(mat: list[list[float]] | list[Vector], vec: list[float] | Vector):
    assert len(mat[0]) == len(vec)
    result = []
    for v1 in mat:
        dot = dot_product_algebraic(Vector(v1), Vector(vec))
        result.append(dot)
    return Vector(result)



def matscalarmul(scalar: float, mat: list[list[float]] | list[Vector]):
    return [Vector(scalar * coord for coord in v) for v in mat]


import math

Degrees = float
def rotateby(angle: Degrees):
    angle = math.radians(angle)
    cos = math.cos(angle)
    sin = math.sin(angle)
    return [Vector([cos, sin]), Vector([-sin, cos])]


