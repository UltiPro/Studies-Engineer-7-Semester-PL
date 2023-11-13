import math
from points import Point


def get_polynomial_coefficient(i, n):
    return math.factorial(n) / float(math.factorial(i) * math.factorial(n - i))


def get_polynomial_term(i, n, t):
    return get_polynomial_coefficient(i, n) * (t**i) * (1 - t) ** (n - i)


def get_curve_point(points: list[Point], t):
    x = 0
    y = 0
    n = len(points) - 1
    for i, point in enumerate(points):
        polynomial_term = get_polynomial_term(i, n, t)
        x += polynomial_term * point.x
        y += polynomial_term * point.y
    return x, y


def construct_bezier_curve(points: list[Point], n) -> list[tuple[int, int]]:
    points_in_curve = []
    for i in range(n):
        t = i / float(n - 1)
        points_in_curve.append(get_curve_point(points, t))

    return points_in_curve
