import tkinter as tk
from dataclasses import dataclass

from src.math2d import Matrix, Vec2, intersect, vec_mul_mat


@dataclass
class Shape:
    coords: list[int]

    @classmethod
    def from_vectors(cls, vectors: list[Vec2]):
        coords: list[int] = []
        for vec in vectors:
            coords.append(vec.x)
            coords.append(vec.y)
        return cls(coords)

    def as_vector_list(self) -> list[Vec2]:
        vecs: list[Vec2] = []
        for i in range(0, len(self.coords), 2):
            vecs.append(Vec2(self.coords[i], self.coords[i + 1]))

        return vecs

    def transform(self, matrix: Matrix):
        vecs = self.as_vector_list()
        new_vecs: list[Vec2] = []
        for vec in vecs:
            new_vecs.append(vec_mul_mat(vec, matrix))

        self.coords = Shape.from_vectors(new_vecs).coords

    def copy(self) -> "Shape":
        return Shape(self.coords)

    def is_colliding(self, point: Vec2):
        line = (point, Vec2(point.x, 0))
        vecs = self.as_vector_list()

        intersect_count = 0
        for i in range(len(vecs)):
            next = (i + 1) % len(vecs)
            if intersect(*line, vecs[i], vecs[next]):
                intersect_count += 1

        return intersect_count % 2 == 1

    def get_center(self) -> Vec2:
        vecs = self.as_vector_list()
        center_x = round(sum([vec.x for vec in vecs]) / len(vecs))
        center_y = round(sum([vec.y for vec in vecs]) / len(vecs))

        return Vec2(center_x, center_y)

    def draw(self, canvas: tk.Canvas, color: str, outline: str):
        canvas.create_polygon(self.coords, fill=color, outline=outline)
