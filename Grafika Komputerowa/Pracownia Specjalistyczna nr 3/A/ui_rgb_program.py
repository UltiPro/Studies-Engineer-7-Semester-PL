from PyQt5 import QtCore, QtGui, QtWidgets
from pyslider import PySlider


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("PyQT_Grafika")
        MainWindow.resize(947, 348)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet(
            "QWidget { background-color: #F3F3F4; color: #404244; }"
        )

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout.setObjectName("verticalLayout")

        self.frame_5 = QtWidgets.QFrame(self.frame_4)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")

        self.r_slider = PySlider(self.frame_5, bg_color_end="#ff0000")
        self.r_slider.setRange(0, 255)
        self.r_slider.setGeometry(QtCore.QRect(10, 30, 160, 16))
        self.r_slider.setOrientation(QtCore.Qt.Horizontal)
        self.r_slider.setObjectName("r_slider")

        self.r_text = QtWidgets.QLineEdit(self.frame_5)
        self.r_text.setGeometry(QtCore.QRect(190, 30, 71, 23))
        self.r_text.setObjectName("r_text")
        self.r_text.setValidator(QtGui.QIntValidator(0, 255))

        self.verticalLayout.addWidget(self.frame_5)

        self.frame_6 = QtWidgets.QFrame(self.frame_4)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")

        self.g_slider = PySlider(self.frame_6, bg_color_end="#00ff00")
        self.g_slider.setRange(0, 255)
        self.g_slider.setGeometry(QtCore.QRect(10, 30, 160, 16))
        self.g_slider.setOrientation(QtCore.Qt.Horizontal)
        self.g_slider.setObjectName("g_slider")

        self.g_text = QtWidgets.QLineEdit(self.frame_6)
        self.g_text.setGeometry(QtCore.QRect(190, 30, 71, 23))
        self.g_text.setObjectName("g_text")
        self.g_text.setValidator(QtGui.QIntValidator(0, 255))

        self.verticalLayout.addWidget(self.frame_6)

        self.frame_7 = QtWidgets.QFrame(self.frame_4)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")

        self.b_slider = PySlider(self.frame_7, bg_color_end="#0000ff")
        self.b_slider.setRange(0, 255)
        self.b_slider.setGeometry(QtCore.QRect(10, 30, 160, 16))
        self.b_slider.setOrientation(QtCore.Qt.Horizontal)
        self.b_slider.setObjectName("b_slider")

        self.b_text = QtWidgets.QLineEdit(self.frame_7)
        self.b_text.setGeometry(QtCore.QRect(190, 30, 71, 23))
        self.b_text.setObjectName("b_text")
        self.b_text.setValidator(QtGui.QIntValidator(0, 255))

        self.verticalLayout.addWidget(self.frame_7)
        self.horizontalLayout_2.addWidget(self.frame_4)

        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.color_display = QtWidgets.QWidget(self.frame_2)
        self.color_display.setObjectName("color_display")
        self.color_display.setAutoFillBackground(True)

        self.verticalLayout_3.addWidget(self.color_display)
        self.horizontalLayout_2.addWidget(self.frame_2)

        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.frame_11 = QtWidgets.QFrame(self.frame_3)
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")

        self.c_slider = PySlider(self.frame_11, bg_color_end="#00ffff")
        self.c_slider.setRange(0, 100)
        self.c_slider.setGeometry(QtCore.QRect(10, 20, 160, 16))
        self.c_slider.setOrientation(QtCore.Qt.Horizontal)
        self.c_slider.setObjectName("c_slider")

        self.c_text = QtWidgets.QLineEdit(self.frame_11)
        self.c_text.setGeometry(QtCore.QRect(190, 20, 71, 23))
        self.c_text.setObjectName("c_text")
        self.c_text.setValidator(QtGui.QIntValidator(0, 255))

        self.verticalLayout_2.addWidget(self.frame_11)

        self.frame_8 = QtWidgets.QFrame(self.frame_3)
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")

        self.m_slider = PySlider(self.frame_8, bg_color_end="#ff00ff")
        self.m_slider.setRange(0, 100)
        self.m_slider.setGeometry(QtCore.QRect(10, 20, 160, 16))
        self.m_slider.setOrientation(QtCore.Qt.Horizontal)
        self.m_slider.setObjectName("m_slider")

        self.m_text = QtWidgets.QLineEdit(self.frame_8)
        self.m_text.setGeometry(QtCore.QRect(190, 20, 71, 23))
        self.m_text.setObjectName("m_text")
        self.m_text.setValidator(QtGui.QIntValidator(0, 255))

        self.verticalLayout_2.addWidget(self.frame_8)

        self.frame_9 = QtWidgets.QFrame(self.frame_3)
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")

        self.y_slider = PySlider(self.frame_9, bg_color_end="#ffff00")
        self.y_slider.setRange(0, 100)
        self.y_slider.setGeometry(QtCore.QRect(10, 20, 160, 16))
        self.y_slider.setOrientation(QtCore.Qt.Horizontal)
        self.y_slider.setObjectName("y_slider")

        self.y_text = QtWidgets.QLineEdit(self.frame_9)
        self.y_text.setGeometry(QtCore.QRect(190, 20, 71, 23))
        self.y_text.setObjectName("y_text")
        self.y_text.setValidator(QtGui.QIntValidator(0, 255))

        self.verticalLayout_2.addWidget(self.frame_9)

        self.frame_10 = QtWidgets.QFrame(self.frame_3)
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")

        self.k_slider = PySlider(self.frame_10, bg_color_end="#000000")
        self.k_slider.setRange(0, 100)
        self.k_slider.setGeometry(QtCore.QRect(10, 20, 160, 16))
        self.k_slider.setOrientation(QtCore.Qt.Horizontal)
        self.k_slider.setObjectName("k_slider")

        self.k_text = QtWidgets.QLineEdit(self.frame_10)
        self.k_text.setGeometry(QtCore.QRect(190, 20, 71, 23))
        self.k_text.setObjectName("k_text")
        self.k_text.setValidator(QtGui.QIntValidator(0, 255))

        self.verticalLayout_2.addWidget(self.frame_10)
        self.horizontalLayout_2.addWidget(self.frame_3)
        self.horizontalLayout.addWidget(self.frame)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        for text in [
            self.r_text,
            self.g_text,
            self.b_text,
            self.c_text,
            self.m_text,
            self.y_text,
            self.k_text,
        ]:
            text.setText("0")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("PyQT_Grafika", "PyQT_Grafika"))
