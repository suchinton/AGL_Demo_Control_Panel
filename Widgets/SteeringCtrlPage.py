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
from PyQt5.QtWidgets import QApplication, QButtonGroup
from PyQt5.QtCore import QThread

import time

current_dir = os.path.dirname(os.path.abspath(__file__))

# ========================================

sys.path.append(os.path.dirname(current_dir))

from extras.FeedKuksa import FeedKuksa
import extras.FeedCAN as feed_can

Form, Base = uic.loadUiType(os.path.join(current_dir, "../ui/SteeringControls.ui"))

# ========================================

class Steering_Paths():
    def __init__(self):
        self.switches = {
            "VolumeUp": ["Vehicle.Cabin.SteeringWheel.Switches.VolumeUp","021#FFFFFFFF40000000"],
            "VolumeDown": ["Vehicle.Cabin.SteeringWheel.Switches.VolumeDown","021#FFFFFFFF10000000"],
            "VolumeMute": ["Vehicle.Cabin.SteeringWheel.Switches.VolumeMute","021#FFFFFFFF01000000"],
            "Mode": ["Vehicle.Cabin.SteeringWheel.Switches.Mode","021#FFFFFFFF20000000"],
            "NextTrack": ["Vehicle.Cabin.SteeringWheel.Switches.Next","021#FFFFFFFF08000000"],
            "PreviousTrack": ["Vehicle.Cabin.SteeringWheel.Switches.Previous","021#FFFFFFFF80000000"],
            "Info": ["Vehicle.Cabin.SteeringWheel.Switches.Info","021#FFFFFFFF02000000"],
            "PhoneCall": ["Vehicle.Cabin.SteeringWheel.Switches.PhoneCall","021#FFFFFFFF00010000"],
            "PhoneHangup": ["Vehicle.Cabin.SteeringWheel.Switches.PhoneHangup","021#FFFFFFFF00020000"],
            "Voice": ["Vehicle.Cabin.SteeringWheel.Switches.Voice","021#FFFFFFFF00040000"],
            "LaneDeparture": ["Vehicle.Cabin.SteeringWheel.Switches.LaneDepartureWarning","021#FFFFFFFF00000001"],
            "Horn": ["Vehicle.Cabin.SteeringWheel.Switches.Horn","021#FFFFFFFF00000080"],
            "CruiseEnable": ["Vehicle.Cabin.SteeringWheel.Switches.CruiseEnable","021#FFFFFFFF00008000"],
            "CruiseSet": ["Vehicle.Cabin.SteeringWheel.Switches.CruiseSet","021#FFFFFFFF00001000"],
            "CruiseResume": ["Vehicle.Cabin.SteeringWheel.Switches.CruiseResume",],
            "CruiseCancel": ["Vehicle.Cabin.SteeringWheel.Switches.CruiseCancel","021#FFFFFFFF00000800"],
            "CruiseLimit": ["Vehicle.Cabin.SteeringWheel.Switches.CruiseLimit","021#FFFFFFFF00000200"],
            "CruiseDistance": ["Vehicle.Cabin.SteeringWheel.Switches.CruiseDistance","021#FFFFFFFF00000100"]
        }
        
class SteeringCtrlWidget(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        
        self.Steering = Steering_Paths()
        self.feed_kuksa = FeedKuksa()
        self.add_buttons()

    def add_buttons(self):

        # Define button groups and actions
        LeftControlsBtns = [self.VolumeUp,
                               self.VolumeDown,
                               self.Mode,
                               self.VolumeMute,
                               self.NextTrack,
                               self.PreviousTrack,
                               self.Info]
         

        PhoneBtns = [self.PhoneCall, self.PhoneHangup]
        ExtraContolsBtns = [self.Voice, self.LaneDeparture]

        RightControlsBtns = [self.CruiseEnable,
                            self.CruiseSet,
                            self.CruiseResume,
                            self.CruiseCancel,
                            self.CruiseLimit,
                            self.CruiseDistance]

        self.LeftControlsBtnsGroup = QButtonGroup()
        self.PhoneBtnsGroup = QButtonGroup()
        self.ExtraContolsBtnsGroup = QButtonGroup()
        self.RiqhtControlsBtnsGroup = QButtonGroup()

        for btn in LeftControlsBtns:
            self.LeftControlsBtnsGroup.addButton(btn)

        for btn in PhoneBtns:
            self.PhoneBtnsGroup.addButton(btn)
            

        for btn in RightControlsBtns:
            self.RiqhtControlsBtnsGroup.addButton(btn)

        self.LeftControlsBtnsGroup.buttonClicked.connect(self.left_controls_clicked)
        self.RiqhtControlsBtnsGroup.buttonClicked.connect(self.right_controls_clicked)

        self.Horn.clicked.connect(self.horn_clicked)

    def left_controls_clicked(self, button):
        button_clicked = button.objectName()
        feed_can.send_can_signal(self.Steering.switches[button_clicked][1])
        print("Left controls clicked")

    def right_controls_clicked(self):
        print("Right controls clicked")

    def horn_clicked(self):
        print("Horn clicked")

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = SteeringCtrlWidget()
    w.show()
    sys.exit(app.exec_())