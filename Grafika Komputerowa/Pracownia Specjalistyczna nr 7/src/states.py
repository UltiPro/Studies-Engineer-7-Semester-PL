import tkinter as tk
from abc import ABC, abstractmethod
from typing import Callable

from src.canvas import CustomCanvas
from src.math2d import Mat3, Vec2
from src.shapes import Shape


class State(ABC):
    def __init__(self, canvas: CustomCanvas, state_callback: Callable):
        self.canvas = canvas
        self.set_state = state_callback

    @abstractmethod
    def bind(self):
        raise NotImplementedError()

    @abstractmethod
    def unbind(self):
        raise NotImplementedError()

    def confirm(self):
        pass

    def exit_state(self, event=None):
        self.set_state(SelectState(self.canvas, self.set_state))


class SelectState(State):
    def bind(self):
        self.canvas.bind("<Button-1>", self.__select)

    def unbind(self):
        self.canvas.unbind("<Button-1>")

    def __select(self, event: tk.Event):
        selected = None
        shapes = self.canvas.shapes
        for shape in reversed(shapes):
            if shape.is_colliding(Vec2(event.x, event.y)):
                selected = shape
                break

        self.canvas.selected = selected
        if selected:
            shapes.append(shapes.pop(shapes.index(selected)))

        self.canvas.draw()


class FocalState(State):
    def bind(self):
        self.canvas.bind("<Button-1>", self.__set_focal)

    def unbind(self):
        self.canvas.unbind("<Button-1>")

    def __set_focal(self, event: tk.Event):
        self.canvas.focal_point = Vec2(event.x, event.y)
        self.canvas.draw()


class CreateState(State):
    def __init__(self, canvas: CustomCanvas, state_callback: Callable):
        super().__init__(canvas, state_callback)
        self.points: list[Vec2] = []

    def bind(self):
        self.canvas.bind("<Button-1>", self.__add_point)

    def unbind(self):
        self.canvas.unbind("<Button-1>")

    def confirm(self):
        self.canvas.shapes.append(Shape.from_vectors(self.points))
        self.canvas.draw()

    def __add_point(self, event: tk.Event):
        self.points.append(Vec2(event.x, event.y))
        self.canvas.draw(new_shape=self.points)


class TranslateState(State):
    def __init__(
        self,
        canvas: CustomCanvas,
        state_callback: Callable,
        in_tx: tk.Entry,
        in_ty: tk.Entry,
    ):
        super().__init__(canvas, state_callback)

        if self.canvas.selected is not None:
            self.selected = self.canvas.selected
            self.origin = self.canvas.selected.get_center()

        self.translate_vector = Vec2()

        self.in_tx = in_tx
        self.in_ty = in_ty
        self.__configure_inputs()

    def bind(self):
        if self.canvas.selected is None:
            self.exit_state()
            return

        self.canvas.bind("<Motion>", self.__move)
        self.canvas.bind("<Button-1>", self.__place)

    def unbind(self):
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<Button-1>")
        self.__remove_input_trace()

    def confirm(self):
        transformation_matrix = Mat3.translation_matrix(*self.translate_vector)
        self.selected.transform(transformation_matrix)
        self.canvas.draw()

    def __configure_inputs(self):
        self.svx = tk.StringVar()
        self.svx.trace_add("write", self.__text_input)
        self.in_tx.configure(textvariable=self.svx)
        self.svy = tk.StringVar()
        self.svy.trace_add("write", self.__text_input)
        self.in_ty.configure(textvariable=self.svy)

    def __remove_input_trace(self):
        self.svx = tk.StringVar()
        self.svy = tk.StringVar()
        self.in_tx.configure(textvariable=self.svx)
        self.in_ty.configure(textvariable=self.svy)

    def __move(self, event: tk.Event):
        dx = event.x - self.origin.x
        dy = event.y - self.origin.y
        self.svx.set(str(dx))
        self.svy.set(str(dy))
        self.__update_preview(dx, dy)

    def __text_input(self, var, index, mode):
        x = self.in_tx.get()
        y = self.in_ty.get()
        x = int(x) if x else 0
        y = int(y) if y else 0
        self.__update_preview(x, y)

    def __update_preview(self, x: int, y: int):
        self.translate_vector.set(x, y)

        transformation_matrix = Mat3.translation_matrix(x, y)
        preview_shape = self.selected.copy()
        preview_shape.transform(transformation_matrix)

        self.canvas.draw(preview=preview_shape)

    def __place(self, event: tk.Event):
        self.confirm()
        self.set_state(SelectState(self.canvas, self.set_state))


