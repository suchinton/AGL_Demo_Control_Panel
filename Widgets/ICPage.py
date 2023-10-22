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

from extras.FeedKuksa import FeedKuksa
import os
import sys
from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtCore import QObject, pyqtSignal
import time
from PyQt5.QtWidgets import QWidget
from qtwidgets import AnimatedToggle
import threading
import logging

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
    """
    This class represents the ICWidget which is a widget for the AGL Demo Control Panel.
    It inherits from the Base and Form classes.
    """

    def __init__(self, parent=None):
        """
        Initializes the ICWidget object.

        Args:
        - parent: The parent widget. Defaults to None.
        """
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)

        self.IC = IC_Paths()
        # self.vehicle_simulator = VehicleSimulator(self)

        self.feed_kuksa = FeedKuksa()
        self.vehicle_simulator = VehicleSimulator()

        header_frame = self.findChild(QWidget, "header_frame")
        layout = header_frame.layout()

        self.IC_Frame = self.findChild(QWidget, "frame_1")

        self.Script_toggle = AnimatedToggle(
            checked_color="#4BD7D6",
            pulse_checked_color="#00ffff"
        )

        layout.replaceWidget(self.demoToggle, self.Script_toggle)
        self.demoToggle.deleteLater()

        buttons = [self.parkBtn,
                   self.reverseBtn,
                   self.neutralBtn,
                   self.driveBtn]

        # group for the buttons for mutual exclusion

        self.vehicle_simulator.speed_changed.connect(self.set_Vehicle_Speed)
        self.vehicle_simulator.rpm_changed.connect(self.set_Vehicle_RPM)

        self.driveGroupBtns = QtWidgets.QButtonGroup(self)
        self.driveGroupBtns.setExclusive(True)

        for button in buttons:
            self.driveGroupBtns.addButton(button)

        self.driveGroupBtns.buttonClicked.connect(self.driveBtnClicked)

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
        self.Script_toggle.clicked.connect(self.handle_Script_toggle)
        self.leftIndicatorBtn.setCheckable(True)
        self.rightIndicatorBtn.setCheckable(True)
        self.hazardBtn.setCheckable(True)

        self.leftIndicatorBtn.toggled.connect(self.leftIndicatorBtnClicked)
        self.rightIndicatorBtn.toggled.connect(self.rightIndicatorBtnClicked)
        self.hazardBtn.toggled.connect(self.hazardBtnClicked)

    def set_Vehicle_Speed(self, speed):
        self.Speed_slider.setValue(speed)

    def set_Vehicle_RPM(self, rpm):
        self.RPM_slider.setValue(rpm)

    def update_Speed_monitor(self):
        """
        Updates the speed monitor with the current speed value.
        """
        speed = int(self.Speed_slider.value())
        self.Speed_monitor.display(speed)
        try:
            self.feed_kuksa.send_values(self.IC.speed, str(speed), 'value')
        except Exception as e:
            logging.error(f"Error sending values to kuksa {e}")

    def update_RPM_monitor(self):
        """
        Updates the RPM monitor with the current RPM value.
        """
        rpm = int(self.RPM_slider.value())
        self.RPM_monitor.display(rpm)
        try:
            self.feed_kuksa.send_values(self.IC.engineRPM, str(rpm), 'value')
        except Exception as e:
            logging.error(f"Error sending values to kuksa {e}")

    def update_coolantTemp_monitor(self):
        """
        Updates the coolant temperature monitor with the current coolant temperature value.
        """
        coolantTemp = int(self.coolantTemp_slider.value())
        try:
            self.feed_kuksa.send_values(
                self.IC.coolantTemp, str(coolantTemp), 'value')
        except Exception as e:
            logging.error(f"Error sending values to kuksa {e}")

    def update_fuelLevel_monitor(self):
        """
        Updates the fuel level monitor with the current fuel level value.
        """
        fuelLevel = int(self.fuelLevel_slider.value())
        try:
            self.feed_kuksa.send_values(self.IC.fuelLevel, str(fuelLevel))
        except Exception as e:
            logging.error(f"Error sending values to kuksa {e}")

    def hazardBtnClicked(self):
        """
        Handles the hazard button click event.
        """
        hazardIcon = QPixmap(":/Images/Images/hazard.png")
        painter = QPainter(hazardIcon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)

        if self.hazardBtn.isChecked():
            color = QtCore.Qt.yellow
            value = "true"
        else:
            color = QtCore.Qt.black
            value = "false"

        painter.fillRect(hazardIcon.rect(), color)
        painter.end()
        self.hazardBtn.setIcon(QIcon(hazardIcon))

        self.leftIndicatorBtn.setChecked(self.hazardBtn.isChecked())
        self.rightIndicatorBtn.setChecked(self.hazardBtn.isChecked())

        try:
            self.feed_kuksa.send_values(self.IC.leftIndicator, value)
            self.feed_kuksa.send_values(self.IC.rightIndicator, value)
            self.feed_kuksa.send_values(self.IC.hazard, value)
        except Exception as e:
            logging.error(f"Error sending values to kuksa {e}")

    def leftIndicatorBtnClicked(self):
        """
        Handles the left indicator button click event.
        """
        leftIndicatorIcon = QPixmap(":/Images/Images/left.png")
        painter = QPainter(leftIndicatorIcon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)

        if self.leftIndicatorBtn.isChecked():
            color = QtCore.Qt.green
            value = "true"
        else:
            color = QtCore.Qt.black
            value = "false"

        painter.fillRect(leftIndicatorIcon.rect(), color)
        painter.end()
        self.leftIndicatorBtn.setIcon(QIcon(leftIndicatorIcon))

        try:
            self.feed_kuksa.send_values(self.IC.leftIndicator, value)
        except Exception as e:
            logging.error(f"Error sending values to kuksa {e}")

    def rightIndicatorBtnClicked(self):
        """
        Handles the right indicator button click event.
        """
        rightIndicatorIcon = QPixmap(":/Images/Images/right.png")
        painter = QPainter(rightIndicatorIcon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)

        if self.rightIndicatorBtn.isChecked():
            color = QtCore.Qt.green
            value = "true"
        else:
            color = QtCore.Qt.black
            value = "false"

        painter.fillRect(rightIndicatorIcon.rect(), color)
        painter.end()
        self.rightIndicatorBtn.setIcon(QIcon(rightIndicatorIcon))

        try:
            self.feed_kuksa.send_values(self.IC.rightIndicator, value)
        except Exception as e:
            logging.error(f"Error sending values to kuksa {e}")

    def accelerationBtnPressed(self):
        """
        Handles the acceleration button press event.
        """
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

    def handle_Script_toggle(self):
        if self.Script_toggle.isChecked():
            self.set_Vehicle_RPM(1000)
            self.set_Vehicle_Speed(0)
            self.vehicle_simulator.start()
        else:
            self.vehicle_simulator.stop()

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
        gear_mapping = {
            self.driveBtn: "127",
            self.parkBtn: "126",
            self.reverseBtn: "-1",
            self.neutralBtn: "0"
        }

        checked_button = self.driveGroupBtns.checkedButton()

        if checked_button in gear_mapping:
            gear_value = gear_mapping[checked_button]
            self.accelerationBtn.setEnabled(True)
            self.Speed_slider.setEnabled(checked_button != self.neutralBtn)
            self.RPM_slider.setEnabled(True)
            try:
                self.feed_kuksa.send_values(self.IC.selectedGear, gear_value)
            except Exception as e:
                logging.error(f"Error sending values to kuksa {e}")
        else:
            print("Unknown button checked!")


