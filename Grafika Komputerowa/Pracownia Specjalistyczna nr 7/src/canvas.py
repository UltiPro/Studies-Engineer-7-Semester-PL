import tkinter as tk
from typing import Optional

from src.math2d import Vec2
from src.shapes import Shape

C_BG = "#212733"
C_SHAPE = "#d9d7ce"
C_SELECTED = "#f28779"
C_POINT = "#e85c51"
C_PREVIEW = "#425e5e"


class CustomCanvas(tk.Canvas):
    def __init__(self, parent, width: int, height: int, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, width=width, height=height, **kwargs)
        self.configure(bg=C_BG)

        self.dims = width, height
        self.shapes: list[Shape] = []
        self.focal_point = Vec2(0, height)
        self.selected: Optional[Shape] = None
        self.preview_loc: Optional[Vec2] = None
        self.draw()

    def draw(
        self, new_shape: Optional[list[Vec2]] = None, preview: Optional[Shape] = None
    ):
        self.delete("all")

        for shape in self.shapes:
            color = C_SELECTED if shape == self.selected else C_SHAPE
            shape.draw(self, color, outline=C_BG)

        self.__draw_point(self.focal_point, 6)

        if new_shape is not None:
            for i in range(len(new_shape) - 1):
                self.create_line(
                    new_shape[i].x,
                    new_shape[i].y,
                    new_shape[i + 1].x,
                    new_shape[i + 1].y,
                    fill=C_PREVIEW,
                )
            for point in new_shape:
                self.__draw_point(point, 4, color=C_SHAPE)

        if preview is not None:
            preview.draw(self, C_PREVIEW, outline=C_BG)

    def __draw_point(self, pos: Vec2, radius: int, color=C_POINT):
        self.create_oval(
            pos.x - radius,
            pos.y - radius,
            pos.x + radius,
            pos.y + radius,
            fill=color,
        )
