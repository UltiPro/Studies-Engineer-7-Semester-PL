from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
import numpy as np

def open_image():
    global left_img_label, right_img_label
    global left_canvas, right_canvas
    global current_image

    file_path = filedialog.askopenfilename(filetypes=[("Image Files", ("*.jpg", "*.jpeg", "*.png", "*.gif"))])
    if file_path:
        current_image = Image.open(file_path)
        width, height = current_image.size
        new_width, new_height = calculate_new_size(width, height)
        current_image = current_image.resize((new_width, new_height))

        left_frame = tk.Frame(root)
        left_frame.grid(row=0, column=0)

        img_temp1 = ImageTk.PhotoImage(current_image)
        
        left_img_label = tk.Label(left_frame, image=img_temp1)
        left_img_label.image = img_temp1
        left_img_label.grid(row=0, column=0, padx=10)

        left_canvas = tk.Frame(root)
        left_canvas.grid(row=1, column=0)

        right_frame = tk.Frame(root)
        right_frame.grid(row=0, column=1)

        img_temp2 = ImageTk.PhotoImage(current_image)

        right_img_label = tk.Label(right_frame, image=img_temp2)
        right_img_label.image = img_temp2
        right_img_label.grid(row=0, column=0, padx=10)

        right_canvas = tk.Frame(root)
        right_canvas.grid(row=1, column=1)

def calculate_new_size(width, height):
    max_size = 500
    if width > height:
        new_width = max_size
        new_height = int(height * (max_size / width))
    else:
        new_height = max_size
        new_width = int(width * (max_size / height))
    return new_width, new_height

def manual_thresholding():
    global right_img_label
    global current_image

    if right_img_label and current_image:
        threshold_value = int(threshold_entry.get())

        img_pil = current_image.convert('L')
        image_array = np.array(img_pil)
        
        # Binaryzacja z zadanym progiem
        binary_image_array = np.where(image_array > threshold_value, 255, 0)
        binary_image = Image.fromarray(binary_image_array.astype('uint8'))
        binary_image_tk = ImageTk.PhotoImage(binary_image)
        right_img_label.configure(image=binary_image_tk)
        right_img_label.image = binary_image_tk

def percent_black_selection():
    global right_img_label
    global current_image

    if right_img_label and current_image:
        percent_value = float(percent_entry.get())  # Pobranie wartości procentowej selekcji czarnego z pola wprowadzania

        img_pil = current_image.convert('L')
        image_array = np.array(img_pil)

        # Obliczenie progu na podstawie procentu czarnego
        black_pixels = (image_array < 128).sum()
        total_pixels = image_array.size
        threshold_value = (black_pixels / total_pixels) * 255 * (percent_value / 100)

        # Binaryzacja obrazu
        binary_image_array = np.where(image_array > threshold_value, 255, 0)
        binary_image = Image.fromarray(binary_image_array.astype('uint8'))
        binary_image_tk = ImageTk.PhotoImage(binary_image)
        right_img_label.configure(image=binary_image_tk)
        right_img_label.image = binary_image_tk

def mean_iterative_selection():
    global right_img_label
    global current_image

    if right_img_label and current_image:
        img_pil = current_image.convert('L')
        image_array = np.array(img_pil)

        # Początkowy próg - średnia wartość pikseli
        initial_threshold = np.mean(image_array)

        # Iteracyjna aktualizacja progu
        previous_threshold = 0
        while abs(initial_threshold - previous_threshold) > 1:
            previous_threshold = initial_threshold
            background = image_array[image_array <= initial_threshold]
            foreground = image_array[image_array > initial_threshold]
            initial_threshold = (np.mean(background) + np.mean(foreground)) / 2

        # Binaryzacja obrazu
        binary_image_array = np.where(image_array > initial_threshold, 255, 0)
        binary_image = Image.fromarray(binary_image_array.astype('uint8'))
        binary_image_tk = ImageTk.PhotoImage(binary_image)
        right_img_label.configure(image=binary_image_tk)
        right_img_label.image = binary_image_tk

root = tk.Tk()
root.title("Pracownia Specjalistyczna nr 5")

left_img_label = None
right_img_label = None
left_canvas = None
right_canvas = None

current_image = None

threshold_label = tk.Label(root, text="Podaj wartość progu:")
threshold_label.grid(row=2, column=0)

threshold_entry = tk.Entry(root)
threshold_entry.grid(row=3, column=0)

manual_threshold_button = tk.Button(root, text="Binaryzacja ręczna", command=manual_thresholding)
manual_threshold_button.grid(row=3, column=1)

percent_label = tk.Label(root, text="Podaj procent selekcji czarnego:")
percent_label.grid(row=4, column=0)

percent_entry = tk.Entry(root)
percent_entry.grid(row=5, column=0)

percent_black_selection_button = tk.Button(root, text="Procentowa selekcja czarnego", command=percent_black_selection)
percent_black_selection_button.grid(row=5, column=1)

mean_iterative_selection_button = tk.Button(root, text="Selekcja iteratywna średniej", command=mean_iterative_selection)
mean_iterative_selection_button.grid(row=6, columnspan=2)

open_image()

root.mainloop()
