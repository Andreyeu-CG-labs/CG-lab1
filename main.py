import sys

from PyQt5 import QtWidgets

import controller
from ui.lab1_ui import Ui_MainWindow
from utils.handlers_connection import connect_rgb, connect_lab, connect_cmyk, \
    isolate_from


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.buttonPickColor.pressed.connect(self.pick_color)
        connect_rgb(self.ui, self.rgb_changed)
        connect_lab(self.ui, self.lab_changed)
        connect_cmyk(self.ui, self.cmyk_changed)
        controller.set_rgb(self.ui, 0, 0, 0)
        controller.slider_set_bounds_and_value(self.ui, 0, 255, 0)
        self.ui.verticalSlider.valueChanged.connect(self.slider_changed)
        self.ui.button_group = controller.init_button_group(self.ui)
        self.ui.button_group.buttonClicked.connect(self.radio_button_clicked)

    def pick_color(self):
        controller.pick_color(self.ui)

    def rgb_changed(self):
        with isolate_from(self.ui,
                          cmyk_changed=self.cmyk_changed,
                          lab_changed=self.lab_changed):
            controller.rgb_changed(self.ui)

    def lab_changed(self):
        with isolate_from(self.ui,
                          cmyk_changed=self.cmyk_changed,
                          rgb_changed=self.rgb_changed):
            controller.lab_changed(self.ui)

    def cmyk_changed(self):
        with isolate_from(self.ui,
                          rgb_changed=self.rgb_changed,
                          lab_changed=self.lab_changed):
            controller.cmyk_changed(self.ui)

    def slider_changed(self):
        controller.slider_changed(self.ui)

    def radio_button_clicked(self):
        self.ui.verticalSlider.valueChanged.disconnect(self.slider_changed)
        controller.radio_button_clicked(self.ui)
        self.ui.verticalSlider.valueChanged.connect(self.slider_changed)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Main()
    MainWindow.show()
    sys.exit(app.exec_())
