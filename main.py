#   Copyright 2023 Suchinton Chakravarty
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import sys
import os

from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QPushButton

from functools import partial

from Widgets.settings import *

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = uic.loadUiType(os.path.join(current_dir, "Main_Window.ui"))

class MainWindow(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.mouse_press_position = None
        self.resizing = False

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

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mouse_press_position = event.globalPos()
            self.resizing = True

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.resizing = False
            self.setCursor(QtCore.Qt.ArrowCursor)

    def mouseMoveEvent(self, event):
        if self.resizing:
            delta = event.globalPos() - self.mouse_press_position
            self.resize(self.width() + delta.x(), self.height() + delta.y())
            self.mouse_press_position = event.globalPos()
            self.setCursor(QtCore.Qt.SizeAllCursor)

    def mouseDoubleClickEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.toggleMaximized()

    def enterEvent(self, event):
        if self.resizing:
            self.setCursor(QtCore.Qt.SizeAllCursor)

    def leaveEvent(self, event):
        if self.resizing:
            self.setCursor(QtCore.Qt.ArrowCursor)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
