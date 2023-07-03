"""
   Copyright 2023 Suchinton Chakravarty

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import sys
import os

from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget
from functools import partial

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = uic.loadUiType(os.path.join(current_dir, "Main_Window.ui"))

from extras.UI_Handeler import *

class MainWindow(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # # load the stylesheet
        # theme = open(os.path.join(current_dir, "ui/styles/Tron/MainWindow.qss"), 'r')
        # self.setStyleSheet(theme.read())

        self.headerContainer = self.findChild(QWidget, 'headerContainer')
        self.headerContainer.mouseDoubleClickEvent = lambda event: UI_Handeler.toggleMaximized(self)
        self.headerContainer.mouseMoveEvent = lambda event: UI_Handeler.moveWindow(self, event)
        self.headerContainer.mousePressEvent = lambda event: UI_Handeler.mousePressEvent(self, event)
        self.headerContainer.mouseReleaseEvent = lambda event: UI_Handeler.mouseReleaseEvent(self, event)



        self.leftMenuSubContainer = self.findChild(QWidget, 'leftMenuSubContainer')
        self.menuButton = self.findChild(QPushButton, 'menuButton')
        self.menuButton.clicked.connect(lambda: UI_Handeler.toggleNavigationBar(self, 250, True))

        self.notificationContent = self.findChild(QWidget, 'notificationContent')

        # Window Controls
        closeButton = self.findChild(QPushButton, 'closeBtn')
        minimizeButton = self.findChild(QPushButton, 'minimizeBtn')
        maximizeButton = self.findChild(QPushButton, 'maximizeBtn')

        closeButton.clicked.connect(self.close)
        minimizeButton.clicked.connect(self.showMinimized)
        maximizeButton.clicked.connect(lambda: UI_Handeler.toggleMaximized(self))

        # Widget Navigation
        buttons = (self.icButton, 
                   self.hvacButton, 
                   self.steeringCtrlButton,
                   self.navButton,
                   self.newButton, 
                   self.settingsBtn)
        NavigationButtons = QtWidgets.QButtonGroup(self)
        NavigationButtons.setExclusive(True)

        for i, button in enumerate(buttons):
            button.setCheckable(True)
            NavigationButtons.addButton(button)
            button.clicked.connect(partial(UI_Handeler.animateSwitch, self, i))

        self.stackedWidget.currentChanged.connect(self.handleChangedPage)

        self.stackedWidget.setCurrentIndex(0)
        self.icButton.setChecked(True)

    def handleChangedPage(self, index):
        Page = self.stackedWidget.widget(index)
        if Page is not self.stackedWidget.widget(3):
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
