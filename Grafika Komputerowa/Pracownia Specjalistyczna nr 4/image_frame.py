import tkinter as tk
from PIL import Image, ImageTk
from typing import Protocol


class Filter(Protocol):
    def apply_filter(self, image: Image.Image) -> Image.Image:
        ...


class ImageFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.dims = (kwargs["width"], kwargs["height"])
        self.image: Image.Image
        self.view_image: ImageTk.PhotoImage
        self.label = tk.Label(self)
        self.label.pack()

    def load_image(self, filepath: str):
        img = Image.open(filepath)
        self.display_image(img)

    def display_image(self, image: Image.Image):
        self.image = self.__resize_image(image)
        self.view_image = ImageTk.PhotoImage(self.image)
        self.label.configure(image=self.view_image)

    def apply_filter(self, filter: Filter):
        filtered_image = filter.apply_filter(self.image)
        self.display_image(filtered_image)

    def apply_luts(self, luts: list[dict[int, int]]):
        w, h = self.image.size
        for x in range(0, w):
            for y in range(0, h):
                r, g, b = self.image.getpixel((x, y))
                if len(luts) == 1:
                    new_r = luts[0][r]
                    new_g = luts[0][g]
                    new_b = luts[0][b]
                else:
                    new_r = luts[0][r]
                    new_g = luts[1][g]
                    new_b = luts[2][b]
                self.image.putpixel((x, y), (new_r, new_g, new_b))
        self.display_image(self.image)

    def __resize_image(self, image: Image.Image) -> Image.Image:
        w, h = image.size
        fw, fh = self.dims

        if w <= fw and h <= fh:
            return image

        scale = fh / h
        new_w = round(w * scale)
        new_h = round(h * scale)

        resized_image = image.resize((new_w, new_h), Image.Resampling.LANCZOS)
        return resized_image
