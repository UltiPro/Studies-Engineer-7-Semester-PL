import tkinter as tk
from tkinter.filedialog import askopenfilename

from image_frame import ImageFrame
from morph import closing, dilation, erosion, hitandmiss, opening


class Panel(tk.Frame):
    def __init__(self, parent, image_frame: ImageFrame, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.image_frame = image_frame

        self.structure_label = tk.Label(self, width=20)
        self.structure_label.grid()

        bt_load = tk.Button(
            self,
            text="Load File",
            command=lambda: self.image_frame.load_image(askopenfilename()),
        )
        bt_erode = tk.Button(
            self, text="Erosion", command=lambda: self.image_frame.apply_op(erosion)
        )
        bt_dilate = tk.Button(
            self, text="Dilation", command=lambda: self.image_frame.apply_op(dilation)
        )
        bt_open = tk.Button(
            self, text="Opening", command=lambda: self.image_frame.apply_op(opening)
        )
        bt_close = tk.Button(
            self, text="Closing", command=lambda: self.image_frame.apply_op(closing)
        )
        bt_ham = tk.Button(
            self,
            text="HitAndMiss",
            command=lambda: self.image_frame.apply_op(hitandmiss),
        )

        bt_load.grid(sticky=tk.EW)
        bt_erode.grid(sticky=tk.EW)
        bt_dilate.grid(sticky=tk.EW)
        bt_open.grid(sticky=tk.EW)
        bt_close.grid(sticky=tk.EW)
        bt_ham.grid(sticky=tk.EW)
