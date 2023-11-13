from dataclasses import dataclass


@dataclass
class Vec2:
    x: int
    y: int

    def set(self, x: int, y: int):
        self.x = x
        self.y = y

    def change(self, dx: int, dy: int):
        self.x += dx
        self.y += dy

    def dist(self, other: "Vec2"):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


class Point(Vec2):
    def check_collision(self, mouse_pos: Vec2):
        if self.dist(mouse_pos) < 10:
            return True
        return False
