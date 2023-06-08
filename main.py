import sys
import os

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

from ui_Main_Window import *

from functools import partial

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = uic.loadUiType(os.path.join(current_dir, "Main_Window.ui"))

class MainWindow(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)

        buttons = (self.icButton, self.hvacButton, self.newButton)

        for i, button in enumerate(buttons):
            button.clicked.connect(partial(self.stackedWidget.setCurrentIndex, i))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
