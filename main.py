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
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5 import QtSvg
from PyQt5.QtSvg import *
from PyQt5.QtGui import QIcon

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = uic.loadUiType(os.path.join(current_dir, "Main_Window.ui"))

from extras.UI_Handeler import *
from Widgets.Dashboard import Dashboard

class MainWindow(Base, Form):
    """
    The main window of the AGL Demo Control Panel application.
    Inherits from the Base and Form classes.
    """

    # signal to stop the thread
    stop_thread_signal = QtCore.pyqtSignal()
    start_thread_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        """
        Initializes the MainWindow object.
        Sets up the UI, window flags, and geometry.
        Connects signals and slots for window controls and widget navigation.
        Initializes the Dashboard object and connects its signals.
        """
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
        #self.resize(1400,840)
        self.headerContainer = self.findChild(QWidget, 'headerContainer')
        self.headerContainer.DoubleClickMaximize = lambda: UI_Handeler.toggleMaximized(self)
        self.headerContainer.mouseMoveEvent = lambda event: UI_Handeler.moveWindow(self, event)
        self.headerContainer.mousePressEvent = lambda event: UI_Handeler.mousePressEvent(self, event)
        self.headerContainer.mouseReleaseEvent = lambda event: UI_Handeler.mouseReleaseEvent(self, event)

        self.leftMenuSubContainer = self.findChild(QWidget, 'leftMenuSubContainer')
        self.dashboardButton = self.findChild(QPushButton, 'dashboardButton')
        UI_Handeler.Hide_Navbar(self,bool_arg=True)

        self.stackedWidget.currentChanged.connect(lambda: UI_Handeler.subscribe_VSS_Signals(self) if UI_Handeler.set_instance(self) else None)

        self.notificationContent = self.findChild(QWidget, 'notificationContent')

        # Window Controls
        closeButton = self.findChild(QPushButton, 'closeBtn')
        minimizeButton = self.findChild(QPushButton, 'minimizeBtn')
        maximizeButton = self.findChild(QPushButton, 'maximizeBtn')

        # make the close button also end all threads
        closeButton.clicked.connect(lambda: [self.close(), self.stop_thread_signal.emit()])
        minimizeButton.clicked.connect(self.showMinimized)
        maximizeButton.clicked.connect(lambda: UI_Handeler.toggleMaximized(self))

        # Widget Navigation
        Navigation_buttons = ( self.dashboardButton,
                    self.icButton, 
                    self.hvacButton, 
                    self.steeringCtrlButton,
                    self.settingsBtn)
        
        steering_icon = ":/Images/Images/steering-wheel.svg"
        getsize = QtSvg.QSvgRenderer(steering_icon)
        svg_widget = QtSvg.QSvgWidget(steering_icon)
        svg_widget.setFixedSize(getsize.defaultSize())
        svg_widget.setStyleSheet("background-color: transparent;")
        self.steeringCtrlButton.setIcon(QIcon(svg_widget.grab()))
        
        NavigationButtons = QtWidgets.QButtonGroup(self)
        NavigationButtons.setExclusive(True)

        for i, button in enumerate(Navigation_buttons):
            button.setCheckable(True)
            NavigationButtons.addButton(button)
            button.clicked.connect(partial(UI_Handeler.animateSwitch, self, i))

        self.stackedWidget.currentChanged.connect(self.handleChangedPage)
        
        self.stop_thread_signal.connect(self.stackedWidget.widget(0).feed_kuksa.stop)

        self.stackedWidget.setCurrentIndex(0)        
        self.dashboardButton.setChecked(True)
        UI_Handeler.Hide_Navbar(self,bool_arg=False)

        self.Dashboard = Dashboard()
        self.Dashboard.tileClickedSignal.connect(self.handleTileClicked)

        self.current_page = self.stackedWidget.currentIndex()

        self.centralwidget = self.findChild(QWidget, 'centralwidget')
        self.size_grip = QtWidgets.QSizeGrip(self)
        self.size_grip.setFixedSize(20, 20)
        #self.size_grip.setStyleSheet("QSizeGrip { background-color: transparent; }")
        self.size_grip.setStyleSheet("""
                                        QSizeGrip {
                                            background-color: transparent;
                                            background-image: url(:/Carbon_Icons/carbon_icons/corner.svg);
                                            background-repeat: no-repeat;
                                            background-position: center;
                                            border: none;
                                        }
                                    """)
        self.centralwidget.layout().addWidget(self.size_grip, 0, Qt.AlignBottom | Qt.AlignRight)

    def VSS_callback(self,data):
        pass

    def handleTileClicked(self):
        """
        Handles the tile clicked signal from the Dashboard object.
        Shows the navbar.
        """
        UI_Handeler.Hide_Navbar(self,bool_arg=False)

    def handleChangedPage(self, index):
        """
        Handles the change of pages in the stacked widget.
        Stops the previous thread and starts the new one.
        If the index is 0, the navbar is not hidden. Otherwise, it is hidden.
        """
        if index == 0:
            UI_Handeler.Hide_Navbar(self,bool_arg=False)
        else:
            UI_Handeler.Hide_Navbar(self,bool_arg=True)
        try:
            self.stop_thread_signal.connect(self.stackedWidget.widget(self.current_page).feed_kuksa.stop)
            self.stop_thread_signal.emit()
        except:
            pass

        self.current_page = self.stackedWidget.currentIndex()

        try:
            self.start_thread_signal.connect(self.stackedWidget.widget(self.current_page).feed_kuksa.start)
            self.start_thread_signal.emit()
        except:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("AGL Demo Control Panel")
    app.setWindowIcon(QtGui.QIcon(':/Images/Images/Automotive_Grade_Linux_logo.svg'))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())