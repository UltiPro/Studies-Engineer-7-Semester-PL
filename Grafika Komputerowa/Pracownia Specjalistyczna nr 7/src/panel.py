import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

from src import serializer
from src.canvas import CustomCanvas
from src.states import (
    CreateState,
    FocalState,
    RotateState,
    ScaleState,
    SelectState,
    State,
    TranslateState,
)


class Panel(tk.Frame):
    def __init__(self, parent, canvas: CustomCanvas, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.canvas = canvas

        self.title_label = tk.Label(self, text="Panel", width=20)
        self.title_label.grid(columnspan=2)

        self.bt_create = tk.Button(
            self,
            text="Create",
            command=lambda: self.set_state(CreateState(self.canvas, self.set_state)),
        )
        self.bt_focal = tk.Button(
            self,
            text="Move Focal Point",
            command=lambda: self.set_state(FocalState(self.canvas, self.set_state)),
        )
        self.in_tx = tk.Entry(self, width=5)
        self.in_ty = tk.Entry(self, width=5)
        self.bt_translate = tk.Button(
            self,
            text="Translate",
            command=lambda: self.set_state(
                TranslateState(self.canvas, self.set_state, self.in_tx, self.in_ty)
            ),
        )
        self.in_rd = tk.Entry(self, width=5)
        self.bt_rotate = tk.Button(
            self,
            text="Rotate",
            command=lambda: self.set_state(
                RotateState(self.canvas, self.set_state, self.in_rd)
            ),
        )
        self.in_sx = tk.Entry(self, width=5)
        self.in_sy = tk.Entry(self, width=5)
        self.bt_scale = tk.Button(
            self,
            text="Scale",
            command=lambda: self.set_state(
                ScaleState(self.canvas, self.set_state, self.in_sx, self.in_sy)
            ),
        )
        self.bt_confirm = tk.Button(self, text="Confirm", command=self.__confirm)
        self.bt_save = tk.Button(self, text="Save", command=self.__save)
        self.bt_load = tk.Button(self, text="Load", command=self.__load)

        self.bt_create.grid(row=0, sticky=tk.EW, columnspan=2)
        self.bt_focal.grid(row=1, sticky=tk.EW, columnspan=2)
        self.bt_translate.grid(row=2, sticky=tk.EW, columnspan=2)
        self.in_tx.grid(row=3, column=0, sticky=tk.EW)
        self.in_ty.grid(row=3, column=1, sticky=tk.EW)
        self.bt_rotate.grid(row=4, sticky=tk.EW, columnspan=2)
        self.in_rd.grid(row=5, sticky=tk.EW, columnspan=2)
        self.bt_scale.grid(row=6, sticky=tk.EW, columnspan=2)
        self.in_sx.grid(row=7, column=0, sticky=tk.EW)
        self.in_sy.grid(row=7, column=1, sticky=tk.EW)
        self.bt_confirm.grid(sticky=tk.EW, columnspan=2, pady=20)
        self.bt_save.grid(sticky=tk.EW, columnspan=2)
        self.bt_load.grid(sticky=tk.EW, columnspan=2)

        self.state: State = SelectState(self.canvas, self.set_state)
        self.state.bind()

    def set_state(self, state: State):
        self.state.unbind()
        self.state = state
        self.state.bind()

    def __confirm(self):
        self.state.confirm()
        self.set_state(SelectState(self.canvas, self.set_state))

    def __save(self):
        filename = asksaveasfilename()
        if filename:
            serializer.write(filename, self.canvas.shapes)

    def __load(self):
        filename = askopenfilename()
        if filename:
            self.canvas.selected = None
            self.canvas.shapes = serializer.read(filename)
            self.canvas.draw()
