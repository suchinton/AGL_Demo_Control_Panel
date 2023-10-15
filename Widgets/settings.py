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
from PyQt5.QtWidgets import QApplication, QLineEdit, QPushButton, QLabel, QComboBox, QStyledItemDelegate
from qtwidgets import AnimatedToggle
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThread
from PyQt5 import QtGui
import logging

current_dir = os.path.dirname(os.path.abspath(__file__))

# ========================================

sys.path.append(os.path.dirname(current_dir))

import extras.Kuksa_Instance as kuksa_instance
from extras import config

Form, Base = uic.loadUiType(os.path.join(
    current_dir, "../ui/Settings_Window.ui"))

# ========================================

Steering_Signal_Type = "Kuksa"

def create_animated_toggle():
    return AnimatedToggle(
        checked_color="#4BD7D6",
        pulse_checked_color="#00ffff",
    )

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
        
        self.SSL_toggle = create_animated_toggle()
        self.Protocol_toggle = create_animated_toggle()
        self.AGL_CAFile_toggle = create_animated_toggle()
        self.CAN_Kuksa_toggle = create_animated_toggle()

        self.connectionStatus = self.findChild(QLabel, "connectionStatus")
        self.connectionLogo = self.findChild(QLabel, "connectionLogo")

        list_of_configs = config.get_list_configs()
        default_config_name = config.get_default_config()

        self.List_Configs_ComboBox = self.findChild(QComboBox, "List_Configs_ComboBox")
        self.List_Configs_ComboBox.setItemDelegate(QStyledItemDelegate())
        self.List_Configs_ComboBox.addItems(list_of_configs)
        self.List_Configs_ComboBox.setCurrentText(default_config_name)
        self.List_Configs_ComboBox.currentTextChanged.connect(lambda: self.set_settings(self.List_Configs_ComboBox.currentText()))

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
        GS_layout.replaceWidget(self.place_holder_toggle_4, self.AGL_CAFile_toggle)
        PS_layout.replaceWidget(self.place_holder_toggle_3, self.CAN_Kuksa_toggle)
        
        self.place_holder_toggle_1.deleteLater()
        self.place_holder_toggle_2.deleteLater()
        self.place_holder_toggle_3.deleteLater()
        self.place_holder_toggle_4.deleteLater()

        self.set_settings(default_config_name)

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
        self.kuksa.reconnect(self.make_new_config(), self.kuksa_token)
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
        if (self.client is not None):
            try:
                config = self.make_new_config()
                self.client.stop()
                self.client = self.kuksa.reconnect(config, self.kuksa_token)
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
        if self.AGL_CAFile_toggle.isChecked():
            new_config["cacertificate"] = config.CA
        new_config["tls_server_name"] = "Server" if self.Protocol_toggle.isChecked() else None
        return new_config
    
    def set_settings(self, config_name):
        """
        Reloads the parameters of settings widget.
        """
        new_config = config.select_config(config_name)
        self.kuksa_config_name = new_config[0]
        self.kuksa_config = new_config[1]
        self.kuksa_token = new_config[2]

        self.IPAddrInput.setText(self.kuksa_config["ip"])
        self.PortInput.setText(self.kuksa_config["port"])
        self.SSL_toggle.setChecked(not self.kuksa_config["insecure"])
        self.Protocol_toggle.setChecked(self.kuksa_config["protocol"] == 'grpc')
        self.AGL_CAFile_toggle.setChecked(self.kuksa_config["cacertificate"])

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
