from functools import wraps

from PyQt5 import QtWidgets

from utils.color_conversion import rgb_to_lab, rgb_to_cmyk, lab_to_rgb, \
    cmyk_to_rgb


def pick_color(ui):
    color = QtWidgets.QColorDialog.getColor()
    html = color.name().lstrip('#')
    rgb = tuple(int(html[i:i + 2], 16) for i in (0, 2, 4))
    set_rgb(ui, *rgb)


def rgb_changed(ui):
    try:
        r = float(ui.lineEdit_R.text())
        g = float(ui.lineEdit_G.text())
        b = float(ui.lineEdit_B.text())
    except ValueError:
        return

    if not check_rgb(r, g, b):
        error_message(ui)
        return
    else:
        ui.statusbar.clearMessage()

    lab = rgb_to_lab(r, g, b)
    set_lab(ui, *normalize_lab(ui, *lab))

    cmyk = rgb_to_cmyk(r, g, b)
    set_cmyk(ui, *normalize_cmyk(ui, *cmyk))

    display_color(ui, *normalize_rgb(ui, r, g, b))
    slider_update(ui)


def lab_changed(ui):
    try:
        l = float(ui.lineEdit_L.text())
        a = float(ui.lineEdit_a.text())
        b = float(ui.lineEdit_b.text())
    except ValueError:
        return

    if not check_lab(l, a, b):
        error_message(ui)
        return
    else:
        ui.statusbar.clearMessage()

    rgb = lab_to_rgb(l, a, b)
    set_rgb(ui, *normalize_rgb(ui, *rgb))

    cmyk = rgb_to_cmyk(*rgb)
    set_cmyk(ui, *normalize_cmyk(ui, *cmyk))

    display_color(ui, *normalize_rgb(ui, *rgb))
    slider_update(ui)


def cmyk_changed(ui):
    try:
        c = float(ui.lineEdit_C.text())
        m = float(ui.lineEdit_M.text())
        y = float(ui.lineEdit_Y.text())
        k = float(ui.lineEdit_K.text())
    except ValueError:
        return

    if not check_cmyk(c, m, y, k):
        error_message(ui)
        return
    else:
        ui.statusbar.clearMessage()

    rgb = cmyk_to_rgb(c, m, y, k)
    set_rgb(ui, *normalize_rgb(ui, *rgb))

    lab = rgb_to_lab(*rgb)
    set_lab(ui, *normalize_lab(ui, *lab))

    display_color(ui, *normalize_rgb(ui, *rgb))
    slider_update(ui)


def slider_changed(ui):
    if ui.radioButton_R.isChecked():
        ui.lineEdit_R.setText(str(ui.verticalSlider.sliderPosition()))
    elif ui.radioButton_G.isChecked():
        ui.lineEdit_G.setText(str(ui.verticalSlider.sliderPosition()))
    elif ui.radioButton_B.isChecked():
        ui.lineEdit_B.setText(str(ui.verticalSlider.sliderPosition()))
    elif ui.radioButton_L.isChecked():
        ui.lineEdit_L.setText(str(ui.verticalSlider.sliderPosition()))
    elif ui.radioButton_a.isChecked():
        ui.lineEdit_a.setText(str(ui.verticalSlider.sliderPosition()))
    elif ui.radioButton_b.isChecked():
        ui.lineEdit_b.setText(str(ui.verticalSlider.sliderPosition()))
    elif ui.radioButton_C.isChecked():
        ui.lineEdit_C.setText(str(ui.verticalSlider.sliderPosition()))
    elif ui.radioButton_M.isChecked():
        ui.lineEdit_M.setText(str(ui.verticalSlider.sliderPosition()))
    elif ui.radioButton_Y.isChecked():
        ui.lineEdit_Y.setText(str(ui.verticalSlider.sliderPosition()))
    elif ui.radioButton_K.isChecked():
        ui.lineEdit_K.setText(str(ui.verticalSlider.sliderPosition()))


def radio_button_clicked(ui):
    slider_update(ui)


