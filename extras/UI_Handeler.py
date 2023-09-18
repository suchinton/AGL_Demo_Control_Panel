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
from PyQt5.QtWidgets import QDesktopWidget
import logging
import json

from . import Kuksa_Instance as kuksa_instance

# Global variables
subscribed = False
should_execute_callback = True

class UI_Handeler(MainWindow):
    """
    This class handles the UI of the AGL Demo Control Panel. It contains methods for hiding the navbar, animating page switches,
    toggling window maximization, moving the window by dragging the header, setting the Kuksa client instance, subscribing to VSS signals,
    and handling VSS signal callbacks.
    """
    def Hide_Navbar(self, bool_arg):
        """
        This method hides the navbar by animating its height to 0 if bool_arg is False, or to 75 if bool_arg is True.

        Args:
        - bool_arg (bool): A boolean value that determines whether the navbar should be hidden or not.
        """
        height = self.BottomMenuSubContainer.height()
        heightExtended = 75 if bool_arg else 0

        self.animation = QPropertyAnimation(self.BottomMenuSubContainer, b"minimumHeight")
        self.animation.setDuration(400)
        self.animation.setStartValue(height)
        self.animation.setEndValue(heightExtended)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    def animateSwitch(self, index):
        """
        This method animates the switch between pages in the QStackedWidget by fading out the current widget and fading in the new widget.

        Args:
        - index (int): The index of the widget to switch to.
        """
        self.fader_widget = FaderWidget(self.stackedWidget.currentWidget(), self.stackedWidget.widget(index))
        self.stackedWidget.setCurrentIndex(index)

    def toggleMaximized(self):
        """
        This method toggles the window between maximized and normal size.
        """
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def moveWindow(self, event):
        """
        This method moves the window by dragging the header.

        Args:
        - event (QEvent): The event object that contains information about the mouse event.
        """
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.clickPosition)
            self.clickPosition = event.globalPos()
            event.accept()

    def set_instance(self):
        """
        This method sets the Kuksa client instance and checks if there is a connection to Kuksa.

        Returns:
        - bool: True if there is a connection to Kuksa, False otherwise.
        """
        self.kuksa = kuksa_instance.KuksaClientSingleton.instance()
        self.client = self.kuksa.get_client()
        if self.client is not None and self.client.checkConnection():
            return True
        else:
            print("No connection to Kuksa")
            return False

    def subscribe_VSS_Signals(self):
        """
        This method subscribes to VSS signals and sets a callback function to handle the received data.
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

                # run the callback function on a se
                for signal in signals:
                    self.client.subscribe(signal, lambda data: UI_Handeler.VSS_callback(self,data), 'value')
                subscribed = True
            else:
                subscribed = False
                print("No connection to Kuksa")

    def VSS_callback(self,data):
        """
        This method handles the received VSS signal data and updates the UI accordingly.

        Args:
        - data (str): The received VSS signal data in JSON format.
        """
        global should_execute_callback
        if should_execute_callback is False:
            return
        IC_Page = self.stackedWidget.widget(1)
        HVAC_Page = self.stackedWidget.widget(2)

        info = json.loads(data)
        path = info.get('data', {}).get('path')
        value = info.get('data', {}).get('dp', {}).get('value')

        print(f"Received subscription event: {path} {value}")

        if path == "Vehicle.Speed":
            try:
                IC_Page.Speed_slider.setValue(int(value))
                IC_Page.Speed_monitor.display(int(IC_Page.Speed_slider.value()))
            except Exception as e:
                logging.error(f"Error setting speed value {e}")

        if path == "Vehicle.Powertrain.CombustionEngine.Speed":
            try:
                IC_Page.RPM_slider.setValue(int(value))
                IC_Page.RPM_monitor.display(int(IC_Page.RPM_slider.value()))
            except Exception as e:
                logging.error(f"Error setting RPM value {e}")

        if path == "Vehicle.Body.Lights.DirectionIndicator.Left.IsSignaling":
            try:
                IC_Page.leftIndicatorBtn.setChecked(bool(value))
            except Exception as e:
                logging.error(f"Error setting left signal value {e}")

        if path == "Vehicle.Body.Lights.DirectionIndicator.Right.IsSignaling":
            try:
                IC_Page.rightIndicatorBtn.setChecked(bool(value))
            except Exception as e:
                logging.error(f"Error setting right signal value {e}")

        if path == "Vehicle.Body.Lights.Hazard.IsSignaling":
            try:
                IC_Page.hazardBtn.setChecked(bool(value))
            except Exception as e:
                logging.error(f"Error setting hazard signal value {e}")

        if path == "Vehicle.Powertrain.FuelSystem.Level":  
            try:
                IC_Page.fuelLevel_slider.setValue(int(value))
            except Exception as e:
                logging.error(f"Error setting fuel level value {e}")

        if path == "Vehicle.Powertrain.CombustionEngine.ECT":
            try:
                IC_Page.coolantTemp_slider.setValue(int(value))
            except Exception as e:
                logging.error(f"Error setting coolant temp value {e}")

        if path == "Vehicle.Powertrain.Transmission.SelectedGear":
            try:
                if int(value) == 127:
                    IC_Page.driveBtn.setChecked(True)
                elif int(value) == 126:
                    IC_Page.parkBtn.setChecked(True)
                elif int(value) == -1:
                    IC_Page.reverseBtn.setChecked(True)
                elif int(value) == 0:
                    IC_Page.neutralBtn.setChecked(True)
            except Exception as e:
                logging.error(f"Error setting gear value {e}")

        if path == "Vehicle.Cabin.HVAC.Station.Row1.Left.Temperature":
            try:
                HVAC_Page.left_temp.setValue(int(value))
            except Exception as e:
                logging.error(f"Error setting left temp value {e}")

        if path == "Vehicle.Cabin.HVAC.Station.Row1.Left.FanSpeed":
            try:
                HVAC_Page.left_fan.setValue(int(value))
            except Exception as e:
                logging.error(f"Error setting left fan value {e}")

        if path == "Vehicle.Cabin.HVAC.Station.Row1.Right.Temperature":
            try:
                HVAC_Page.right_temp.setValue(int(value))
            except Exception as e:
                logging.error(f"Error setting right temp value {e}")

        if path == "Vehicle.Cabin.HVAC.Station.Row1.Right.FanSpeed":
            try:
                HVAC_Page.right_fan.setValue(int(value))
            except Exception as e:
                logging.error(f"Error setting right fan value {e}")


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