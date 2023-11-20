import math
from dataclasses import dataclass


@dataclass
class Vec2:
    x: int = 0
    y: int = 0

    def set(self, x: int, y: int):
        self.x = x
        self.y = y

    def neg(self):
        return Vec2(-self.x, -self.y)

    def __iter__(self):
        for val in [self.x, self.y]:
            yield val


Matrix = list[list[float]]


class Mat3:
    @staticmethod
    def empty() -> Matrix:
        mat: Matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        return mat

    @staticmethod
    def identity() -> Matrix:
        mat = Mat3.empty()
        for i in range(3):
            mat[i][i] = 1
        return mat

    @staticmethod
    def translation_matrix(x: float, y: float):
        mat = Mat3.identity()
        mat[0][2] = x
        mat[1][2] = y
        return mat

    @staticmethod
    def rotation_matrix(degrees: int):
        rads = math.radians(degrees)
        mat = Mat3.identity()
        mat[0][0] = math.cos(rads)
        mat[0][1] = -math.sin(rads)
        mat[1][0] = math.sin(rads)
        mat[1][1] = math.cos(rads)
        return mat

    @staticmethod
    def scale_matrix(factor_x: float, factor_y: float):
        mat = Mat3.identity()
        mat[0][0] = factor_x
        mat[1][1] = factor_y
        return mat

    @staticmethod
    def with_focal(matrix: Matrix, focal: Vec2):
        trans_mat = Mat3.translation_matrix(*focal)
        trans_mat_rev = Mat3.translation_matrix(*focal.neg())

        mat = mat_mul(trans_mat, matrix)
        mat = mat_mul(mat, trans_mat_rev)

        return mat


def mat_mul(a: Matrix, b: Matrix) -> Matrix:
    mat = Mat3.empty()
    for row in range(3):
        for col in range(3):
            for i in range(3):
                mat[row][col] += a[row][i] * b[i][col]
    return mat


def vec_mul_mat(v: Vec2, m: Matrix) -> Vec2:
    vec = Vec2()
    vec.x = round(v.x * m[0][0] + v.y * m[0][1] + m[0][2])
    vec.y = round(v.x * m[1][0] + v.y * m[1][1] + m[1][2])

    return vec


def ccw(a: Vec2, b: Vec2, c: Vec2):
    return (c.y - a.y) * (b.x - a.x) > (b.y - a.y) * (c.x - a.x)


def intersect(a: Vec2, b: Vec2, c: Vec2, d: Vec2):
    return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)
