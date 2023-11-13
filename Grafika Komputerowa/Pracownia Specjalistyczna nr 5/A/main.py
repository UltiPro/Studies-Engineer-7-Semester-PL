from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def open_image():
    global left_img_label, middle_img_label, right_img_label
    global left_canvas, middle_canvas, right_canvas
    global current_image
    global root

    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", ("*.jpg", "*.jpeg", "*.png", "*.gif"))]
    )
    if file_path:
        current_image = Image.open(file_path)
        width, height = current_image.size
        new_width, new_height = calculate_new_size(width, height)
        current_image = current_image.resize((new_width, new_height))
        current_image = current_image.convert("L")

        left_frame = tk.Frame(root)
        left_frame.grid(row=0, column=0)

        middle_frame = tk.Frame(root)
        middle_frame.grid(row=0, column=1)

        right_frame = tk.Frame(root)
        right_frame.grid(row=0, column=2)

        img_temp1 = ImageTk.PhotoImage(current_image)

        left_img_label = tk.Label(left_frame, image=img_temp1)
        left_img_label.image = img_temp1
        left_img_label.grid(row=0, column=0, padx=10)

        img_temp2 = ImageTk.PhotoImage(current_image)

        middle_img_label = tk.Label(middle_frame, image=img_temp2)
        middle_img_label.image = img_temp2
        middle_img_label.grid(row=0, column=1, padx=10)

        img_temp3 = ImageTk.PhotoImage(current_image)

        right_img_label = tk.Label(right_frame, image=img_temp3)
        right_img_label.image = img_temp3
        right_img_label.grid(row=0, column=2, padx=10)

        left_canvas = tk.Frame(root)
        left_canvas.grid(row=1, column=0)

        middle_canvas = tk.Frame(root)
        middle_canvas.grid(row=1, column=1)

        right_canvas = tk.Frame(root)
        right_canvas.grid(row=1, column=2)

        display_histogram(current_image, left_canvas)
        display_histogram(current_image, middle_canvas)
        display_histogram(current_image, right_canvas)


def calculate_new_size(width, height):
    max_size = 250
    if width > height:
        new_width = max_size
        new_height = int(height * (max_size / width))
    else:
        new_height = max_size
        new_width = int(width * (max_size / height))
    return new_width, new_height


def display_histogram(image, canvas):
    image_array = np.array(image)
    histogram, bin_edges = np.histogram(image_array, bins=256, range=(0, 256))

    fig = plt.Figure(figsize=(7, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.bar(bin_edges[0:-1], histogram, width=1)

    ax.set_xlabel("Wartośc koloru")
    ax.set_ylabel("Liczba pikseli")

    # Zaktualizuj obecne dane histogramu w przekazanym canvasie
    for widget in canvas.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=canvas)
    canvas.get_tk_widget().grid(row=0, column=0)


def extend_histogram():
    global middle_img_label
    global current_image

    if middle_img_label and current_image:
        img_pil = current_image.convert("L")
        image_array = np.array(img_pil)
        processed_image_array = extend_histogram_helper(image_array)
        processed_image = Image.fromarray(processed_image_array.astype("uint8"))
        processed_image_tk = ImageTk.PhotoImage(processed_image)
        right_img_label.configure(image=processed_image_tk)
        right_img_label.image = processed_image_tk
        if right_canvas:
            display_histogram(processed_image, middle_canvas)


# Funkcja do rozszerzania histogramu
def extend_histogram_helper(image_array):
    Jmin = np.min(image_array)
    Jmax = np.max(image_array)
    extended_image_array = (255 / (Jmax - Jmin)) * (image_array - Jmin)
    return extended_image_array


def equalize_histogram():
    global right_img_label
    global current_image

    if right_img_label and current_image:
        img_pil = current_image.convert("L")
        image_array = np.array(img_pil)
        processed_image_array = equalize_histogram_helper(image_array)
        processed_image = Image.fromarray(processed_image_array.astype("uint8"))
        processed_image_tk = ImageTk.PhotoImage(processed_image)
        right_img_label.configure(image=processed_image_tk)
        right_img_label.image = processed_image_tk
        if right_canvas:
            display_histogram(processed_image, right_canvas)


# Funkcja do wyrównywania histogramu
def equalize_histogram_helper(image_array):
    hist, bins = np.histogram(image_array.flatten(), 256, [0, 256])
    cdf = hist.cumsum()
    cdf_normalized = (cdf - cdf.min()) * 255 / (cdf.max() - cdf.min())
    equalized_image = (
        np.interp(image_array.flatten(), bins[:-1], cdf_normalized)
        .reshape(image_array.shape)
        .astype("uint8")
    )
    return equalized_image


root = tk.Tk()
root.title("Pracownia Specjalistyczna nr 5")

left_img_label = None
middle_img_label = None
right_img_label = None
left_canvas = None
middle_canvas = None
right_canvas = None

current_image = None

open_image()

extend_histogram()

equalize_histogram()

root.mainloop()
