import tkinter as tk
from typing import Callable

from PIL import Image, ImageTk


def binary_threshold_lut(threshold: int) -> dict:
    lut = dict()
    for i in range(256):
        lut[i] = 0 if i < threshold else 255

    return lut


class ImageFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.dims = (kwargs["width"], kwargs["height"])

        self.image: Image.Image
        self.view_image: ImageTk.PhotoImage

        self.label = tk.Label(self)
        self.label.pack()

        self.load_image("lenna.png")

    def load_image(self, filepath: str):
        img = Image.open(filepath)
        self.display_image(img)

    def display_image(self, image: Image.Image):
        image = self.__resize_image(image)
        image = self.__grayscale(image)
        self.image = self.__apply_lut(image, binary_threshold_lut(128))
        image = self.image.copy()
        while image.size[0] < 400:
            w, h = image.size
            image = image.resize((w * 2, h * 2), resample=Image.Resampling.NEAREST)
        self.view_image = ImageTk.PhotoImage(image)
        self.label.configure(image=self.view_image)

    def apply_op(self, operation: Callable):
        morphed_image = operation(self.image)
        self.display_image(morphed_image)

    def iter_apply_op(self, operation: Callable):
        for morphed_image in operation(self.image):
            self.display_image(morphed_image)

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

    def __grayscale(self, image: Image.Image) -> Image.Image:
        w, h = image.size
        for x in range(w):
            for y in range(h):
                new_pixel_val = sum(image.getpixel((x, y))) // 3
                image.putpixel((x, y), (new_pixel_val,) * 3)

        return image

    def __apply_lut(self, image: Image.Image, lut: dict) -> Image.Image:
        w, h = image.size
        for x in range(w):
            for y in range(h):
                original_pixel_val = sum(image.getpixel((x, y))) // 3
                new_pixel_val = lut[original_pixel_val]
                image.putpixel((x, y), (new_pixel_val,) * 3)

        return image
