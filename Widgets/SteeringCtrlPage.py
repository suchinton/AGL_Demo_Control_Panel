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

from . import settings
import extras.FeedCAN as feed_can
from extras.FeedKuksa import FeedKuksa
import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QButtonGroup

current_dir = os.path.dirname(os.path.abspath(__file__))

# ========================================

sys.path.append(os.path.dirname(current_dir))


Form, Base = uic.loadUiType(os.path.join(
    current_dir, "../ui/SteeringControls.ui"))

# ========================================


class Steering_Paths():
    def __init__(self):
        self.switches = {
            "VolumeUp": {
                "Kuksa": "Vehicle.Cabin.SteeringWheel.Switches.VolumeUp",
                "CAN": "021#FFFFFFFF40000000"},
            "VolumeDown": {
                "Kuksa": "Vehicle.Cabin.SteeringWheel.Switches.VolumeDown",
                "CAN": "021#FFFFFFFF10000000"},
            "VolumeMute": {
                "Kuksa": "Vehicle.Cabin.SteeringWheel.Switches.VolumeMute",
                "CAN": "021#FFFFFFFF01000000"},
            "Mode": {
                "Kuksa": "Vehicle.Cabin.SteeringWheel.Switches.Mode",
                "CAN": "021#FFFFFFFF20000000"},
            "NextTrack": {
                "Kuksa": "Vehicle.Cabin.SteeringWheel.Switches.Next",
                "CAN": "021#FFFFFFFF08000000"},
            "PreviousTrack": {
                "Kuksa": "Vehicle.Cabin.SteeringWheel.Switches.Previous",
                "CAN": "021#FFFFFFFF80000000"},
            "Info": {
                "Kuksa": "Vehicle.Cabin.SteeringWheel.Switches.Info",
                "CAN": "021#FFFFFFFF02000000"},
            "PhoneCall": {
                "Kuksa": "Vehicle.Cabin.SteeringWheel.Switches.PhoneCall",
                "CAN": "021#FFFFFFFF00010000"},
            "PhoneHangup": {
                "Kuksa": "Vehicle.Cabin.SteeringWheel.Switches.PhoneHangup",
                "CAN": "021#FFFFFFFF00020000"},
            "Voice": {
                "Kuksa": "Vehicle.Cabin.SteeringWheel.Switches.Voice",
                "CAN": "021#FFFFFFFF00040000"},
            "LaneDeparture": {
                "Kuksa": "Vehicle.Cabin.SteeringWheel.Switches.LaneDepartureWarning",
                "CAN": "021#FFFFFFFF00000001"},
            "Horn": {
                "Kuksa": "Vehicle.Cabin.SteeringWheel.Switches.Horn",
                "CAN": "021#FFFFFFFF00000080"},
            "CruiseEnable": {
                "Kuksa": "Vehicle.Cabin.SteeringWheel.Switches.CruiseEnable",
                "CAN": "021#FFFFFFFF00008000"},
            "CruiseSet": {
                "Kuksa": "Vehicle.Cabin.SteeringWheel.Switches.CruiseSet",
                "CAN": "021#FFFFFFFF00001000"},
            "CruiseResume": {
                "Kuksa": "Vehicle.Cabin.SteeringWheel.Switches.CruiseResume",
                "CAN": "021#FFFFFFFF00004000"},
            "CruiseCancel": {
                "Kuksa": "Vehicle.Cabin.SteeringWheel.Switches.CruiseCancel",
                "CAN": "021#FFFFFFFF00000800"},
            "CruiseLimit": {
                "Kuksa": "Vehicle.Cabin.SteeringWheel.Switches.CruiseLimit",
                "CAN": "021#FFFFFFFF00000200"},
            "CruiseDistance": {
                "Kuksa": "Vehicle.Cabin.SteeringWheel.Switches.CruiseDistance",
                "CAN": "021#FFFFFFFF00000100"}
        }


class SteeringCtrlWidget(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)

        self.Steering = Steering_Paths()
        self.feed_kuksa = FeedKuksa()
        self.settings = settings

        self.add_buttons()

    def add_buttons(self):

        # Define button groups and actions
        ControlsBtns = [self.VolumeUp,
                        self.VolumeDown,
                        self.Mode,
                        self.VolumeMute,
                        self.NextTrack,
                        self.PreviousTrack,
                        self.Info,
                        self.PhoneCall,
                        self.PhoneHangup,
                        self.Voice,
                        self.LaneDeparture,
                        self.Horn,
                        self.CruiseEnable,
                        self.CruiseSet,
                        self.CruiseResume,
                        self.CruiseCancel,
                        self.CruiseLimit,
                        self.CruiseDistance]

        self.ControlsBtnsGroup = QButtonGroup()

        for btn in ControlsBtns:
            self.ControlsBtnsGroup.addButton(btn)

        self.ControlsBtnsGroup.buttonClicked.connect(self.controls_clicked)

    def controls_clicked(self, button):
        button_clicked = button.objectName()
        signal_type = settings.Steering_Signal_Type
        if signal_type == "Kuksa":
            self.feed_kuksa.send_values(
                self.Steering.switches[button_clicked]["Kuksa"], "1")
            self.feed_kuksa.send_values(
                self.Steering.switches[button_clicked]["Kuksa"], "0")
        elif signal_type == "CAN":
            feed_can.send_can_signal(
                self.Steering.switches[button_clicked]["CAN"])
            # Making sure button state goes back to off
            feed_can.send_can_signal("021#FFFFFFFF00000000")


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = SteeringCtrlWidget()
    w.show()
    sys.exit(app.exec_())
