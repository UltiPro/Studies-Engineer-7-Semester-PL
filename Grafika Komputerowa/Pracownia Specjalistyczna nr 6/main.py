import tkinter as tk
from canvas import CustomCanvas


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.canvas = CustomCanvas(self, 700, 700)
        self.canvas.grid()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pracownia Specjalistyczna nr 6")
    app = MainApplication(root)
    app.pack(side="top", fill="both", expand=True)

    print("-------------------------")
    print("-------- KEYMAPS --------")
    print("-------------------------")
    print("i | insert mode")
    print("o | edit mode")
    print("-------")
    print("h | toggle control lines")
    print("q | reduce step count")
    print("e | increase step count")
    print("-------")
    print("d | clear canvas")
    print("-------------------------")

    root.mainloop()
