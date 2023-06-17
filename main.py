import sys
import os

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QPushButton

from functools import partial

from Widgets.settings import *

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = uic.loadUiType(os.path.join(current_dir, "Main_Window.ui"))

class MainWindow(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)

        # Window Controls
        closeButton = self.findChild(QPushButton, 'closeBtn')
        minimizeButton = self.findChild(QPushButton, 'minimizeBtn')
        resizeButton = self.findChild(QPushButton, 'resizeBtn')

        closeButton.clicked.connect(self.close)
        minimizeButton.clicked.connect(self.showMinimized)
        resizeButton.clicked.connect(self.toggleMaximized)

        # Widget Navigation
        buttons = (self.icButton, self.hvacButton, self.newButton)

        for i, button in enumerate(buttons):
            button.clicked.connect(partial(self.stackedWidget.setCurrentIndex, i))

        settings = self.findChild(QPushButton, 'settingsBtn')
        settings.clicked.connect(partial(self.stackedWidget.setCurrentIndex, 3))

        self.stackedWidget.setCurrentIndex(0)

    def toggleMaximized(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
