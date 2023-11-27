import tkinter as tk

from image_frame import ImageFrame
from panel import Panel


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.image_frame = ImageFrame(self, width=700, height=700)
        self.panel = Panel(self, self.image_frame)
        self.panel.grid(row=0, column=0)
        self.image_frame.grid(row=0, column=1)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pracownia Specjalistyczna nr 8")
    app = MainApplication(root)
    app.pack(side="top", fill="both", expand=True)

    root.mainloop()
