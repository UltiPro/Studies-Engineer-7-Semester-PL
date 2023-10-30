import tkinter as tk
from typing import Protocol
from operations import AddOperation, DivOperation, MulOperation, SubOperation
from filters import GrayscaleFilter, GrayscaleFilterThree, GrayscaleFilterTwo


class Operation(Protocol):
    def transform(self, val, transformation_val) -> int:
        ...


def clamp(val, min, max):
    if val < min:
        return min
    if val > max:
        return max
    return val


def create_lut(op: Operation, val) -> dict[int, int]:
    lut = dict()
    for i in range(256):
        lut[i] = clamp(op.transform(i, val), 0, 255)
    return lut


class PointFrame(tk.Frame):
    def __init__(self, parent, image_frame, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.image_frame = image_frame
        self.r_label = tk.Label(self, text="r:")
        self.r_label.grid(row=0, column=0)
        self.val_r = tk.Entry(self, width=4)
        self.val_r.grid(row=0, column=1)
        self.g_label = tk.Label(self, text="g:")
        self.g_label.grid(row=1, column=0)
        self.val_g = tk.Entry(self, width=4)
        self.val_g.grid(row=1, column=1)
        self.b_label = tk.Label(self, text="b:")
        self.b_label.grid(row=2, column=0)
        self.val_b = tk.Entry(self, width=4)
        self.val_b.grid(row=2, column=1)
        self.val_light = tk.Entry(self)
        self.add = tk.Button(
            self, text="+", command=lambda: self.__send_luts(AddOperation())
        )
        self.sub = tk.Button(
            self, text="-", command=lambda: self.__send_luts(SubOperation())
        )
        self.mul = tk.Button(
            self, text="*", command=lambda: self.__send_luts(MulOperation())
        )
        self.div = tk.Button(
            self, text="/", command=lambda: self.__send_luts(DivOperation())
        )
        self.light_level = tk.Button(
            self,
            text="brightness",
            command=lambda: self.__send_single_lut(AddOperation()),
        )
        self.gr1 = tk.Button(
            self,
            text="gray 1",
            command=lambda: self.__send_gs_filter(GrayscaleFilter()),
        )
        self.gr2 = tk.Button(
            self,
            text="gray 2",
            command=lambda: self.__send_gs_filter(GrayscaleFilterTwo()),
        )
        self.gr3 = tk.Button(
            self,
            text="gray 3",
            command=lambda: self.__send_gs_filter(GrayscaleFilterThree()),
        )
        self.add.grid(row=3, column=0, sticky=tk.EW)
        self.sub.grid(row=3, column=1, sticky=tk.EW)
        self.mul.grid(row=4, column=0, sticky=tk.EW)
        self.div.grid(row=4, column=1, sticky=tk.EW)
        self.val_light.grid(row=5, column=0, columnspan=2, sticky=tk.EW)
        self.light_level.grid(row=7, column=0, columnspan=2, sticky=tk.EW)
        self.gr1.grid(row=8, column=0, columnspan=2, sticky=tk.EW)
        self.gr2.grid(row=9, column=0, columnspan=2, sticky=tk.EW)
        self.gr3.grid(row=10, column=0, columnspan=2, sticky=tk.EW)

    def __send_luts(self, op: Operation):
        results = validate_inputs(self.val_r, self.val_g, self.val_b)
        if len(results) != 3:
            return
        luts = [
            create_lut(op, results[0]),
            create_lut(op, results[1]),
            create_lut(op, results[2]),
        ]
        self.image_frame.apply_luts(luts)

    def __send_single_lut(self, op: Operation):
        try:
            val = float(self.val_light.get())
            self.val_light.configure(background='white')
        except:
            self.val_light.delete(0, tk.END)
            self.val_light.configure(background='red')
            return
        luts = [create_lut(op, val)]
        self.image_frame.apply_luts(luts)

    def __send_gs_filter(self, filter):
        self.image_frame.apply_filter(filter)


class SidebarPoint(tk.Frame):
    def __init__(self, parent, image_frame, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.image_frame = image_frame
        self.point_frame = PointFrame(self, image_frame)

    def show_point_frame(self):
        self.point_frame.pack()


def validate_inputs(r: tk.Entry, g: tk.Entry, b: tk.Entry) -> list[float]:
    vals = []

    for input in r, g, b:
        try:
            val = float(input.get())
            vals.append(val)
            input.configure(background="white")
        except:
            input.delete(0, tk.END)
            input.configure(background="red")

    return vals
