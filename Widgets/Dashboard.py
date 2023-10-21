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

from PyQt5 import QtCore, QtGui, QtWidgets
from extras.FeedKuksa import FeedKuksa
import os
import sys
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5 import QtSvg

current_dir = os.path.dirname(os.path.abspath(__file__))

# ========================================

sys.path.append(os.path.dirname(current_dir))


Form, Base = uic.loadUiType(os.path.join(current_dir, "../ui/Dashboard.ui"))

# ========================================


class Dashboard(Base, Form):
    """
    A class representing the dashboard widget.

    Attributes:
    - tileClickedSignal: A PyQtSignal emitted when a tile is clicked.

    Methods:
    - __init__(self, parent=None): Initializes the Dashboard widget.
    - set_icon(self, tile, size): Sets the icon for the given tile.
    - tile_clicked(self, tile): Handles the tile click event.
    """

    tileClickedSignal = pyqtSignal()

    def __init__(self, parent=None):
        """
        Initializes the Dashboard widget.

        Parameters:
        - parent: The parent widget. Defaults to None.
        """
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)

        self.feed_kuksa = FeedKuksa()

        Dashboard_tiles = (self.DB_IC_Tile,
                           self.DB_HVAC_Tile,
                           self.DB_Steering_Tile,
                           self.DB_Settings_Tile)

        DashboardTiles = QtWidgets.QButtonGroup(self)

        DashboardTiles.buttonClicked.connect(self.tile_clicked)

        for i, tile in enumerate(Dashboard_tiles):
            self.set_icon(tile, 90)
            DashboardTiles.addButton(tile)

    def set_icon(self, tile, icon_size):
        try:
            if tile == self.DB_IC_Tile:
                file = ":/Carbon_Icons/carbon_icons/meter.svg"
            if tile == self.DB_HVAC_Tile:
                file = ":/Carbon_Icons/carbon_icons/windy--strong.svg"
            if tile == self.DB_Steering_Tile:
                file = ":/Images/Images/steering-wheel.svg"
            if tile == self.DB_Settings_Tile:
                file = ":/Carbon_Icons/carbon_icons/settings.svg"
            getsize = QtSvg.QSvgRenderer(file)
            svg_widget = QtSvg.QSvgWidget(file)
            svg_widget.setFixedSize(getsize.defaultSize()*2)
            svg_widget.setStyleSheet("background-color: transparent;")
            tile.setIcon(QIcon(svg_widget.grab()))
            tile.setIconSize(QtCore.QSize(icon_size, icon_size))
        except Exception as e:
            print(f"Failed to set icon: {e}")

    def tile_clicked(self, tile):
        """
        Handles the tile click event.

        Parameters:
        - tile: The tile that was clicked.
        """
        if tile == self.DB_IC_Tile:
            self.parent().setCurrentIndex(1)
        elif tile == self.DB_HVAC_Tile:
            self.parent().setCurrentIndex(2)
        elif tile == self.DB_Steering_Tile:
            self.parent().setCurrentIndex(3)
        elif tile == self.DB_Settings_Tile:
            self.parent().setCurrentIndex(4)

        self.tileClickedSignal.emit()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = Dashboard()
    w.show()
    sys.exit(app.exec_())