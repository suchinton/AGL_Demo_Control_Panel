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
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread

import time

current_dir = os.path.dirname(os.path.abspath(__file__))

# ========================================

sys.path.append(os.path.dirname(current_dir))

import extras.Kuksa_Instance as kuksa_instance

Form, Base = uic.loadUiType(os.path.join(current_dir, "../ui/SteeringControls.ui"))

# ========================================

class Steering_Paths():
    def __init__(self):
        self.VolumeUp = "ehicle.Cabin.SteeringWheel.Switches.VolumeUp"
        self.VolumeDown = "Vehicle.Cabin.SteeringWheel.Switches.VolumeDown"
        self.VolumeMute = "Vehicle.Cabin.SteeringWheel.Switches.VolumeMute"

        self.NextTrack = "Vehicle.Cabin.SteeringWheel.Switches.Next"
        self.PreviousTrack = "Vehicle.Cabin.SteeringWheel.Switches.Previous"

        self.Info = "Vehicle.Cabin.SteeringWheel.Switches.Info"

        self.CruiseEnable = "Vehicle.Cabin.SteeringWheel.Switches.CruiseEnable"

        self.Voice = "Vehicle.Cabin.SteeringWheel.Switches.Voice"
        self.PhoneCall = "Vehicle.Cabin.SteeringWheel.Switches.PhoneCall"
        self.PhoneHangup = "Vehicle.Cabin.SteeringWheel.Switches.PhoneHangup"

        self.Horn = "Vehicle.Cabin.SteeringWheel.Switches.Horn"


class SteeringCtrlWidget(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        
        self.Steering = Steering_Paths()

        self.kuksa_feeder = FeedKuksa()
        self.kuksa_feeder.start()     

class FeedKuksa(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self,parent)
        self.stop_flag = False
        self.set_instance()

    def run(self):
        print("Starting thread")
        self.set_instance()
        while not self.stop_flag:
            self.send_values()

    def stop(self):
        self.stop_flag = True
        print("Stopping thread")

    def set_instance(self):
        self.kuksa = kuksa_instance.KuksaClientSingleton.get_instance()
        self.client = self.kuksa.get_client()

    def send_values(self, Path=None, Value=None, Attribute=None):
        if self.client is not None:
            if self.client.checkConnection() is True:

                if Attribute is not None:
                    self.client.setValue(Path, Value, Attribute)
                else:
                    self.client.setValue(Path, Value)
            else:
                print("Could not connect to Kuksa")
                self.set_instance()
        else:
            print("Kuksa client is None, try reconnecting")
            time.sleep(2)
            self.set_instance()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = SteeringCtrlWidget()
    w.show()
    sys.exit(app.exec_())