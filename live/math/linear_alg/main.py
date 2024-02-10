import lazy as z
from vectors import (
    Vector,
    dot_product_algebraic,
    vector_angle,
    perpendicular,
    cross_product_algebraic,
    cross_product_geometric,
    project,
    is_parallel,
)


def main1():
    v = Vector([1, 2, 3])
    print(f"{v}.magnitude = {v.magnitude}")
    u = Vector([4, 5, 6])
    print(f"dot({v}, {u}) = {dot_product_algebraic(v, u)}")
    print(f"dot({u}, {v}) = {dot_product_algebraic(u, v)}")
    print(f"angle({v}, {u}) = {vector_angle(v, u)}")


def main2():
    pb = Vector([17, 2, -13])
    upb = pb.unit()
    b = Vector([4, 5, 6])
    cpb = perpendicular(b, Vector([1, 1, 1]))
    ucpb = cpb.unit()
    print(pb, cpb)
    print(upb, ucpb, sep="\n")
    print(ucpb == upb)


def main3():
    a = Vector([1, 2, 3])
    b = Vector([4, 5, 6])
    ab = cross_product_algebraic(a, b)
    print(ab, ab.magnitude)
    abg = cross_product_geometric(a, b, ab.unit())
    print(abg, abg.magnitude)


def main4():
    a = Vector([1, 2, 3])
    b = Vector([4, 5, 6])
    pb = perpendicular(b, Vector([1, 1, 1]))
    height = project(a, pb)
    c_area = height * b.magnitude
    area = cross_product_geometric(a, b)
    print(c_area, area)


def main5():
    a = Vector([1, 2, 3])
    b = Vector([4, 5, 6])
    ab = cross_product_algebraic(a, b)
    ba = cross_product_algebraic(b, a)
    print(ab, ba, ba * -1, sep="\n")
    assert ab == -1 * ba


def main6():
    a = Vector([2, 2, 2])
    b = Vector([3, 3, 3])
    c = Vector([1, 2, 3])
    print(f"{a.unit()=}")
    print(f"{b.unit()=}")
    print(f"{c.unit()=}")
    abp = is_parallel(a, b)
    acp = is_parallel(a, c)
    bcp = is_parallel(b, c)
    print(f"{a} // {b}: {abp}")
    print(f"{a} // {c}: {acp}")
    print(f"{b} // {c}: {bcp}")


def main7():
    b = z.Vector(map(z.number, [2, 2, 2]))
    print(b.unit())
    a = z.Vector(map(z.number, [1, 2, 3]))
    b = z.Vector(map(z.number, [4, 5, 6]))
    print(z.absolute(a))
    print(a.magnitude())
    print(a.magnitude() == z.absolute(a))
    print(z.evaluate(a.magnitude()) == z.evaluate(z.absolute(a)))


def main8():
    a = Vector([1, 2, 3])
    b = Vector([4, 5, 6])
    ab = cross_product_algebraic(a, b)
    c = perpendicular(b, a)
    # print(ab, c)
    # print(ab.unit(), c.unit(), sep="\n")
    a = Vector([4, 6])
    b = Vector([8, 7])
    pa = perpendicular(a, Vector([-5, -7]))
    pb = perpendicular(b, Vector([1, 99]))
    print(dot_product_algebraic(pa, a))
    print(dot_product_algebraic(pb, b))
    scale = dot_product_algebraic(a, pb)
    print(scale / a.magnitude)
    print(scale / pb.magnitude)


import math


def matvecmul(mat: list[list[float]] | list[Vector], vec: list[float] | Vector):
    assert len(mat[0]) == len(vec)
    result = []
    for v1 in mat:
        dot = dot_product_algebraic(Vector(v1), Vector(vec))
        result.append(dot)
    return Vector(result)


Degrees = float

def matscalarmul(scalar: float, mat: list[list[float]] | list[Vector]):
    return [Vector(scalar * coord for coord in v) for v in mat]

def rotateby(angle: Degrees):
    angle = math.radians(angle)
    cos = math.cos(angle)
    sin = math.sin(angle)
    return [Vector([cos, sin]), Vector([-sin, cos])]


def main():
    # mat = [Vector([0, -1]), Vector([1, 0])]
    # mat = [Vector([0, 0.25]), Vector([-0.25, 0])]
    # v1 = Vector([1, 0])
    # v2 = matvecmul(mat, v1)
    # print(v1, "->", v2)
    # theta = vector_angle(v1, v2)
    # print("Angle:", theta)
    # mat60 = rotateby(-45)
    # v3 = matvecmul(mat60, v1)
    # print(mat60)
    # print(v1, "/ 60 /", v3, ":", vector_angle(v1, v3))
    v1 = Vector([5, 6])
    mat = rotateby(-30)
    v2 = matvecmul(mat, v1)
    print(v1, v2, v1.magnitude, v2.magnitude)
    angle = vector_angle(v1, v2)
    print(angle)


if __name__ == "__main__":
    main()
