import tkinter as tk

from image_frame import ImageFrame
from sidebar import Sidebar
from sidebar_point import SidebarPoint


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.image_frame = ImageFrame(self, width=700, height=700)
        self.filter_side_bar = Sidebar(self, self.image_frame)
        self.point_side_bar = SidebarPoint(self, self.image_frame)
        self.point_side_bar.grid(column=0, row=0)
        self.image_frame.grid(column=1, row=0)
        self.filter_side_bar.grid(column=2, row=0)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Grafika_PS5")
    app = MainApplication(root)
    app.pack(side="top", fill="both", expand=True)
    root.mainloop()
