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

from PyQt5 import QtCore, QtWidgets
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
        icon_mapping = {
            self.DB_IC_Tile: ":/Carbon_Icons/carbon_icons/meter.svg",
            self.DB_HVAC_Tile: ":/Carbon_Icons/carbon_icons/windy--strong.svg",
            self.DB_Steering_Tile: ":/Images/Images/steering-wheel.svg",
            self.DB_Settings_Tile: ":/Carbon_Icons/carbon_icons/settings.svg"
        }

        file = icon_mapping.get(tile)
        if file is None:
            return

        svg_widget = QtSvg.QSvgWidget(file)
        svg_widget.setFixedSize(QtSvg.QSvgRenderer(file).defaultSize()*2)
        svg_widget.setStyleSheet("background-color: transparent;")
        tile.setIcon(QIcon(svg_widget.grab()))
        tile.setIconSize(QtCore.QSize(icon_size, icon_size))

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
