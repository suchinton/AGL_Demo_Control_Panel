#   Copyright 2023 Suchinton Chakravarty
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


import os
import sys
import time
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLineEdit, QPushButton, QLabel
from qtwidgets import AnimatedToggle
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThread
from PyQt5 import QtGui
import logging

current_dir = os.path.dirname(os.path.abspath(__file__))

# ========================================

sys.path.append(os.path.dirname(current_dir))

import extras.Kuksa_Instance as kuksa_instance

Form, Base = uic.loadUiType(os.path.join(
    current_dir, "../ui/Settings_Window.ui"))

# ========================================

Steering_Signal_Type = "Kuksa"

class settings(Base, Form):
    """
    A class representing the settings widget of the AGL Demo Control Panel.

    Attributes:
    - SSL_toggle: An AnimatedToggle object representing the SSL toggle button.
    - CAN_Kuksa_toggle: An AnimatedToggle object representing the CAN/Kuksa toggle button.
    - connectionStatus: A QLabel object representing the connection status label.
    - connectionLogo: A QLabel object representing the connection logo label.
    - IPAddrInput: A QLineEdit object representing the IP address input field.
    - reconnectBtn: A QPushButton object representing the reconnect button.
    - refreshBtn: A QPushButton object representing the refresh button.
    - startClientBtn: A QPushButton object representing the start client button.
    """
    
    def __init__(self, parent=None):
        """
        Initializes the settings widget of the AGL Demo Control Panel.
        """
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        
        default_config = kuksa_instance.get_default_config()
        
        self.SSL_toggle = AnimatedToggle(
            checked_color="#4BD7D6",
            pulse_checked_color="#00ffff",
        )

        self.Protocol_toggle = AnimatedToggle(
            checked_color="#4BD7D6",
            pulse_checked_color="#00ffff"
        )
        
        self.CAN_Kuksa_toggle = AnimatedToggle(
            checked_color="#4BD7D6",
            pulse_checked_color="#00ffff"
        )

        self.connectionStatus = self.findChild(QLabel, "connectionStatus")
        self.connectionLogo = self.findChild(QLabel, "connectionLogo")

        self.IPAddrInput = self.findChild(QLineEdit, "IPAddrInput")
        self.PortInput = self.findChild(QLineEdit, "PortInput")

        self.reconnectBtn = self.findChild(QPushButton, "reconnectBtn")
        self.startClientBtn = self.findChild(QPushButton, "startClientBtn")

        self.startClientBtn.clicked.connect(self.set_instance)
        self.reconnectBtn.clicked.connect(self.reconnectClient)
        self.SSL_toggle.clicked.connect(self.toggleSSL)
        self.CAN_Kuksa_toggle.clicked.connect(self.toggle_CAN_Kuksa)
    
        Frame_GS = self.findChild(QWidget, "frame_general_settings")
        Frame_PS = self.findChild(QWidget, "frame_page_settings")
        GS_layout = Frame_GS.layout()
        PS_layout = Frame_PS.layout()
        
        GS_layout.replaceWidget(self.place_holder_toggle_1, self.SSL_toggle)
        GS_layout.replaceWidget(self.place_holder_toggle_2, self.Protocol_toggle)
        PS_layout.replaceWidget(self.place_holder_toggle_3, self.CAN_Kuksa_toggle)
        
        self.place_holder_toggle_1.deleteLater()
        self.place_holder_toggle_2.deleteLater()
        self.place_holder_toggle_3.deleteLater()

        self.IPAddrInput.setText(default_config["ip"])
        self.PortInput.setText(default_config["port"])
        self.SSL_toggle.setChecked(not default_config["insecure"])
        self.Protocol_toggle.setChecked(default_config["protocol"] == 'grpc')

        # self.refreshStatus()

    def toggleSSL(self):
        """
        Toggles the SSL connection.
        """
        self.kuksa_config["insecure"] = not self.SSL_toggle.isChecked()
        print(self.kuksa_config)

    def toggle_CAN_Kuksa(self):
        """
        Toggles the CAN/Kuksa connection.
        """
        global Steering_Signal_Type
        if (self.CAN_Kuksa_toggle.isChecked()):
            Steering_Signal_Type = "CAN"
        else:
            Steering_Signal_Type = "Kuksa"

    def get_protocol(self):
        if (not self.Protocol_toggle.isChecked()):
            return "ws"
        else:
            return "grpc"

    def set_instance(self):
        """
        Sets the instance of the Kuksa client.
        """
        self.kuksa = kuksa_instance.KuksaClientSingleton.instance()
        self.kuksa.reconnect(self.make_new_config())
        self.client = self.kuksa.get_client()

        time.sleep(2)

        if (self.client is None):
            self.connectionStatus.setText('Not Connected')
            self.connectionLogo.setStyleSheet("background-color: red")

        self.refreshStatus()

    def refreshStatus(self):
        """
        Refreshes the connection status.
        """
        try:
            if (self.client is None):
                self.connectionStatus.setText('Not Connected')
                self.connectionLogo.setStyleSheet("background-color: red")
                self.connectionLogo.setPixmap(QtGui.QPixmap(":/Carbon_Icons/carbon_icons/connection-signal--off.svg"))
                return None

            if (self.client.checkConnection() == True):
                self.connectionStatus.setText('Connected')
                self.connectionLogo.setStyleSheet("background-color: green")
                self.connectionLogo.setPixmap(QtGui.QPixmap(":/Carbon_Icons/carbon_icons/connection-signal.svg"))
                self.client.start()
                return True

            if (self.client.checkConnection() == False):
                self.client.stop()
                self.connectionStatus.setText('Disconnected')
                self.connectionLogo.setStyleSheet("background-color: yellow")
                self.connectionLogo.setPixmap(QtGui.QPixmap(":/Carbon_Icons/carbon_icons/connection-signal--off.svg"))
                return False
        except:
            pass

    def reconnectClient(self):
        """
        Reconnects the client.
        """
        try:
            config = self.make_new_config()
            self.client = self.kuksa.reconnect(config)
            self.client.start()
            self.refreshStatus()

            self.refreshThread = RefreshThread(self)
            self.refreshThread.start()

        except Exception as e:
            logging.error(e)

    def make_new_config(self):
        """
        Makes a new configuration using fields in the settings widget.
        """
        new_config = {}
        new_config["ip"] = self.IPAddrInput.text()
        new_config["port"] = self.PortInput.text()
        new_config["protocol"] = self.get_protocol()
        new_config["insecure"] = not self.SSL_toggle.isChecked()
        new_config["cacertificate"] = None
        new_config["tls_server_name"] = None
        return new_config

class RefreshThread(QThread):
    def __init__(self, settings):
        QThread.__init__(self)
        self.settings = settings

    def run(self):
        time.sleep(2)
        self.settings.refreshStatus()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = settings()
    w.show()
    sys.exit(app.exec_())
