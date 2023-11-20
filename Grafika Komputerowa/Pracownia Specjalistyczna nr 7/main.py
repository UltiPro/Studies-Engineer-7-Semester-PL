import tkinter as tk

from src.canvas import CustomCanvas
from src.panel import Panel


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.canvas = CustomCanvas(self, 700, 700)
        self.canvas.grid(row=0, column=1)

        self.panel = Panel(self, self.canvas)
        self.panel.grid(row=0, column=0)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pracownia Specjalistyczna nr 7")
    app = MainApplication(root)
    app.pack(side="top", fill="both", expand=True)

    root.mainloop()
