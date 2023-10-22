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

from main import *
from PyQt5 import QtCore
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QEasingCurve
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5.QtCore import pyqtSignal
import logging
import json

from . import Kuksa_Instance as kuksa_instance

# Global variables
subscribed = False
block_subscription_updates = False


class UI_Handeler(MainWindow):

    def display_sending_message(self):
        print("message sent")

    def block_updates():
        global block_subscription_updates
        block_subscription_updates = True

    def unblock_updates():
        global block_subscription_updates
        block_subscription_updates = False

    def Hide_Navbar(self, bool_arg):
        """
        This method hides the navigation bar of the UI.

        Args:
        - bool_arg: A boolean value indicating whether to hide the navigation bar or not.
        """
        height = self.BottomMenuSubContainer.height()
        heightExtended = 75 if bool_arg else 0

        self.animation = QPropertyAnimation(
            self.BottomMenuSubContainer, b"minimumHeight")
        self.animation.setDuration(400)
        self.animation.setStartValue(height)
        self.animation.setEndValue(heightExtended)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    def animateSwitch(self, index):
        """
        This method animates the switching of pages for QstackedWidget with the animation being a fade in and out.

        Args:
        - index: The index of the page to switch to.
        """
        self.fader_widget = FaderWidget(
            self.stackedWidget.currentWidget(), self.stackedWidget.widget(index))
        self.stackedWidget.setCurrentIndex(index)

    def toggleMaximized(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def moveWindow(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.clickPosition)
            self.clickPosition = event.globalPos()
            event.accept()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
        event.accept()

    def mouseReleaseEvent(self, event):
        self.clickPosition = None
        event.accept()

    def set_instance(self):
        self.kuksa = kuksa_instance.KuksaClientSingleton.instance()
        self.client = self.kuksa.get_client()
        if self.client is not None and self.client.checkConnection():
            return True
        else:
            logging.error("Kuksa client is not connected, try reconnecting")
            return False

    def stop_client(self):
        if self.client is not None and self.client.checkConnection():
            self.client.stop()

    def subscribe_VSS_Signals(self):
        """
        This method subscribes to the VSS signals from Kuksa.
        """
        global subscribed
        if not subscribed:
            self.kuksa = kuksa_instance.KuksaClientSingleton.instance()
            self.client = self.kuksa.get_client()
            if self.client is not None and self.client.checkConnection():
                signals = [
                    "Vehicle.Speed",
                    "Vehicle.Powertrain.CombustionEngine.Speed",
                    "Vehicle.Body.Lights.DirectionIndicator.Left.IsSignaling",
                    "Vehicle.Body.Lights.DirectionIndicator.Right.IsSignaling",
                    "Vehicle.Body.Lights.Hazard.IsSignaling",
                    "Vehicle.Powertrain.FuelSystem.Level",
                    "Vehicle.Powertrain.CombustionEngine.ECT",
                    "Vehicle.Powertrain.Transmission.SelectedGear",
                    "Vehicle.Cabin.HVAC.Station.Row1.Left.Temperature",
                    "Vehicle.Cabin.HVAC.Station.Row1.Left.FanSpeed",
                    "Vehicle.Cabin.HVAC.Station.Row1.Right.Temperature",
                    "Vehicle.Cabin.HVAC.Station.Row1.Right.FanSpeed"]

                for signal in signals:
                    self.client.subscribe(
                        signal, lambda data: UI_Handeler.VSS_callback(self, data), 'value')
                subscribed = True
            else:
                subscribed = False
                logging.error(
                    "Kuksa client is not connected, try reconnecting")

    def VSS_callback(self, data):
        """
        This method is the callback function for the VSS signals from Kuksa.

        Args:
        - data: The data received from the signal.
        """
        global block_subscription_updates
        if block_subscription_updates:
            return

        IC_Page = self.stackedWidget.widget(1)
        HVAC_Page = self.stackedWidget.widget(2)

        info = json.loads(data)
        path = info.get('data', {}).get('path')
        value = info.get('data', {}).get('dp', {}).get('value')

        print(f"Received subscription event: {path} {value}")

        if path == "Vehicle.Speed":
            IC_Page.Speed_monitor.display(int(IC_Page.Speed_slider.value()))
            IC_Page.Speed_slider.setValue(int(value))

        if path == "Vehicle.Powertrain.CombustionEngine.Speed":
            IC_Page.RPM_slider.setValue(int(value))
            IC_Page.RPM_monitor.display(int(IC_Page.RPM_slider.value()))

        if path == "Vehicle.Body.Lights.DirectionIndicator.Left.IsSignaling":
            IC_Page.leftIndicatorBtn.setChecked(bool(value))

        if path == "Vehicle.Body.Lights.DirectionIndicator.Right.IsSignaling":
            IC_Page.rightIndicatorBtn.setChecked(bool(value))

        if path == "Vehicle.Body.Lights.Hazard.IsSignaling":
            IC_Page.hazardBtn.setChecked(bool(value))

        if path == "Vehicle.Powertrain.FuelSystem.Level":
            IC_Page.fuelLevel_slider.setValue(int(value))

        if path == "Vehicle.Powertrain.CombustionEngine.ECT":
            IC_Page.coolantTemp_slider.setValue(int(value))

        if path == "Vehicle.Powertrain.Transmission.SelectedGear":
            if int(value) == 127:
                IC_Page.driveBtn.setChecked(True)
            elif int(value) == 126:
                IC_Page.parkBtn.setChecked(True)
            elif int(value) == -1:
                IC_Page.reverseBtn.setChecked(True)
            elif int(value) == 0:
                IC_Page.neutralBtn.setChecked(True)

        if path == "Vehicle.Cabin.HVAC.Station.Row1.Left.Temperature":
            HVAC_Page.left_temp.setValue(int(value))

        if path == "Vehicle.Cabin.HVAC.Station.Row1.Left.FanSpeed":
            HVAC_Page.left_fan.setValue(int(value))

        if path == "Vehicle.Cabin.HVAC.Station.Row1.Right.Temperature":
            HVAC_Page.right_temp.setValue(int(value))

        if path == "Vehicle.Cabin.HVAC.Station.Row1.Right.FanSpeed":
            HVAC_Page.right_fan.setValue(int(value))


class FaderWidget(QWidget):
    def __init__(self, old_widget, new_widget):
        super().__init__(new_widget)

        self.old_widget = old_widget
        self.new_widget = new_widget

        self.effect = QGraphicsOpacityEffect()
        self.new_widget.setGraphicsEffect(self.effect)

        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.finished.connect(self.close)

        self.animate()

    def animate(self):
        self.animation.start()

    def close(self):
        self.old_widget.close()
        self.new_widget.show()
        super().close()
