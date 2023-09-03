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

import os
import sys
from PyQt5 import uic
from PyQt5 import QtWidgets 
from PyQt5.QtCore import pyqtSignal

current_dir = os.path.dirname(os.path.abspath(__file__))

# ========================================

sys.path.append(os.path.dirname(current_dir))

from extras.FeedKuksa import FeedKuksa

Form, Base = uic.loadUiType(os.path.join(current_dir, "../ui/Dashboard.ui"))

# ========================================

class Dashboard(Base, Form):

    tileClickedSignal = pyqtSignal()

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)

        self.feed_kuksa = FeedKuksa()

        Dashboard_tiles = (self.DB_IC_Tile,
                             self.DB_HVAC_Tile,
                             self.DB_Steering_Tile,
                             self.DB_Settings_Tile)
        
        DashboardTiles = QtWidgets.QButtonGroup(self)

        for i, tile in enumerate(Dashboard_tiles):
            DashboardTiles.addButton(tile)
        
        DashboardTiles.buttonClicked.connect(self.tile_clicked)

    def tile_clicked(self, tile):
        if tile == self.DB_IC_Tile:
            self.parent().setCurrentIndex(1)
        elif tile == self.DB_HVAC_Tile:
            self.parent().setCurrentIndex(2)
        elif tile == self.DB_Steering_Tile:
            self.parent().setCurrentIndex(3)
        elif tile == self.DB_Settings_Tile:
            self.parent().setCurrentIndex(4)

        self.tileClickedSignal.emit()