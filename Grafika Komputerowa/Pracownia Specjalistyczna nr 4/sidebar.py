import tkinter as tk
from tkinter import filedialog as fd
from pathlib import Path

from filters import (
    AverageFilter,
    CustomFilter,
    GaussianFilter,
    HighPassFilter,
    MedianFilter,
    SobelFilter,
)
from custom_filter import create_custom_filter_window


class FileLoaderFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.filename: str

        self.input_label = tk.Label(self, text="Current File: ", width=30)
        self.input = tk.Button(
            self, text="Open", command=lambda: self.__load_file(fd.askopenfilename())
        )

        self.input_label.pack()
        self.input.pack()

    def __load_file(self, filename: str) -> None:
        file_path = Path(filename)
        self.parent.load_file(file_path)
        self.input_label.configure(text=f"Current File: {file_path.name}")


class FilterFrame(tk.Frame):
    def __init__(self, parent, image_frame, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.image_frame = image_frame

        self.avg_filter_bt = tk.Button(
            self,
            text="Filtr Uśredniający",
            command=lambda: self.__send_filter(AverageFilter()),
        )
        self.med_filter_bt = tk.Button(
            self,
            text="Filtr Medianowy",
            command=lambda: self.__send_filter(MedianFilter()),
        )
        self.sobel_filter_bt = tk.Button(
            self,
            text="Filtr Sobela",
            command=lambda: self.__send_filter(SobelFilter()),
        )
        self.hp_filter_bt = tk.Button(
            self,
            text="Filtr Górnoprzepustowy",
            command=lambda: self.__send_filter(HighPassFilter()),
        )
        self.gauss_filter_bt = tk.Button(
            self,
            text="Filtr Gaussa",
            command=lambda: self.__send_filter(GaussianFilter()),
        )
        self.custom_filter_bt = tk.Button(
            self,
            text="Stwórz własny filtr",
            command=lambda: create_custom_filter_window(
                self, self.parent.parent.parent),
        )

        self.avg_filter_bt.pack()
        self.med_filter_bt.pack()
        self.sobel_filter_bt.pack()
        self.hp_filter_bt.pack()
        self.gauss_filter_bt.pack()
        self.custom_filter_bt.pack()

    def send_custom_filter(self, dims: int, weights: list[int]):
        self.__send_filter(CustomFilter(dims, weights))

    def __send_filter(self, filter):
        self.image_frame.apply_filter(filter)


class Sidebar(tk.Frame):
    def __init__(self, parent, image_frame, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.image_frame = image_frame

        self.file_loader = FileLoaderFrame(self)
        self.file_loader.pack()

        self.filter_frame = FilterFrame(self, self.image_frame)

    def load_file(self, file_path: str):
        self.image_frame.load_image(file_path)
        if not self.filter_frame.winfo_ismapped():
            self.filter_frame.pack()
            self.parent.point_side_bar.show_point_frame()