def slider_update(ui):
    if ui.radioButton_R.isChecked():
        slider_set_bounds_and_value(ui, 0, 255, float(ui.lineEdit_R.text()))
    elif ui.radioButton_G.isChecked():
        slider_set_bounds_and_value(ui, 0, 255, float(ui.lineEdit_G.text()))
    elif ui.radioButton_B.isChecked():
        slider_set_bounds_and_value(ui, 0, 255, float(ui.lineEdit_B.text()))
    elif ui.radioButton_L.isChecked():
        slider_set_bounds_and_value(ui, 0, 100, float(ui.lineEdit_L.text()))
    elif ui.radioButton_a.isChecked():
        slider_set_bounds_and_value(ui, -275, 275, float(ui.lineEdit_a.text()))
    elif ui.radioButton_b.isChecked():
        slider_set_bounds_and_value(ui, -110, 113, float(ui.lineEdit_b.text()))
    elif ui.radioButton_C.isChecked():
        slider_set_bounds_and_value(ui, 0, 100, float(ui.lineEdit_C.text()))
    elif ui.radioButton_M.isChecked():
        slider_set_bounds_and_value(ui, 0, 100, float(ui.lineEdit_M.text()))
    elif ui.radioButton_Y.isChecked():
        slider_set_bounds_and_value(ui, 0, 100, float(ui.lineEdit_Y.text()))
    elif ui.radioButton_K.isChecked():
        slider_set_bounds_and_value(ui, 0, 100, float(ui.lineEdit_K.text()))


def check_rgb(r, g, b):
    return (0 <= r <= 255 and
            0 <= g <= 255 and
            0 <= b <= 255)


def set_rgb(ui, r, g, b):
    ui.lineEdit_R.setText(str(r))
    ui.lineEdit_R.cursorBackward(False, 10)
    ui.lineEdit_G.setText(str(g))
    ui.lineEdit_G.cursorBackward(False, 10)
    ui.lineEdit_B.setText(str(b))
    ui.lineEdit_B.cursorBackward(False, 10)


def check_lab(l, a, b):
    return (0 <= l <= 100 and
            -275 <= a <= 275 and
            -110 <= b <= 113)


def set_lab(ui, l, a, b):
    ui.lineEdit_L.setText(str(l))
    ui.lineEdit_L.cursorBackward(False, 10)
    ui.lineEdit_a.setText(str(a))
    ui.lineEdit_a.cursorBackward(False, 10)
    ui.lineEdit_b.setText(str(b))
    ui.lineEdit_b.cursorBackward(False, 10)


def check_cmyk(c, m, y, k):
    return (0 <= c <= 100 and 0 <= m <= 100 and
            0 <= y <= 100 and 0 <= k <= 100)


def set_cmyk(ui, c, m, y, k):
    ui.lineEdit_C.setText(str(c))
    ui.lineEdit_C.cursorBackward(False, 10)
    ui.lineEdit_M.setText(str(m))
    ui.lineEdit_M.cursorBackward(False, 10)
    ui.lineEdit_Y.setText(str(y))
    ui.lineEdit_Y.cursorBackward(False, 10)
    ui.lineEdit_K.setText(str(k))
    ui.lineEdit_K.cursorBackward(False, 10)


def normalize_color(ui, color, min_, max_):
    if color < min_:
        warning_message(ui)
        color = min_
    elif color > max_:
        warning_message(ui)
        color = max_
    return color


def normalize_rgb(ui, r, g, b):
    return (normalize_color(ui, r, 0, 255),
            normalize_color(ui, g, 0, 255),
            normalize_color(ui, b, 0, 255))


def normalize_lab(ui, l, a, b):
    a = 0.0 if round(a, 2) == 0 and a < 0 else a
    b = 0.0 if round(b, 2) == 0 and b < 0 else b
    return (normalize_color(ui, round(l, 2), 0, 100),
            normalize_color(ui, round(a, 2), -275, 275),
            normalize_color(ui, round(b, 2), -110, 113))


def normalize_cmyk(ui, s, m, y, k):
    return (normalize_color(ui, round(s, 3), 0, 100.0),
            normalize_color(ui, round(m, 3), 0, 100.0),
            normalize_color(ui, round(y, 3), 0, 100.0),
            normalize_color(ui, round(k, 3), 0, 100.0))


def error_message(ui):
    ui.statusbar.showMessage("Invalid numbers!")


def warning_message(ui):
    ui.statusbar.showMessage("Warning! Values are rounded.")


def display_color(ui, r, g, b):
    ui.textBrColorDispay.setStyleSheet(
        f'background-color:#{int(r):02x}' +
        f'{int(g):02x}{int(b):02x}'
    )


def slider_set_bounds_and_value(ui, min_, max_, val):
    ui.verticalSlider.setMinimum(min_)
    ui.verticalSlider.setMaximum(max_)
    ui.verticalSlider.setValue(val)


def init_button_group(ui):
    button_group = QtWidgets.QButtonGroup()
    buttons = [
        ui.radioButton_R, ui.radioButton_G, ui.radioButton_B, ui.radioButton_L,
        ui.radioButton_a, ui.radioButton_b, ui.radioButton_C, ui.radioButton_M,
        ui.radioButton_Y, ui.radioButton_K
    ]
    for b in buttons:
        button_group.addButton(b)
    return button_group
