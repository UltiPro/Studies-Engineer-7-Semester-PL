import tkinter as tk
from tkinter import filedialog as fd
import ppm_reader
from ppm_reader import Image
import timeit
from PIL import Image as im
from PIL import ImageTk as imtk
from itertools import chain
import os
from PIL import ImageGrab
from dataclasses import dataclass

WIDTH, HEIGHT = 1080, 720


@dataclass
class Vec2():
    x: int
    y: int


pixels: list
img: Image | None
dims = (0, 0)
image: imtk.PhotoImage
imagesprite: int
disp: im.Image
scale = 1

last_mouse_pos: Vec2 = Vec2(0, 0)


def mouse_pressed(event: tk.Event):
    if not image:
        return

    try:
        get_color(event)
    except:
        pass

    global last_mouse_pos
    last_mouse_pos = Vec2(event.x, event.y)


def get_color(event):
    x, y = event.x_root, event.y_root

    screenshot = ImageGrab.grab(bbox=(x - 5, y - 5, x + 5, y + 5))
    pixel = screenshot.getpixel((5, 5))

    color_label.config(text=f'RGB: {pixel}')


def mouse_right_pressed(event: tk.Event):
    pass


def mouse_dragged(event: tk.Event):
    if not image:
        return

    global last_mouse_pos

    dx = event.x - last_mouse_pos.x
    dy = event.y - last_mouse_pos.y
    last_mouse_pos.x, last_mouse_pos.y = event.x, event.y
    if imagesprite:
        coords = canvas.coords(imagesprite)
        canvas.coords(imagesprite, coords[0] + dx, coords[1] + dy)


def mouse_scroll(event: tk.Event):
    if not image:
        return

    global scale
    if event.delta < 0:
        if scale <= 1:
            scale = scale / 2
        else:
            scale = scale - 1
    elif event.delta > 0:
        if scale < 1:
            scale = scale * 2
        else:
            scale = scale + 1

    redraw_img()


def mouse_released(event: tk.Event):
    pass


def scroll_pressed(event: tk.Event):
    if not image:
        return

    global imagesprite
    canvas.coords(imagesprite,
                  canvas.winfo_width()//2, canvas.winfo_height()//2)


def redraw_img():
    global disp, image, imagesprite, scale

    if image:
        disp2 = disp.resize(
            (round(dims[0]*scale), round(dims[1]*scale)), resample=im.Resampling.NEAREST)
        image = imtk.PhotoImage(disp2)

        canvas.itemconfigure(imagesprite, image=image)


def linear_scale_color(scale_factor):
    global imagesprite
    global disp

    if disp.mode != "RGB":
        disp = disp.convert("RGB")

    width, height = disp.size
    pixels = list(disp.getdata())

    scaled_pixels = []
    for pixel in pixels:
        scaled_pixel = tuple(int(value * scale_factor) for value in pixel)
        scaled_pixels.append(scaled_pixel)

    scaled_image = im.new("RGB", (width, height))
    scaled_image.putdata(scaled_pixels)

    save_path = os.path.join('', "program_data") + ".jpeg"

    if scaled_image:
        rgb_disp = scaled_image.convert('RGB')
        rgb_disp.save(save_path, "JPEG", quality=100)

    load_jpeg_file("./program_data.jpeg")


def load_ppm_file(filepath: str):
    global img
    global image
    global pixels
    global imagesprite
    global disp
    global dims
    start_time = timeit.default_timer()
    img = ppm_reader.read_file(filepath)
    print(f'Time to load file: {timeit.default_timer() - start_time}')
    if not img:
        return

    dims = (img.width, img.height)
    buf: bytes
    if img.type == 'bin':
        buf = img.pixel_data
    else:
        buf = bytes(chain.from_iterable(img.pixel_data))

    disp = im.frombuffer(img.mode, (img.width, img.height), buf)
    image = imtk.PhotoImage(disp)

    imagesprite = canvas.create_image(canvas.winfo_width()//2,
                                      canvas.winfo_height()//2, image=image)


def load_jpeg_file(filepath: str):
    global disp, imagesprite, image, dims

    disp = im.open(filepath)
    dims = (disp.width, disp.height)
    image = imtk.PhotoImage(disp)

    imagesprite = canvas.create_image(canvas.winfo_width()//2,
                                      canvas.winfo_height()//2, image=image)


def load_file(filepath: str):
    if filepath[-4:] == '.ppm':
        load_ppm_file(filepath)
    elif filepath[-4:] == '.jpg' or filepath[-5:] == '.jpeg':
        load_jpeg_file(filepath)
    else:
        print('Invalid filetype')


def save_jpeg(filepath: str, compression):
    global disp
    try:
        compression = int(compression)
    except:
        print('compression must be int value')
        return

    if compression < 1 or compression > 100:
        print('compression must be 1-100')
        return

    save_path = os.path.join('', filepath) + ".jpeg"

    if disp:
        rgb_disp = disp.convert('RGB')
        rgb_disp.save(save_path, "JPEG", quality=compression)


top = tk.Tk()
config_pane = tk.Frame(top, height=720, width=220)

canvas = tk.Canvas(top, bg="white", height=720, width=860)
canvas.bind("<Button-1>", mouse_pressed)
canvas.bind("<Button-2>", scroll_pressed)
canvas.bind("<Button-3>", mouse_right_pressed)  # nth
canvas.bind("<ButtonRelease-1>", mouse_released)  # nth
canvas.bind("<B1-Motion>", mouse_dragged)
canvas.bind("<MouseWheel>", mouse_scroll)
canvas.bind("<MouseWheel>", mouse_scroll)


config_pane.pack(side="left")
canvas.pack(side='right')
canvas.update()

open_label = tk.Label(config_pane, text='Open file')
open_label.pack()
open_bt = tk.Button(config_pane, text='open',
                    command=lambda: load_file(fd.askopenfilename()))
open_bt.pack()
color_label = tk.Label(config_pane, text="", font=("Helvetica", 12))
color_label.pack()
sep = tk.Label(config_pane, text='-')
sep.pack(pady=20)
scale_slider = tk.Scale(config_pane, from_=0.1, to=2.0,
                        resolution=0.01, orient="horizontal", label="Scale")
scale_slider.pack()
scale_slider.set(1.0)
scale_button = tk.Button(config_pane, text="Save Scale",
                         command=lambda: linear_scale_color(scale_slider.get()))
scale_button.pack()
save_label = tk.Label(config_pane, text='Save image as jpeg with name:')
save_label.pack()
save_fp = tk.Entry(config_pane)
save_fp.pack()
comp_label = tk.Label(config_pane, text='with quality (1-100):')
comp_label.pack()
save_cmp = tk.Entry(config_pane)
save_cmp.pack()
save_bt = tk.Button(config_pane, text='save',
                    command=lambda: save_jpeg(save_fp.get(), save_cmp.get()))
save_bt.pack()


top.mainloop()
