import os
import sys
import time
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QSlider, QLCDNumber, QPushButton
from PyQt5.QtGui import QIcon, QPixmap, QPainter
import math

current_dir = os.path.dirname(os.path.abspath(__file__))

# ========================================

sys.path.append(os.path.dirname(current_dir))

import extras.Kuksa_Instance as kuksa_instance

Form, Base = uic.loadUiType(os.path.join(current_dir, "../ui/IC.ui"))

# ========================================


class IC_Paths():
    def __init__(self):
        self.speed = "Vehicle.Speed"
        self.engineRPM = "Vehicle.Powertrain.CombustionEngine.Speed"
        self.leftIndicator = "Vehicle.Body.Lights.DirectionIndicator.Left.IsSignaling"
        self.rightIndicator = "Vehicle.Body.Lights.DirectionIndicator.Right.IsSignaling"
        self.fuelLevel = "Vehicle.Powertrain.FuelSystem.Level"
        self.coolantTemp = "Vehicle.Powertrain.CombustionEngine.ECT"

class ICWidget(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.set_instance()

        self.IC = IC_Paths()

        self.reconnectBtn = self.findChild(QPushButton, "reconnectBtn")
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

        self.reconnectBtn.clicked.connect(self.set_instance)

        self.Speed_slider.valueChanged.connect(self.update_Speed_monitor)
        self.Speed_slider.setMinimum(0)
        self.Speed_slider.setMaximum(240)

        self.RPM_slider.valueChanged.connect(self.update_RPM_monitor)
        self.RPM_slider.setMinimum(0)
        self.RPM_slider.setMaximum(8000)

        self.coolantTemp_slider.valueChanged.connect(self.update_coolantTemp_monitor)
        self.fuelLevel_slider.valueChanged.connect(self.update_fuelLevel_monitor)

        self.accelerationBtn.clicked.connect(self.accelerationBtnClicked)

        # make both buttons checkable
        self.leftIndicatorBtn.setCheckable(True)
        self.rightIndicatorBtn.setCheckable(True)
        self.hazardBtn.setCheckable(True)

        self.leftIndicatorBtn.clicked.connect(self.leftIndicatorBtnClicked)
        self.rightIndicatorBtn.clicked.connect(self.rightIndicatorBtnClicked)
        self.hazardBtn.clicked.connect(self.hazardBtnClicked)

        # Create QTimer object
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(lambda: [self.send_value(),self.updateSpeedAndEngineRpm] if self.client is not None else self.set_instance())

        # Create QThread object
        self.thread = QtCore.QThread()
        self.timer.moveToThread(self.thread)
        self.thread.started.connect(self.timer.start)
        # Start thread
        self.thread.start()

    def set_instance(self):
        self.kuksa = kuksa_instance.KuksaClientSingleton.get_instance()
        self.client = self.kuksa.get_client()
        if self.client is None:
            print("Client is None")

    def update_Speed_monitor(self):
        speed = int(self.Speed_slider.value())
        self.Speed_monitor.display(speed)

    def update_RPM_monitor(self):
        rpm = int(self.RPM_slider.value())
        self.RPM_monitor.display(rpm)

    def update_coolantTemp_monitor(self):
        coolantTemp = int(self.coolantTemp_slider.value())
        self.client.setValue(self.IC.coolantTemp, str(coolantTemp), 'value')

    def update_fuelLevel_monitor(self):
        fuelLevel = int(self.fuelLevel_slider.value())
        self.client.setValue(self.IC.fuelLevel, str(fuelLevel), 'value')

    def send_value(self):
        speed = int(self.Speed_slider.value())
        rpm = int(self.RPM_slider.value())

        try:
            self.client.setValue(self.IC.speed, str(speed), 'value')
            self.client.setValue(self.IC.engineRPM, str(rpm), 'value')

        except Exception as e:
            print(e)

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
            self.client.setValue(self.IC.leftIndicator, "true")
            self.client.setValue(self.IC.rightIndicator, "true")
        else:
            painter = QPainter(hazardIcon)
            painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter.fillRect(hazardIcon.rect(), QtCore.Qt.black)
            painter.end()
            self.hazardBtn.setIcon(QIcon(hazardIcon))

            self.leftIndicatorBtn.setChecked(False)
            self.rightIndicatorBtn.setChecked(False)
            self.client.setValue(self.IC.leftIndicator, "false")
            self.client.setValue(self.IC.rightIndicator, "false")

    def leftIndicatorBtnClicked(self):
        leftIndicatorIcon = QPixmap(":/Images/Images/left.png")
        if self.leftIndicatorBtn.isChecked():     

            painter = QPainter(leftIndicatorIcon)
            painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter.fillRect(leftIndicatorIcon.rect(), QtCore.Qt.green)
            painter.end()

            self.leftIndicatorBtn.setIcon(QIcon(leftIndicatorIcon))
            self.client.setValue(self.IC.leftIndicator, "true")
        else:

            painter = QPainter(leftIndicatorIcon)
            painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter.fillRect(leftIndicatorIcon.rect(), QtCore.Qt.black)
            painter.end()

            self.leftIndicatorBtn.setIcon(QIcon(leftIndicatorIcon))
            self.client.setValue(self.IC.leftIndicator, "false")

    def rightIndicatorBtnClicked(self):
        rightIndicatorIcon = QPixmap(":/Images/Images/right.png")
        if self.rightIndicatorBtn.isChecked():

            painter = QPainter(rightIndicatorIcon)
            painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter.fillRect(rightIndicatorIcon.rect(), QtCore.Qt.green)
            painter.end()
            self.rightIndicatorBtn.setIcon(QIcon(rightIndicatorIcon))

            self.client.setValue(self.IC.rightIndicator, "true")
        else:

            painter = QPainter(rightIndicatorIcon)
            painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter.fillRect(rightIndicatorIcon.rect(), QtCore.Qt.black)
            painter.end()
            self.rightIndicatorBtn.setIcon(QIcon(rightIndicatorIcon))
            self.client.setValue(self.IC.rightIndicator, "false")

    def calculate_speed(self, time):
        # Use the given acceleration of 0-60 in 5 seconds
        acceleration = 60 / 5 # acceleration from 0 to 60 in 5 seconds
        time = time / 1000 # convert milliseconds to seconds
        speed = acceleration * time # calculate speed
        return speed

    def calculate_engine_rpm(self,speed):
        # Use the wheel diameter of a Tesla Model 3 as an example
        wheel_diameter = 0.48 # in meters [1]
        wheel_circumference = wheel_diameter * 3.14 # in meters

        # Use the average sports car gear ratios [2]
        gear_ratios = [3.36, 2.10, 1.48, 1.16, 0.95, 0.81]

        # Convert speed from km/h to m/s
        speed = speed * 1000 / 3600

        # Calculate the wheel revolutions per second
        wheel_rps = speed / wheel_circumference

        # Find the current gear based on the wheel rps
        current_gear = None
        for i in range(len(gear_ratios)):
            if wheel_rps * gear_ratios[i] < 8000 / 60: # assuming max rpm is 8000
                current_gear = i + 1
                break

        # If no gear is found, use the highest gear
        if current_gear is None:
            current_gear = len(gear_ratios)

        # Calculate the engine rpm based on the current gear ratio
        engine_rpm = wheel_rps * gear_ratios[current_gear - 1] * 60

        return engine_rpm

    def calculate_speed_from_rpm_and_gear(self,rpm,gear):
        # Use the wheel diameter of a Tesla Model 3 as an example
        wheel_diameter = 0.48 # in meters [1]
        wheel_circumference = wheel_diameter * 3.14 # in meters

        # Use the average sports car gear ratios [2]
        gear_ratios = [3.36, 2.10, 1.48, 1.16, 0.95, 0.81]

        # Calculate the wheel revolutions per second
        wheel_rps = rpm / (gear_ratios[gear - 1] * 60)

        # Calculate the speed in m/s
        speed = wheel_rps * wheel_circumference

        # Convert speed from m/s to km/h
        speed = speed * 3600 / 1000

        return speed

    def accelerationBtnClicked(self):
        self.startTime = QtCore.QTime.currentTime()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateSpeedAndEngineRpm)
        self.timer.start(100)

    def updateSpeedAndEngineRpm(self):
        currentTime = QtCore.QTime.currentTime()
        duration = self.startTime.msecsTo(currentTime)
        speed = self.calculate_speed(duration)
        rpm = self.calculate_engine_rpm(speed)
        self.Speed_slider.setValue(int(speed))
        self.RPM_slider.setValue(int(rpm))
        self.send_value()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = ICWidget()
    w.show()
    sys.exit(app.exec_())
