import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ui_rgb_program import Ui_MainWindow
from event_handler import EventHandler

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    event_handler = EventHandler(
        ui.r_slider,
        ui.r_text,
        ui.g_slider,
        ui.g_text,
        ui.b_slider,
        ui.b_text,
        ui.c_slider,
        ui.c_text,
        ui.m_slider,
        ui.m_text,
        ui.y_slider,
        ui.y_text,
        ui.k_slider,
        ui.k_text,
        ui.color_display,
    )

    window.show()
    sys.exit(app.exec_())