class RotateState(State):
    def __init__(
        self,
        canvas: CustomCanvas,
        state_callback: Callable,
        in_rd: tk.Entry,
    ):
        super().__init__(canvas, state_callback)

        if self.canvas.selected is not None:
            self.selected = self.canvas.selected
            self.origin = self.canvas.selected.get_center()

        self.degrees = 0

        self.in_rd = in_rd
        self.__configure_inputs()

    def bind(self):
        if self.canvas.selected is None:
            self.exit_state()
            return

        self.canvas.bind("<Motion>", self.__move)
        self.canvas.bind("<Button-1>", self.__place)

    def unbind(self):
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<Button-1>")
        self.__remove_input_trace()

    def confirm(self):
        rotation_matrix = Mat3.rotation_matrix(self.degrees)
        transformation_matrix = Mat3.with_focal(
            rotation_matrix, self.canvas.focal_point
        )
        self.selected.transform(transformation_matrix)
        self.canvas.draw()

    def __configure_inputs(self):
        self.svd = tk.StringVar()
        self.svd.trace_add("write", self.__text_input)
        self.in_rd.configure(textvariable=self.svd)

    def __remove_input_trace(self):
        self.svd = tk.StringVar()
        self.in_rd.configure(textvariable=self.svd)

    def __move(self, event: tk.Event):
        degs = event.x - self.origin.x
        self.svd.set(str(degs))
        self.__update_preview(degs)

    def __text_input(self, var, index, mode):
        degs = self.in_rd.get()
        degs = int(degs) if degs else 0
        self.__update_preview(degs)

    def __update_preview(self, degs: int):
        self.degrees = degs

        rotation_matrix = Mat3.rotation_matrix(degs)
        transformation_matrix = Mat3.with_focal(
            rotation_matrix, self.canvas.focal_point
        )
        preview_shape = self.selected.copy()
        preview_shape.transform(transformation_matrix)

        self.canvas.draw(preview=preview_shape)

    def __place(self, event: tk.Event):
        self.confirm()
        self.set_state(SelectState(self.canvas, self.set_state))


class ScaleState(State):
    def __init__(
        self,
        canvas: CustomCanvas,
        state_callback: Callable,
        in_sx: tk.Entry,
        in_sy: tk.Entry,
    ):
        super().__init__(canvas, state_callback)

        if self.canvas.selected is not None:
            self.selected = self.canvas.selected
            self.origin = Vec2(350, 350)

        self.scalex = 1.0
        self.scaley = 1.0

        self.in_sx = in_sx
        self.in_sy = in_sy
        self.__configure_inputs()

    def bind(self):
        if self.canvas.selected is None:
            self.exit_state()
            return

        self.canvas.bind("<Motion>", self.__move)
        self.canvas.bind("<Button-1>", self.__place)

    def unbind(self):
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<Button-1>")
        self.__remove_input_trace()

    def confirm(self):
        scale_matrix = Mat3.scale_matrix(self.scalex, self.scaley)
        transformation_matrix = Mat3.with_focal(scale_matrix, self.canvas.focal_point)
        self.selected.transform(transformation_matrix)
        self.canvas.draw()

    def __configure_inputs(self):
        self.svx = tk.StringVar()
        self.svx.set("1")
        self.svx.trace_add("write", self.__text_input)
        self.in_sx.configure(textvariable=self.svx)
        self.svy = tk.StringVar()
        self.svy.set("1")
        self.svy.trace_add("write", self.__text_input)
        self.in_sy.configure(textvariable=self.svy)

    def __remove_input_trace(self):
        self.svx = tk.StringVar()
        self.svy = tk.StringVar()
        self.in_sx.configure(textvariable=self.svx)
        self.in_sy.configure(textvariable=self.svy)

    def __move(self, event: tk.Event):
        dx = event.x - self.origin.x - 1
        dy = event.y - self.origin.y - 1
        self.svx.set(str(dx / 100))
        self.svy.set(str(dy / 100))
        self.__update_preview(dx, dy)

    def __text_input(self, var, index, mode):
        x = self.in_sx.get()
        y = self.in_sy.get()
        x = float(x) if x else 0
        y = float(y) if y else 0
        self.__update_preview(x * 100, y * 100)

    def __update_preview(self, x: float, y: float):
        self.scalex = x / 100
        self.scaley = y / 100

        scale_matrix = Mat3.scale_matrix(self.scalex, self.scaley)
        transformation_matrix = Mat3.with_focal(scale_matrix, self.canvas.focal_point)
        preview_shape = self.selected.copy()
        preview_shape.transform(transformation_matrix)

        self.canvas.draw(preview=preview_shape)

    def __place(self, event: tk.Event):
        self.confirm()
        self.set_state(SelectState(self.canvas, self.set_state))
