import tkinter as tk
from enum import Enum, auto
from typing import Optional
from bezier import *
from points import Point, Vec2

PT_RADIUS = 20


class InputState(Enum):
    INSERT = auto()
    MODIFY = auto()


class CustomCanvas(tk.Canvas):
    def __init__(self, parent, width: int, height: int, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, width=width, height=height, **kwargs)
        self.dims = width, height
        self.steps = 1000
        self.show_lines = True
        self.points: list[Point] = []
        self.clicked_point: Optional[Point] = None
        self.last_mouse_pos = Vec2(0, 0)
        self.configure(bg="#212733")
        self.bind("<Key>", self.__handle_keys)
        self.bind("<Button-1>", self.__mouse_insert)
        self.focus_set()

    def set_steps(self, steps: int):
        self.steps = steps
        self.redraw_curve()

    def redraw_curve(self):
        self.delete("all")
        if self.show_lines:
            for i in range(len(self.points) - 1):
                curr_point = self.points[i]
                next_point = self.points[i + 1]
                self.create_line(
                    curr_point.x,
                    curr_point.y,
                    next_point.x,
                    next_point.y,
                    fill="#425e5e",
                )
        bezier_curve_points = construct_bezier_curve(self.points, self.steps)
        for x, y in bezier_curve_points:
            self.create_line(x, y, x + 1, y, fill="#d9d7ce")
        for point in self.points:
            self.create_oval(
                point.x - PT_RADIUS,
                point.y - PT_RADIUS,
                point.x + PT_RADIUS,
                point.y + PT_RADIUS,
                fill="#e85c51",
                outline="#e85c51",
            )

    def __handle_keys(self, event: tk.Event):
        if event.char == "i":
            self.bind("<Button-1>", self.__mouse_insert)
            self.unbind("<B1-Motion>")
        elif event.char == "o":
            self.bind("<Button-1>", self.__mouse_modify)
            self.bind("<B1-Motion>", self.__mouse_modify_drag)
        elif event.char == "d":
            self.points = []
        elif event.char == "q":
            self.steps -= 50
        elif event.char == "e":
            self.steps += 50
        elif event.char == "h":
            self.show_lines = not self.show_lines
        self.redraw_curve()

    def __mouse_insert(self, event: tk.Event):
        self.points.append(Point(event.x, event.y))
        self.redraw_curve()

    def __mouse_modify(self, event: tk.Event):
        self.last_mouse_pos.set(event.x, event.y)
        self.clicked_point = None
        for p in reversed(self.points):
            if p.check_collision(self.last_mouse_pos):
                self.clicked_point = p

    def __mouse_modify_drag(self, event: tk.Event):
        dx = event.x - self.last_mouse_pos.x
        dy = event.y - self.last_mouse_pos.y
        self.last_mouse_pos.set(event.x, event.y)
        if self.clicked_point is not None:
            self.clicked_point.change(dx, dy)
            self.redraw_curve()
