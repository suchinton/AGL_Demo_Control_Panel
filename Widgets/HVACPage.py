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
from PyQt5.QtWidgets import QApplication, QListWidget, QSlider, QPushButton

current_dir = os.path.dirname(os.path.abspath(__file__))

# ========================================

sys.path.append(os.path.dirname(current_dir))

from extras.FeedKuksa import FeedKuksa

Form, Base = uic.loadUiType(os.path.join(current_dir, "../ui/HVAC.ui"))

# ========================================

class HVAC_Paths():
    def __init__(self):
        self.leftTemp = "Vehicle.Cabin.HVAC.Station.Row1.Left.Temperature"
        self.leftFanSpeed = "Vehicle.Cabin.HVAC.Station.Row1.Left.FanSpeed"
        self.rightTemp = "Vehicle.Cabin.HVAC.Station.Row1.Right.Temperature"
        self.rightFanSpeed = "Vehicle.Cabin.HVAC.Station.Row1.Right.FanSpeed"

        # temperatureList contains values from 32 to 16 
        self.temperatureList = [str(i) + "°C" for i in range(32, 15, -1)]

class HVACWidget(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        
        self.HVAC = HVAC_Paths()

        self.feed_kuksa = FeedKuksa()
        
        self.leftTempList = self.findChild(QListWidget, "leftTempList")
        self.leftTempList.addItems(self.HVAC.temperatureList)
        self.leftTempList.setCurrentRow(0)
        self.leftTempList.itemClicked.connect(self.leftTempListClicked)
        self.leftTempList.itemSelectionChanged.connect(self.leftTempListClicked)
        self.leftTempList.wheelEvent = lambda event: None

        self.rightTempList = self.findChild(QListWidget, "rightTempList")
        self.rightTempList.addItems(self.HVAC.temperatureList)
        self.rightTempList.setCurrentRow(0)
        self.rightTempList.itemClicked.connect(self.rightTempListClicked)
        self.rightTempList.itemSelectionChanged.connect(self.rightTempListClicked)
        self.rightTempList.wheelEvent = lambda event: None

        self.leftTempUp = self.findChild(QPushButton, "leftTempUp")
        self.leftTempUp.clicked.connect(lambda: self.leftTempList.setCurrentRow(self.leftTempList.currentRow() - 1))

        self.leftTempDown = self.findChild(QPushButton, "leftTempDown")
        self.leftTempDown.clicked.connect(lambda: self.leftTempList.setCurrentRow(self.leftTempList.currentRow() + 1))

        self.rightTempUp = self.findChild(QPushButton, "rightTempUp")
        self.rightTempUp.clicked.connect(lambda: self.rightTempList.setCurrentRow(self.rightTempList.currentRow() - 1))

        self.rightTempDown = self.findChild(QPushButton, "rightTempDown")
        self.rightTempDown.clicked.connect(lambda: self.rightTempList.setCurrentRow(self.rightTempList.currentRow() + 1))

        self.leftFanSpeed_slider = self.findChild(QSlider, "leftFanSpeed_slider")
        self.leftFanSpeed_slider.valueChanged.connect(self.leftFanSpeed_sliderChanged)

        self.rightFanSpeed_slider = self.findChild(QSlider, "rightFanSpeed_slider")
        self.rightFanSpeed_slider.valueChanged.connect(self.rightFanSpeed_sliderChanged)

    def leftTempListClicked(self):
        item = self.leftTempList.currentItem()
        self.leftTempList.scrollToItem(item, 1)
        self.feed_kuksa.send_values(self.HVAC.leftTemp, item.text()[:-2])
        print(item.text())

    def rightTempListClicked(self):
        item = self.rightTempList.currentItem()
        self.rightTempList.scrollToItem(item, 1)
        self.feed_kuksa.send_values(self.HVAC.rightTemp, item.text()[:-2])
        print(item.text())

    def leftFanSpeed_sliderChanged(self):
        value = self.leftFanSpeed_slider.value()
        self.feed_kuksa.send_values(self.HVAC.leftFanSpeed, str(value))
        print(value)

    def rightFanSpeed_sliderChanged(self):
        value = self.rightFanSpeed_slider.value()
        self.feed_kuksa.send_values(self.HVAC.rightFanSpeed, str(value))
        print(value)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = HVACWidget()
    w.show()
    sys.exit(app.exec_())
