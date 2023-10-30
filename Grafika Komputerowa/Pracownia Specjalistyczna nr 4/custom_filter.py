import tkinter as tk


def create_custom_filter_window(filter_frame: tk.Frame, root: tk.Frame):
    window = CustomFilterWindow(root, filter_frame)
    window.grab_set()


class CustomFilterWindow(tk.Toplevel):
    def __init__(self, parent, filter_frame, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.filter_frame = filter_frame

        self.label = tk.Label(self, text="Rozmiar filtru")
        self.dims_input = tk.Entry(self)
        self.button = tk.Button(
            self, text="Create", command=lambda: self.create_filter_input()
        )

        self.label.grid()
        self.dims_input.grid()
        self.button.grid()

    def create_filter_input(self):
        dims = self.dims_input.get()
        try:
            int_dims = int(dims)
            self.dims_input.configure(background="white")
        except:
            self.dims_input.delete(0, tk.END)
            self.dims_input.configure(background="red")
            return

        if int_dims % 2 == 0:
            self.dims_input.delete(0, tk.END)
            self.dims_input.configure(background="red")
            return

        self.weight_inputs = WeightInputFrame(
            self.parent, self.filter_frame, int_dims)
        self.weight_inputs.grab_set()
        self.destroy()


class WeightInputFrame(tk.Toplevel):
    def __init__(self, parent, filter_frame, dims: int, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.filter_frame = filter_frame
        self.dims = dims

        self.inputs = []
        for i in range(dims * dims):
            entry = tk.Entry(self)
            self.inputs.append(entry)

            col = i % dims
            row = i // dims
            entry.grid(column=col, row=row, padx=2, pady=2)

        self.submit = tk.Button(self, text="Zapisz",
                                command=self.return_weights)

        self.submit.grid(column=(dims // 2), row=dims)

    def return_weights(self):
        weights = []
        for input in self.inputs:
            try:
                val = int(input.get())
                weights.append(val)
                input.configure(background="white")
            except:
                input.delete(0, tk.END)
                input.configure(background="red")

        if len(weights) != len(self.inputs):
            return

        self.filter_frame.send_custom_filter(self.dims, weights)
        self.destroy()