class AccelerationFns():
    WHEEL_CIRCUMFERENCE = 0.48 * 3.14  # in meters
    GEAR_RATIOS = [3.36, 2.10, 1.48, 1.16, 0.95, 0.75]

    def calculate_speed(time, acceleration) -> int:
        time = time / 1000  # convert milliseconds to seconds
        speed = acceleration * time  # calculate speed
        return int(speed)

    def calculate_engine_rpm(speed) -> int:
        speed = speed * 1000 / 3600  # Convert speed from km/h to m/s
        wheel_rps = speed / AccelerationFns.WHEEL_CIRCUMFERENCE

        current_gear = None
        for i, ratio in enumerate(AccelerationFns.GEAR_RATIOS, start=1):
            if wheel_rps * ratio < 8000 / 60:
                current_gear = i
                break

        # If no gear is found, use the highest gear
        if current_gear is None:
            current_gear = len(AccelerationFns.GEAR_RATIOS)

        engine_rpm = wheel_rps * \
            AccelerationFns.GEAR_RATIOS[current_gear - 1] * 60

        return int(engine_rpm)


class VehicleSimulator(QObject):
    # Define signals for updating speed and rpm
    speed_changed = pyqtSignal(int)
    rpm_changed = pyqtSignal(int)

    DEFAULT_IDLE_RPM = 1000

    def __init__(self):
        super().__init__()
        self.freq = 10
        self.vehicle_speed = 0
        self.engine_speed = self.DEFAULT_IDLE_RPM
        self.running = False
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self.run, daemon=True)

    def start(self):
        if not self.running:
            self.reset()
            self.running = True
            self.thread.start()

    def stop(self):
        self.running = False

    def reset(self):
        with self.lock:
            self.vehicle_speed = 0
            self.engine_speed = self.DEFAULT_IDLE_RPM

    def run(self):
        while self.running:
            if not self.running:
                break

            # Simulate acceleration and update speed and rpm
            self.accelerate(60, 1800, 3)
            self.accelerate(65, 1700, 1)
            self.accelerate(80, 2500, 6)
            self.accelerate(100, 3000, 4)
            self.brake(80, 3000, 3)
            self.accelerate(104, 4000, 6)
            self.brake(40, 2000, 4)
            self.accelerate(90, 3000, 5)
            self.brake(1, 650, 5)

            # Ensure reset is called when not in cruise mode
            if not self.running:
                self.reset()

            time.sleep(5)

    def accelerate(self, target_speed, target_rpm, duration):
        if target_speed <= self.vehicle_speed:
            return
        v = (target_speed - self.vehicle_speed) / (duration * self.freq)
        r = (target_rpm - self.engine_speed) / (duration * self.freq)
        while self.vehicle_speed < target_speed and self.running:
            with self.lock:
                self.vehicle_speed += v
                self.engine_speed += r
                self.speed_changed.emit(int(self.vehicle_speed))
                self.rpm_changed.emit(int(self.engine_speed))
            time.sleep(1 / self.freq)

    def brake(self, target_speed, target_rpm, duration):
        if target_speed >= self.vehicle_speed:
            return
        v = (self.vehicle_speed - target_speed) / (duration * self.freq)
        r = (self.engine_speed - target_rpm) / (duration * self.freq)
        while self.vehicle_speed > target_speed and self.running:
            with self.lock:
                self.vehicle_speed -= v
                self.engine_speed -= r
                self.speed_changed.emit(int(self.vehicle_speed))
                self.rpm_changed.emit(int(self.engine_speed))
            time.sleep(1 / self.freq)

    def increase(self, bycruise=True):
        if self.CRUISEACTIVE:
            target_speed = self.vehicle_speed + 5
            target_rpm = self.engine_speed * 1.1
            self.accelerate(target_speed, target_rpm, 2, bycruise)

    def decrease(self, bycruise=True):
        if self.CRUISEACTIVE:
            target_speed = self.vehicle_speed - 5
            target_rpm = self.engine_speed * 0.9
            self.brake(target_speed, target_rpm, 2, bycruise)

    def resume(self, bycruise=True):
        target_speed = self.CRUISESPEED
        target_rpm = self.CRUISERPM
        current_speed = self.get_vehicle_speed()
        if target_speed > current_speed:
            self.accelerate(target_speed, target_rpm, 2, bycruise)
        else:
            self.brake(target_speed, target_rpm, 2, bycruise)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = ICWidget()
    w.show()
    sys.exit(app.exec_())
