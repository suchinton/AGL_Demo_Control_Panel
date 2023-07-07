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

import extras.Kuksa_Instance as kuksa_instance
import os
import sys
from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QSlider, QLCDNumber, QPushButton
from PyQt5.QtGui import QIcon, QPixmap, QPainter
import time
from PyQt5.QtCore import QThread

current_dir = os.path.dirname(os.path.abspath(__file__))

# ========================================

sys.path.append(os.path.dirname(current_dir))


Form, Base = uic.loadUiType(os.path.join(current_dir, "../ui/IC.ui"))

# ========================================


class IC_Paths():
    def __init__(self):
        self.speed = "Vehicle.Speed"
        self.engineRPM = "Vehicle.Powertrain.CombustionEngine.Speed"
        self.leftIndicator = "Vehicle.Body.Lights.DirectionIndicator.Left.IsSignaling"
        self.rightIndicator = "Vehicle.Body.Lights.DirectionIndicator.Right.IsSignaling"
        self.hazard = "Vehicle.Body.Lights.Hazard.IsSignaling"
        self.fuelLevel = "Vehicle.Powertrain.FuelSystem.Level"
        self.coolantTemp = "Vehicle.Powertrain.CombustionEngine.ECT"
        self.selectedGear = "Vehicle.Powertrain.Transmission.SelectedGear"


