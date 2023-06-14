import os
import sys
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QSlider, QLCDNumber, QPushButton

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


class ICWidget(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.set_instance()

        self.IC = IC_Paths()

        self.Speed_slider = self.findChild(QSlider, "Speed_slider")
        self.Speed_monitor = self.findChild(QLCDNumber, "Speed_monitor")
        self.RPM_slider = self.findChild(QSlider, "RPM_slider")
        self.RPM_monitor = self.findChild(QLCDNumber, "RPM_monitor")
        self.leftIndicatorBtn = self.findChild(QPushButton, "leftIndicatorBtn")
        self.rightIndicatorBtn = self.findChild(
            QPushButton, "rightIndicatorBtn")

        self.Speed_slider.valueChanged.connect(self.update_Speed_monitor)
        self.Speed_slider.setMinimum(0)
        self.Speed_slider.setMaximum(240)

        self.RPM_slider.valueChanged.connect(self.update_RPM_monitor)
        self.RPM_slider.setMinimum(0)
        self.RPM_slider.setMaximum(8000)

        # make both buttons checkable
        self.leftIndicatorBtn.setCheckable(True)
        self.rightIndicatorBtn.setCheckable(True)

        self.leftIndicatorBtn.clicked.connect(self.leftIndicatorBtnClicked)
        self.rightIndicatorBtn.clicked.connect(self.rightIndicatorBtnClicked)

        # Create QTimer object
        self.timer = QtCore.QTimer()
        # Set interval to 100ms (10 times per second)
        self.timer.setInterval(1000)
        # Connect timeout signal to send_value function
        self.timer.timeout.connect(self.send_value)

        # Create QThread object
        self.thread = QtCore.QThread()
        # Move timer object to thread
        self.timer.moveToThread(self.thread)
        # Connect thread started signal to timer start slot
        self.thread.started.connect(self.timer.start)
        # Start thread
        self.thread.start()

    def set_instance(self):
        self.kuksa = kuksa_instance.KuksaClientSingleton.get_instance()
        self.client = self.kuksa.get_client()
        self.client.stop()
        self.client.start()

    def update_Speed_monitor(self):
        speed = int(self.Speed_slider.value())
        self.Speed_monitor.display(speed)

    def update_RPM_monitor(self):
        rpm = int(self.RPM_slider.value())
        self.RPM_monitor.display(rpm)

    def send_value(self):
        speed = int(self.Speed_slider.value())
        rpm = int(self.RPM_slider.value())

        try:
            # Send speed value to server
            # self.client.setValue(self.IC.speed, str(speed), 'value')
            # Send RPM value to server
            # self.client.setValue(self.IC.engineRPM, str(rpm), 'value')

            self.client.setValue(self.IC.speed, str(speed), 'value')
            self.client.setValue(self.IC.engineRPM, str(rpm), 'value')

        except Exception as e:
            print(e)

    def leftIndicatorBtnClicked(self):
        if self.leftIndicatorBtn.isChecked():
            self.leftIndicatorBtn.setStyleSheet( "background-color: green")
            self.client.setValue(self.IC.leftIndicator, "true")
        else:
            self.leftIndicatorBtn.setStyleSheet( "background-color: red")
            self.client.setValue(self.IC.leftIndicator, "false")

    def rightIndicatorBtnClicked(self):
        if self.rightIndicatorBtn.isChecked():
            self.rightIndicatorBtn.setStyleSheet( "background-color: green")
            self.client.setValue(self.IC.rightIndicator, "true")
        else:
            self.rightIndicatorBtn.setStyleSheet( "background-color: red")
            self.client.setValue(self.IC.rightIndicator, "false")


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = ICWidget()
    w.show()
    sys.exit(app.exec_())
