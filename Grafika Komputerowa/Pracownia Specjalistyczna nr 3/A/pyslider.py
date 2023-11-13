from PyQt5.QtWidgets import QSlider


style = """
QSlider {{ margin: {_margin}px; }}
QSlider::groove:horizontal {{
    border-radius: {_bg_radius}px;
    height: {_bg_size}px;
    margin: 0px;
    background-color: qlineargradient(x1:0, x2:1, stop:0 {_bg_color_start}, stop:1 {_bg_color_end});
}}
QSlider::groover:horizontal:hover {{ background-color: {_bg_color_hover} }}
QSlider::handle:horizontal {{
    border: none;
    height: {_handle_size}px;
    width: {_handle_size}px;
    margin: {_handle_margin}px;
    border-radius: {_handle_radius}px;
    background-color: {_handle_color};
}}
QSlider::handle:horizontal:hover {{ background-color: {_handle_color_hover}; }}
QSlider::handle:horizontal:pressed {{ background-color: {_handle_color_pressed}; }}

QSlider::groove:vertical {{
    border-radius: {_bg_radius}px;
    width: {_bg_size}px;
    margin: 0px;
    background-color: qlineargradient(y1:0, y2:1, stop:0 {_bg_color_start}, stop:1 {_bg_color_end});
}}
QSlider::groover:vertical:hover {{ background-color: {_bg_color_hover} }}
QSlider::handle:vertical {{
    border: none;
    height: {_handle_size}px;
    width: {_handle_size}px;
    margin: {_handle_margin}px;
    border-radius: {_handle_radius}px;
    background-color: {_handle_color};
}}
QSlider::handle:vertical:hover {{ background-color: {_handle_color_hover}; }}
QSlider::handle:vertical:pressed {{ background-color: {_handle_color_pressed}; }}

"""


class PySlider(QSlider):
    def __init__(
        self,
        parent=None,
        margin=0,
        bg_size=7,
        bg_radius=0,
        bg_color_start="#ffffff",
        bg_color_end="#00ffff",
        bg_color_hover="#1e2229",
        handle_margin=0,
        handle_size=10,
        handle_radius=0,
        handle_color="#000000",
        handle_color_hover="#616161",
        handle_color_pressed="#a1a1a1",
    ):
        super(PySlider, self).__init__(parent=parent)

        adjust_style = style.format(
            _margin=margin,
            _bg_size=bg_size,
            _bg_radius=bg_radius,
            _bg_color_start=bg_color_start,
            _bg_color_end=bg_color_end,
            _bg_color_hover=bg_color_hover,
            _handle_margin=handle_margin,
            _handle_size=handle_size,
            _handle_radius=handle_radius,
            _handle_color=handle_color,
            _handle_color_hover=handle_color_hover,
            _handle_color_pressed=handle_color_pressed,
        )

        self.setStyleSheet(adjust_style)
