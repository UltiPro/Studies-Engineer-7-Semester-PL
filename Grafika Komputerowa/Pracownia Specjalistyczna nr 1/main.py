from tkinter import *
import json

x1, y1 = 0, 0
x2, y2 = 0, 0
temp_shape = None
selected_item = None
shapes = []


def draw_shape():
    global x1, y1, x2, y2, temp_shape, selected_item, my_canvas, selected_shape

    params = entry.get()
    params = params.split()

    if len(params) >= 4:
        x1, y1, x2, y2 = map(float, params[:4])
        fill_color = params[4] if len(params) >= 5 else "blue"
        if selected_shape.get() == "Linia":
            item = my_canvas.create_line(x1, y1, x2, y2, fill=fill_color)
        elif selected_shape.get() == "Prostokąt":
            item = my_canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color)
        elif selected_shape.get() == "Okrąg":
            item = my_canvas.create_oval(x1, y1, x2, y2, fill=fill_color)
        shapes.append(item)


def redraw_shape():
    global x1, y1, x2, y2, temp_shape, selected_item, my_canvas, selected_shape

    params = entry2.get()
    params = params.split()

    if len(params) >= 4 and selected_item:
        x1, y1, x2, y2 = map(float, params[:4])

        entry2.delete(0, END)
        entry2.insert(0, f"{x1} {y1} {x2} {y2} ")

        if selected_item:
            my_canvas.coords(selected_item, x1, y1, x2, y2)


def on_canvas_click(event):
    global x1, y1, x2, y2, temp_shape, selected_item, my_canvas

    x1, y1 = event.x, event.y
    entry.delete(0, END)
    entry.insert(0, f"{x1} {y1} {x1} {y1}")

    if temp_shape:
        my_canvas.delete(temp_shape)

    params = entry.get().split()
    x2, y2 = int(params[2]), int(params[3])
    fill_color = params[4] if len(params) >= 5 else "blue"

    if selected_shape.get() == "Linia":
        temp_shape = my_canvas.create_line(x1, y1, x2, y2, fill=fill_color)
    elif selected_shape.get() == "Prostokąt":
        temp_shape = my_canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color)
    elif selected_shape.get() == "Okrąg":
        temp_shape = my_canvas.create_oval(x1, y1, x2, y2, fill=fill_color)


def on_drag(event):
    global x1, y1, x2, y2, temp_shape, my_canvas

    x2, y2 = event.x, event.y
    entry.delete(0, END)
    entry.insert(0, f"{x1} {y1} {x2} {y2} ")

    if temp_shape:
        my_canvas.delete(temp_shape)

    params = entry.get().split()
    fill_color = params[4] if len(params) >= 5 else "blue"

    if selected_shape.get() == "Linia":
        temp_shape = my_canvas.create_line(x1, y1, x2, y2, fill=fill_color)
    elif selected_shape.get() == "Prostokąt":
        temp_shape = my_canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color)
    elif selected_shape.get() == "Okrąg":
        temp_shape = my_canvas.create_oval(x1, y1, x2, y2, fill=fill_color)


def on_release(event):
    global temp_shape, my_canvas

    draw_shape()
    entry.delete(0, END)
    if temp_shape:
        my_canvas.delete(temp_shape)


def clear_canvas():
    global my_canvas, shapes
    my_canvas.delete("all")
    shapes = []


def move_shape(event):
    global selected_item, my_canvas, x1, y1

    new_x, new_y = event.x, event.y
    dx, dy = new_x - x1, new_y - y1
    x1, y1 = new_x, new_y

    if selected_item:
        my_canvas.move(selected_item, dx, dy)


def resize_shape(event):
    global x1, y1, x2, y2, selected_item, my_canvas

    x2, y2 = event.x, event.y
    entry.delete(0, END)
    entry.insert(0, f"{x1} {y1} {x2} {y2} ")

    if selected_item:
        my_canvas.coords(selected_item, x1, y1, x2, y2)


