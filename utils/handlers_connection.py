from contextlib import contextmanager


@contextmanager
def isolate_from(ui, rgb_changed=None, lab_changed=None, cmyk_changed=None):
    try:
        if rgb_changed is not None:
            disconnect_rgb(ui, rgb_changed)
        if lab_changed is not None:
            disconnect_lab(ui, lab_changed)
        if cmyk_changed is not None:
            disconnect_cmyk(ui, cmyk_changed)
        yield ui
    finally:
        if rgb_changed is not None:
            connect_rgb(ui, rgb_changed)
        if lab_changed is not None:
            connect_lab(ui, lab_changed)
        if cmyk_changed is not None:
            connect_cmyk(ui, cmyk_changed)


def disconnect_rgb(ui, func):
    ui.lineEdit_R.textChanged.disconnect(func)
    ui.lineEdit_G.textChanged.disconnect(func)
    ui.lineEdit_B.textChanged.disconnect(func)


def disconnect_lab(ui, func):
    ui.lineEdit_L.textChanged.disconnect(func)
    ui.lineEdit_a.textChanged.disconnect(func)
    ui.lineEdit_b.textChanged.disconnect(func)


def disconnect_cmyk(ui, func):
    ui.lineEdit_C.textChanged.disconnect(func)
    ui.lineEdit_M.textChanged.disconnect(func)
    ui.lineEdit_Y.textChanged.disconnect(func)
    ui.lineEdit_K.textChanged.disconnect(func)


def connect_rgb(ui, func):
    ui.lineEdit_R.textChanged.connect(func)
    ui.lineEdit_G.textChanged.connect(func)
    ui.lineEdit_B.textChanged.connect(func)


def connect_lab(ui, func):
    ui.lineEdit_L.textChanged.connect(func)
    ui.lineEdit_a.textChanged.connect(func)
    ui.lineEdit_b.textChanged.connect(func)


def connect_cmyk(ui, func):
    ui.lineEdit_C.textChanged.connect(func)
    ui.lineEdit_M.textChanged.connect(func)
    ui.lineEdit_Y.textChanged.connect(func)
    ui.lineEdit_K.textChanged.connect(func)
