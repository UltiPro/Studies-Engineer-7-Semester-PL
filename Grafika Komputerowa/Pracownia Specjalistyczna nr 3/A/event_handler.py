def rgb_to_cmyk(r, g, b):
    r = r/255
    g = g/255
    b = b/255

    k = 1 - max(r, g, b)
    if k == 1:
        return 0, 0, 0, int(k*100)

    c = (1-r-k)/(1-k)
    m = (1-g-k)/(1-k)
    y = (1-b-k)/(1-k)

    return int(c*100), int(m*100), int(y*100), int(k*100)


def cmyk_to_rgb(c, m, y, k):
    c = c/100
    m = m/100
    y = y/100
    k = k/100

    r = 1 - min(1, c*(1-k) + k)
    g = 1 - min(1, m*(1-k) + k)
    b = 1 - min(1, y*(1-k) + k)

    return int(r*255), int(g*255), int(b*255)


class EventHandler():
    def __init__(
        self,
        r_slider, r_text,
        g_slider, g_text,
        b_slider, b_text,
        c_slider, c_text,
        m_slider, m_text,
        y_slider, y_text,
        k_slider, k_text,
        color_display
    ):
        self.r_slider = r_slider
        self.r_text = r_text
        self.g_slider = g_slider
        self.g_text = g_text
        self.b_slider = b_slider
        self.b_text = b_text
        self.c_slider = c_slider
        self.c_text = c_text
        self.m_slider = m_slider
        self.m_text = m_text
        self.y_slider = y_slider
        self.y_text = y_text
        self.k_slider = k_slider
        self.k_text = k_text
        self.color_display = color_display

        self.r_slider.sliderMoved.connect(lambda: self.slider_changed('rgb'))
        self.g_slider.sliderMoved.connect(lambda: self.slider_changed('rgb'))
        self.b_slider.sliderMoved.connect(lambda: self.slider_changed('rgb'))

        self.r_text.textEdited.connect(lambda: self.text_changed('rgb'))
        self.g_text.textEdited.connect(lambda: self.text_changed('rgb'))
        self.b_text.textEdited.connect(lambda: self.text_changed('rgb'))

        self.c_slider.sliderMoved.connect(lambda: self.slider_changed('cmyk'))
        self.m_slider.sliderMoved.connect(lambda: self.slider_changed('cmyk'))
        self.y_slider.sliderMoved.connect(lambda: self.slider_changed('cmyk'))
        self.k_slider.sliderMoved.connect(lambda: self.slider_changed('cmyk'))

        self.c_text.textEdited.connect(lambda: self.text_changed('cmyk'))
        self.m_text.textEdited.connect(lambda: self.text_changed('cmyk'))
        self.y_text.textEdited.connect(lambda: self.text_changed('cmyk'))
        self.k_text.textEdited.connect(lambda: self.text_changed('cmyk'))

        self.color_display.setStyleSheet('background-color: #000000')

        self.r = 0
        self.g = 0
        self.b = 0

        self.c = 0
        self.m = 0
        self.y = 0
        self.k = 0

    def set_color(self, r, g, b):
        self.color_display.setStyleSheet(f'background-color: rgb({r},{g},{b})')

    def slider_changed(self, color_type: str):
        if color_type == 'rgb':
            r, g, b = self.r_slider.value(), self.g_slider.value(), self.b_slider.value()
            self.set_rgb_text(r, g, b)
            c, m, y, k = rgb_to_cmyk(r, g, b)
            self.set_cmyk(c, m, y, k)
            self.set_color(r, g, b)
        else:
            c, m, y, k = self.c_slider.value(), self.m_slider.value(
            ), self.y_slider.value(), self.k_slider.value()
            self.set_cmyk_text(c, m, y, k)
            r, g, b = cmyk_to_rgb(c, m, y, k)
            self.set_rgb(r, g, b)
            self.set_color(r, g, b)

    def text_changed(self, color_type: str):
        if color_type == 'rgb':
            sr, sg, sb = self.r_text.text(), self.g_text.text(), self.b_text.text()
            r = int(sr) if sr else 0
            g = int(sg) if sg else 0
            b = int(sb) if sb else 0
            self.set_rgb_sliders(r, g, b)
            c, m, y, k = rgb_to_cmyk(r, g, b)
            self.set_cmyk(c, m, y, k)
            self.set_color(r, g, b)
        else:
            sc, sm, sy, sk = self.c_text.text(), self.m_text.text(
            ), self.y_text.text(), self.k_text.text()
            c = int(sc) if sc else 0
            m = int(sm) if sm else 0
            y = int(sy) if sy else 0
            k = int(sk) if sk else 0
            self.set_cmyk_sliders(c, m, y, k)
            r, g, b = cmyk_to_rgb(c, m, y, k)
            self.set_rgb(r, g, b)
            self.set_color(r, g, b)

    def set_rgb(self, r, g, b):
        self.set_rgb_sliders(r, g, b)
        self.set_rgb_text(r, g, b)

    def set_cmyk(self, c, m, y, k):
        self.set_cmyk_sliders(c, m, y, k)
        self.set_cmyk_text(c, m, y, k)

    def set_rgb_sliders(self, r, g, b):
        self.r, self.g, self.b = r, g, b
        self.r_slider.setValue(r)
        self.g_slider.setValue(g)
        self.b_slider.setValue(b)

    def set_rgb_text(self, r, g, b):
        self.r, self.g, self.b = r, g, b
        self.r_text.setText(str(r))
        self.g_text.setText(str(g))
        self.b_text.setText(str(b))

    def set_cmyk_sliders(self, c, m, y, k):
        self.c, self.m, self.y, self.k = c, m, y, k
        self.c_slider.setValue(c)
        self.m_slider.setValue(m)
        self.y_slider.setValue(y)
        self.k_slider.setValue(k)

    def set_cmyk_text(self, c, m, y, k):
        self.c, self.m, self.y, self.k = c, m, y, k
        self.c_text.setText(str(c))
        self.m_text.setText(str(m))
        self.y_text.setText(str(y))
        self.k_text.setText(str(k))
