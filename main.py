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
from PyQt5.QtGui import QFontDatabase

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = uic.loadUiType(os.path.join(current_dir, "Main_Window.ui"))

from extras.UI_Handeler import *

class MainWindow(Base, Form):

    # signal to stop the thread
    stop_thread_signal = QtCore.pyqtSignal()
    start_thread_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        fonts = [font for font in os.listdir(os.path.join(current_dir, "assets/fonts")) if font.endswith(".ttf")]
        fonts = [os.path.join(current_dir, "assets/fonts/", font) for font in fonts]

        for font in fonts:
            QFontDatabase.addApplicationFont(font)
        # # load the stylesheet
        # theme = open(os.path.join(current_dir, "ui/styles/Tron/MainWindow.qss"), 'r')
        # self.setStyleSheet(theme.read())

        self.setStyle(QtWidgets.QStyleFactory.create('Fusion'))

        self.headerContainer = self.findChild(QWidget, 'headerContainer')
        self.headerContainer.DoubleClickMaximize = lambda: UI_Handeler.toggleMaximized(self)
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

        #closeButton.clicked.connect(self.close)
        # make the close button also end all threads
        closeButton.clicked.connect(lambda: [self.close(), self.stop_thread_signal.emit()])
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
        
        self.stop_thread_signal.connect(self.stackedWidget.widget(0).kuksa_feeder.stop)

        self.stackedWidget.setCurrentIndex(0)
        self.icButton.setChecked(True)

        self.current_page = self.stackedWidget.currentIndex()

    def handleChangedPage(self, index):
        # stop the previous thread and start the new one
        try:
            self.stop_thread_signal.connect(self.stackedWidget.widget(self.current_page).kuksa_feeder.stop)
            self.stop_thread_signal.emit()
        except:
            pass

        self.current_page = self.stackedWidget.currentIndex()

        try:
            self.start_thread_signal.connect(self.stackedWidget.widget(self.current_page).kuksa_feeder.start)
            self.start_thread_signal.emit()
        except:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