def select_item(event):
    global selected_item, x1, y1, x2, y2

    selected_item = event.widget.find_closest(event.x, event.y)
    selected_item = selected_item[0]

    x1, y1, x2, y2 = my_canvas.coords(selected_item)
    entry.delete(0, END)
    entry.insert(0, f"{x1} {y1} {x2} {y2} ")


def select_shape(event):
    global selected_shape
    selected_shape.set(event)
    entry.delete(0, END)


def save_canvas_json():
    global shapes
    filename = entry_save.get()
    shapes_json = []
    for item in shapes:
        item_type = my_canvas.type(item)
        item_coords = my_canvas.coords(item)
        item_color = my_canvas.itemcget(item, "fill")
        shapes_json.append(
            {"type": item_type, "coords": item_coords, "color": item_color}
        )

    with open(filename, "w") as file:
        json.dump(shapes_json, file, indent=4)
    print(f"Zapisano canvas do pliku JSON: {filename}")


def redraw_canvas():
    global my_canvas, shapes

    my_canvas.delete("all")

    for shape_data in shapes:
        item_type = shape_data["type"]
        item_coords = shape_data["coords"]
        item_color = shape_data["color"]

        if item_type == "rectangle":
            my_canvas.create_rectangle(*item_coords, fill=item_color)
        elif item_type == "oval":
            my_canvas.create_oval(*item_coords, fill=item_color)
        elif item_type == "line":
            my_canvas.create_line(*item_coords, fill=item_color)


def load_canvas_json():
    global shapes
    filename = entry_load.get()
    shapes_json = []
    try:
        with open(filename, "r") as file:
            shapes_json = json.load(file)
    except Exception as e:
        pass

    shapes = []
    redraw_canvas()
    for shape_data in shapes_json:
        item_type = shape_data.get("type", "")
        item_coords = shape_data.get("coords", [])
        item_color = shape_data.get("color", "blue")

        if item_type == "rectangle":
            item = my_canvas.create_rectangle(*item_coords, fill=item_color)
        elif item_type == "oval":
            item = my_canvas.create_oval(*item_coords, fill=item_color)
        elif item_type == "line":
            item = my_canvas.create_line(*item_coords, fill=item_color)
        shapes.append(item)


def main():
    global selected_shape, my_canvas, entry, entry2, entry_save, entry_load

    root = Tk()
    root.title("Pracownia Specjalistyczna nr 1")
    root.geometry("660x800")

    selected_shape = StringVar()
    selected_shape.set("Linia")

    my_canvas = Canvas(root, width=600, height=400, bg="white")
    my_canvas.pack(pady=30)

    shape_option_menu = OptionMenu(root, selected_shape, "Linia", "Prostokąt", "Okrąg")
    shape_option_menu.pack()

    entry_label = Label(root, text="Wprowadź parametry (x1 y1 x2 y2 [kolor]):")
    entry_label.pack()
    entry = Entry(root)
    entry.pack()

    draw_button = Button(root, text="Narysuj", command=draw_shape)
    draw_button.pack()

    entry_label2 = Label(root, text="Wprowadź zmiany (x1 y1 x2 y2):")
    entry_label2.pack()
    entry2 = Entry(root)
    entry2.pack()

    redraw_button = Button(root, text="Zmień", command=redraw_shape)
    redraw_button.pack()

    clear_button = Button(root, text="Wyczyść płótno", command=clear_canvas)
    clear_button.pack()

    my_canvas.bind("<Button-1>", on_canvas_click)
    my_canvas.bind("<B1-Motion>", on_drag)
    my_canvas.bind("<ButtonRelease-1>", on_release)

    my_canvas.bind("<Button-3>", select_item)
    my_canvas.bind("<B3-Motion>", move_shape)
    my_canvas.bind("<Shift-B3-Motion>", resize_shape)

    entry_save = Entry(root)
    entry_save.pack()
    save_button = Button(root, text="Zapisz JSON", command=save_canvas_json)
    save_button.pack()

    entry_load = Entry(root)
    entry_load.pack()
    load_button = Button(root, text="Odczytaj JSON", command=load_canvas_json)
    load_button.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
