import math

RADIUS: float = 1
ACCURACY: int = 36_000


def heros_isoscles_area(a: float, b: float):
    s = (a + a + b) / 2
    sa, sb = s - a, s - b
    return math.sqrt(s * sa * sa * sb)


Degrees = float


def vector_triangle_area(base: float, angle: Degrees):
    import vectors as v

    # Create a matrix transformation for rotating vectors by <angle> degrees
    matrix = v.rotateby(angle)
    v1 = v.Vector([base, 0])  # Vector lying on the x_axis
    v2 = v.matvecmul(matrix, v1)  # Rotate v1 by <angle> towards the y_axis
    y_axis = v.Vector([0, 1])  # y_axis unit vector
    height = v.project(v2, y_axis)  # Project v2 onto the y_axis to get the height
    # The area of the parallerogram divided by 2 is the
    # area of the triangle formed by vectors v1 and v2
    return (base * height) / 2


def area_polygon(divisions: int, side: float) -> float:
    theta = math.tau / divisions
    base = side * math.sqrt(2 * (1 - math.cos(theta)))
    area = heros_isoscles_area(side, base) * divisions
    return area


def area_polygon2(divisions: int, side: float) -> float:
    return vector_triangle_area(side, 360 / divisions) * divisions


def area_circle_integral(x: float, r: float):
    expr = (x * math.sqrt(r**2 - x**2)) / r**2
    return (r**2 / 2) * (expr + math.asin(x / r))


def area_circle(radius: float):
    assert radius > 0, "Expected radius > 0, got %s" % radius
    ai = area_circle_integral(0, radius)
    bi = area_circle_integral(radius, radius)
    return 4 * (bi - ai)


def geometric_pi(divisions: int = ACCURACY, radius: float = RADIUS) -> float:
    area = area_polygon(divisions, radius)
    return area / radius**2


def vectors_pi(divisions: int = ACCURACY, radius: float = RADIUS) -> float:
    area = area_polygon2(divisions, radius)
    return area / radius**2


def algebraic_pi(radius: float = RADIUS):
    area = area_circle(radius)
    return area / radius**2


def main():
    a_pi = (
        algebraic_pi()
    )  # Surprisingly accurate, though not surprised due to being calculus
    g_pi = (
        geometric_pi()
    )  # Has an accuracy sweetspot where more or less leads to loss in PI accuracy
    v_pi = vectors_pi(360_000_000)  # Gets accurate the bigger the number
    print("geometric_pi: %s" % g_pi)
    print("vectors_pi  : %s" % v_pi)
    print("algebraic_pi: %s" % a_pi)
    print("accurate_pi : %s" % math.pi)


if __name__ == "__main__":
    main()