class ICWidget(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        
        self.IC = IC_Paths()

        self.kuksa_feeder = FeedKuksa()
        self.kuksa_feeder.start()

        # # load the stylesheet
        # theme = open(os.path.join(current_dir, "../ui/styles/Tron/ICPage.qss"), 'r')
        # self.setStyleSheet(theme.read())
        # theme.close()

        self.scriptBtn = self.findChild(QPushButton, "scriptBtn")

        self.Speed_slider = self.findChild(QSlider, "Speed_slider")
        self.Speed_monitor = self.findChild(QLCDNumber, "Speed_monitor")
        self.RPM_slider = self.findChild(QSlider, "RPM_slider")
        self.RPM_monitor = self.findChild(QLCDNumber, "RPM_monitor")

        self.coolantTemp_slider = self.findChild(QSlider, "coolantTemp_slider")
        self.fuelLevel_slider = self.findChild(QSlider, "fuelLevel_slider")

        self.accelerationBtn = self.findChild(QPushButton, "accelerationBtn")

        self.leftIndicatorBtn = self.findChild(QPushButton, "leftIndicatorBtn")
        self.rightIndicatorBtn = self.findChild(QPushButton, "rightIndicatorBtn")
        self.hazardBtn = self.findChild(QPushButton, "hazardBtn")

        buttons = [self.parkBtn,
                   self.reverseBtn,
                   self.neutralBtn,
                   self.driveBtn]

        # group for the buttons for mutual exclusion
        self.driveGroupBtns = QtWidgets.QButtonGroup(self)
        self.driveGroupBtns.setExclusive(True)

        for button in buttons:
            self.driveGroupBtns.addButton(button)

        self.driveGroupBtns.buttonClicked.connect(self.driveBtnClicked)

        self.scriptBtn.clicked.connect(self.scriptBtnClicked)

        self.Speed_slider.valueChanged.connect(self.update_Speed_monitor)
        self.Speed_slider.setMinimum(0)
        self.Speed_slider.setMaximum(240)

        self.RPM_slider.valueChanged.connect(self.update_RPM_monitor)
        self.RPM_slider.setMinimum(0)
        self.RPM_slider.setMaximum(8000)

        self.coolantTemp_slider.valueChanged.connect(
            self.update_coolantTemp_monitor)
        self.fuelLevel_slider.valueChanged.connect(
            self.update_fuelLevel_monitor)

        self.accelerationBtn.pressed.connect(self.accelerationBtnPressed)
        self.accelerationBtn.released.connect(self.accelerationBtnReleased)

        # make both buttons checkable
        self.leftIndicatorBtn.setCheckable(True)
        self.rightIndicatorBtn.setCheckable(True)
        self.hazardBtn.setCheckable(True)

        self.leftIndicatorBtn.clicked.connect(self.leftIndicatorBtnClicked)
        self.rightIndicatorBtn.clicked.connect(self.rightIndicatorBtnClicked)
        self.hazardBtn.clicked.connect(self.hazardBtnClicked)

    def scriptBtnClicked(self):
        if self.scriptBtn.isChecked():
            ICScript.start_script()

        if not self.ScriptBtn.isChecked():
            ICScript.stop_script()

    def update_Speed_monitor(self):
        speed = int(self.Speed_slider.value())
        self.Speed_monitor.display(speed)
        self.kuksa_feeder.send_values(self.IC.speed, str(speed), 'value')

    def update_RPM_monitor(self):
        rpm = int(self.RPM_slider.value())
        self.RPM_monitor.display(rpm)
        self.kuksa_feeder.send_values(self.IC.engineRPM, str(rpm), 'value')

    def update_coolantTemp_monitor(self):
        coolantTemp = int(self.coolantTemp_slider.value())
        self.kuksa_feeder.send_values(self.IC.coolantTemp, str(coolantTemp), 'value')

    def update_fuelLevel_monitor(self):
        fuelLevel = int(self.fuelLevel_slider.value())
        self.kuksa_feeder.send_values(self.IC.fuelLevel, str(fuelLevel))

    def hazardBtnClicked(self):
        hazardIcon = QPixmap(":/Images/Images/hazard.png")
        if self.hazardBtn.isChecked():
            painter = QPainter(hazardIcon)
            painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter.fillRect(hazardIcon.rect(), QtCore.Qt.yellow)
            painter.end()
            self.hazardBtn.setIcon(QIcon(hazardIcon))

            self.leftIndicatorBtn.setChecked(True)
            self.rightIndicatorBtn.setChecked(True)
            self.kuksa_feeder.send_values(self.IC.leftIndicator, "true")
            self.kuksa_feeder.send_values(self.IC.rightIndicator, "true")
            self.kuksa_feeder.send_values(self.IC.hazard, "true")
        else:
            painter = QPainter(hazardIcon)
            painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter.fillRect(hazardIcon.rect(), QtCore.Qt.black)
            painter.end()
            self.hazardBtn.setIcon(QIcon(hazardIcon))

            self.leftIndicatorBtn.setChecked(False)
            self.rightIndicatorBtn.setChecked(False)
            self.kuksa_feeder.send_values(self.IC.leftIndicator, "false")
            self.kuksa_feeder.send_values(self.IC.rightIndicator, "false")
            self.kuksa_feeder.send_values(self.IC.hazard, "false")

    def leftIndicatorBtnClicked(self):
        leftIndicatorIcon = QPixmap(":/Images/Images/left.png")
        if self.leftIndicatorBtn.isChecked():

            painter = QPainter(leftIndicatorIcon)
            painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter.fillRect(leftIndicatorIcon.rect(), QtCore.Qt.green)
            painter.end()

            self.leftIndicatorBtn.setIcon(QIcon(leftIndicatorIcon))
            self.kuksa_feeder.send_values(self.IC.leftIndicator, "true")
        else:

            painter = QPainter(leftIndicatorIcon)
            painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter.fillRect(leftIndicatorIcon.rect(), QtCore.Qt.black)
            painter.end()

            self.leftIndicatorBtn.setIcon(QIcon(leftIndicatorIcon))
            self.kuksa_feeder.send_values(self.IC.leftIndicator, "false")

    def rightIndicatorBtnClicked(self):
        rightIndicatorIcon = QPixmap(":/Images/Images/right.png")
        if self.rightIndicatorBtn.isChecked():

            painter = QPainter(rightIndicatorIcon)
            painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter.fillRect(rightIndicatorIcon.rect(), QtCore.Qt.green)
            painter.end()
            self.rightIndicatorBtn.setIcon(QIcon(rightIndicatorIcon))
            self.kuksa_feeder.send_values(self.IC.rightIndicator, "true")
        else:

            painter = QPainter(rightIndicatorIcon)
            painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter.fillRect(rightIndicatorIcon.rect(), QtCore.Qt.black)
            painter.end()
            self.rightIndicatorBtn.setIcon(QIcon(rightIndicatorIcon))
            self.kuksa_feeder.send_values(self.IC.rightIndicator, "false")

    def accelerationBtnPressed(self):
        self.startTime = QtCore.QTime.currentTime()
        self.acceleration_timer = QtCore.QTimer()
        self.acceleration_timer.timeout.connect(
            lambda: self.updateSpeedAndEngineRpm("Accelerate"))
        self.acceleration_timer.start(100)

    def accelerationBtnReleased(self):
        if self.Speed_slider.value() <= 0:
            self.acceleration_timer.stop()
        else:
            self.acceleration_timer.timeout.connect(
                lambda: self.updateSpeedAndEngineRpm("Decelerate"))
            self.acceleration_timer.start(100)

    def updateSpeedAndEngineRpm(self, action, acceleration=(60/5)):
        if action == "Accelerate":
            pass
        elif action == "Decelerate":
            acceleration = -acceleration

        currentTime = QtCore.QTime.currentTime()
        duration = self.startTime.msecsTo(currentTime)
        self.current_speed = AccelerationFns.calculate_speed(
            duration, acceleration)
        self.current_rpm = AccelerationFns.calculate_engine_rpm(
            self.current_speed)

        if self.current_speed <= 0:
            self.current_speed = 0
            self.current_rpm = 0
            self.acceleration_timer.stop()

        if self.current_speed >= 240:
            self.current_speed = 240
            self.current_rpm = 0
            self.acceleration_timer.stop()

        self.Speed_slider.setValue(self.current_speed)
        self.RPM_slider.setValue(self.current_rpm)

        self.update_Speed_monitor()
        self.update_RPM_monitor()

    def driveBtnClicked(self):
        #   // Selected Gear output = > 0 = Neutral, 1/2/.. = Forward, -1/.. = Reverse, 126 = Park, 127 = Drive
        # #859287 ; /* light green */

        if self.driveGroupBtns.checkedButton() == self.driveBtn:
            self.accelerationBtn.setEnabled(True)
            self.Speed_slider.setEnabled(True)
            self.RPM_slider.setEnabled(True)
            self.kuksa_feeder.send_values(self.IC.selectedGear, "127")

        if self.driveGroupBtns.checkedButton() == self.parkBtn:
            self.accelerationBtn.setEnabled(False)
            self.Speed_slider.setEnabled(False)
            self.RPM_slider.setEnabled(False)
            self.kuksa_feeder.send_values(self.IC.selectedGear, "126")

        if self.driveGroupBtns.checkedButton() == self.reverseBtn:
            self.accelerationBtn.setEnabled(True)
            self.Speed_slider.setEnabled(True)
            self.RPM_slider.setEnabled(True)
            self.kuksa_feeder.send_values(self.IC.selectedGear, "-1")

        if self.driveGroupBtns.checkedButton() == self.neutralBtn:
            self.accelerationBtn.setEnabled(False)
            self.Speed_slider.setEnabled(False)
            self.RPM_slider.setEnabled(True)
            self.kuksa_feeder.send_values(self.IC.selectedGear, "0")


class AccelerationFns():
    def calculate_speed(time, acceleration) -> int:
        # acceleration = 60 / 5 # acceleration from 0 to 60 in 5 seconds
        time = time / 1000  # convert milliseconds to seconds
        speed = acceleration * time  # calculate speed
        return int(speed)

    def calculate_engine_rpm(speed) -> int:
        wheel_diameter = 0.48  # in meters
        wheel_circumference = wheel_diameter * 3.14  # in meters

        # Adjust the gear ratios to match the desired speed and rpm
        gear_ratios = [3.36, 2.10, 1.48, 1.16, 0.95, 0.75]
        speed = speed * 1000 / 3600  # Convert speed from km/h to m/s
        wheel_rps = speed / wheel_circumference

        current_gear = None
        for i in range(len(gear_ratios)):
            if wheel_rps * gear_ratios[i] < 8000 / 60:
                current_gear = i + 1
                break

        # If no gear is found, use the highest gear
        if current_gear is None:
            current_gear = len(gear_ratios)

        engine_rpm = wheel_rps * gear_ratios[current_gear - 1] * 60

        return int(engine_rpm)


class ICScript(ICWidget):
    def start_script(self):
        ICWidget.reset()

        # disable all widgets in the scroll area
        for widget in ICWidget.scrollAreaWidgetContents.children():
            widget.setEnabled(False)

        rates = [(60/5), (60/4), (60/3)]

        # start assigning values to the  speed and rpm sliders and send them to the IC do this in a loop for each rate
        for rate in rates:
            ICWidget.accelerationBtnPressed()
            ICWidget.acceleration_timer.timeout.connect(
                lambda: ICWidget.updateSpeedAndEngineRpm("Accelerate"), rate)
            ICWidget.acceleration_timer.start(100)
            time.sleep(5)
            ICWidget.accelerationBtnReleased()
            ICWidget.acceleration_timer.timeout.connect(
                lambda: ICWidget.updateSpeedAndEngineRpm("Decelerate"), rate)
            ICWidget.acceleration_timer.start(100)
            time.sleep(5)

    def stop_script(self):
        ICWidget.reset()

        # enable all widgets in the scroll area
        for widget in ICWidget.scrollAreaWidgetContents.children():
            widget.setEnabled(True)

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
    w = ICWidget()
    w.show()
    sys.exit(app.exec_())