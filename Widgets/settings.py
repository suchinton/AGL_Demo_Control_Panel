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

from extras import config
import extras.Kuksa_Instance as kuksa_instance

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
import can

current_dir = os.path.dirname(os.path.abspath(__file__))

# ========================================

sys.path.append(os.path.dirname(current_dir))


Form, Base = uic.loadUiType(os.path.join(
    current_dir, "../ui/Settings_Window.ui"))

# ========================================

# Global Variables
Steering_Signal_Type = "Kuksa"
Protocol = None

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
        self.client = None

        self.SSL_toggle = create_animated_toggle()
        self.Protocol_toggle = create_animated_toggle()
        self.CAN_Kuksa_toggle = create_animated_toggle()

        self.connectionStatus = self.findChild(QLabel, "connectionStatus")
        self.connectionLogo = self.findChild(QLabel, "connectionLogo")

        list_of_configs = config.get_list_configs()
        default_config_name = config.get_default_config()

        self.List_Configs_ComboBox = self.findChild(
            QComboBox, "List_Configs_ComboBox")
        self.List_Configs_ComboBox.setItemDelegate(QStyledItemDelegate())
        self.List_Configs_ComboBox.addItems(list_of_configs)
        self.List_Configs_ComboBox.setCurrentText(default_config_name)
        self.List_Configs_ComboBox.currentTextChanged.connect(
            lambda: self.set_settings(self.List_Configs_ComboBox.currentText()))

        self.IPAddrInput = self.findChild(QLineEdit, "IPAddrInput")
        self.PortInput = self.findChild(QLineEdit, "PortInput")
        self.TLS_Server_Name = self.findChild(QLineEdit, "TLS_Server_Name")
        self.Auth_Token = self.findChild(QLineEdit, "Auth_Token")
        self.CA_File = self.findChild(QLineEdit, "CA_File")

        self.reconnectBtn = self.findChild(QPushButton, "reconnectBtn")
        self.startClientBtn = self.findChild(QPushButton, "startClientBtn")
        self.startClientBtn.setCheckable(True)
        self.startClientBtn.setStyleSheet("border: 1px solid green;")

        self.Hide_IC = self.findChild(QPushButton, "Hide_IC")
        self.Hide_HVAC = self.findChild(QPushButton, "Hide_HVAC")
        self.Hide_HUD = self.findChild(QPushButton, "Hide_HUD")

        self.startClientBtn.clicked.connect(self.start_stop_client)
        self.reconnectBtn.clicked.connect(self.reconnectClient)
        self.SSL_toggle.clicked.connect(self.toggleSSL)
        self.CAN_Kuksa_toggle.clicked.connect(self.toggle_CAN_Kuksa)

        # self.Hide_IC.clicked.connect(lambda: self.Hide_Pages(self, 1))
        # self.Hide_HUD.clicked.connect(lambda: self.Hide_Pages(self, 2))
        # self.Hide_HVAC.clicked.connect(lambda: self.Hide_Pages(self, 3))

        Frame_GS = self.findChild(QWidget, "frame_general_settings")
        Frame_PS = self.findChild(QWidget, "frame_page_settings")
        GS_layout = Frame_GS.layout()
        PS_layout = Frame_PS.layout()

        GS_layout.replaceWidget(self.place_holder_toggle_1, self.SSL_toggle)
        GS_layout.replaceWidget(
            self.place_holder_toggle_2, self.Protocol_toggle)
        PS_layout.replaceWidget(
            self.place_holder_toggle_3, self.CAN_Kuksa_toggle)

        self.place_holder_toggle_1.deleteLater()
        self.place_holder_toggle_2.deleteLater()
        self.place_holder_toggle_3.deleteLater()

        self.set_settings(default_config_name)

    def start_stop_client(self):
        if self.startClientBtn.isChecked():
            self.set_instance()
        elif self.client is not None:
            self.client.stop()

        self.refreshThread = RefreshThread(self)
        self.refreshThread.start()

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
            # check if can0 is available
            try:
                can_bus = can.interface.Bus(
                    channel='can0', bustype='socketcan_native')
                can_bus.shutdown()
                Steering_Signal_Type = "CAN"
            except:
                self.CAN_Kuksa_toggle.setChecked(False)
                logging.error("CAN Bus not available")
        else:
            Steering_Signal_Type = "Kuksa"

    def get_protocol(self):
        global Protocol
        if (not self.Protocol_toggle.isChecked()):
            Protocol = "ws"
            return "ws"
        else:
            Protocol = "grpc"
            return "grpc"

    def set_instance(self):
        """
        Sets the instance of the Kuksa client.
        """
        self.kuksa = kuksa_instance.KuksaClientSingleton.instance()
        new_config = self.make_new_config()
        if (new_config is None):
            logging.error("Invalid configuration")
        else:
            self.kuksa.reconnect(new_config, self.kuksa_token)
            self.client = self.kuksa.get_client()

    def refreshStatus(self):
        """
        Refreshes the connection status.
        """
        try:
            if (self.client is None):
                self.connectionStatus.setText('Not Connected')
                self.connectionLogo.setStyleSheet("background-color: red")
                self.connectionLogo.setPixmap(QtGui.QPixmap(
                    ":/Carbon_Icons/carbon_icons/connection-signal--off.svg"))

                self.startClientBtn.setStyleSheet("border: 1px solid green;")
                self.startClientBtn.setIcon(QtGui.QIcon(
                    ":/Carbon_Icons/carbon_icons/play.svg"))
                self.startClientBtn.setText("Start Client")
                self.startClientBtn.setChecked(False)
                return None

            if (self.client.checkConnection() == True):
                self.connectionStatus.setText('Connected')
                self.connectionLogo.setStyleSheet("background-color: green")
                self.connectionLogo.setPixmap(QtGui.QPixmap(
                    ":/Carbon_Icons/carbon_icons/connection-signal.svg"))

                self.startClientBtn.setStyleSheet("border: 1px solid red;")
                self.startClientBtn.setIcon(QtGui.QIcon(
                    ":/Carbon_Icons/carbon_icons/stop.svg"))
                self.startClientBtn.setText("Stop Client")
                self.startClientBtn.setChecked(True)
                self.client.start()
                return True

            if (self.client.checkConnection() == False):
                self.client.stop()
                self.connectionStatus.setText('Disconnected')
                self.connectionLogo.setStyleSheet("background-color: yellow")
                self.connectionLogo.setPixmap(QtGui.QPixmap(
                    ":/Carbon_Icons/carbon_icons/connection-signal--off.svg"))

                self.startClientBtn.setStyleSheet("border: 1px solid green;")
                self.startClientBtn.setIcon(QtGui.QIcon(
                    ":/Carbon_Icons/carbon_icons/play.svg"))
                self.startClientBtn.setText("Start Client")
                self.startClientBtn.setChecked(False)
                return False
        except:
            pass

    def reconnectClient(self):
        """
        Reconnects the client.
        """
        if (self.client is not None):
            try:
                self.client.stop()
                self.client = self.kuksa.reconnect(
                    self.make_new_config(), self.kuksa_token)

                self.refreshThread = RefreshThread(self)
                self.refreshThread.start()

            except Exception as e:
                logging.error(e)
        else:
            self.set_instance()
    
            self.refreshThread = RefreshThread(self)
            self.refreshThread.start()

    def make_new_config(self):
        """
        Makes a new configuration using fields in the settings widget.
        """

        def validate_and_set_style(self, widget, key=None):
            text = widget.text()
            if text:
                if os.path.exists(text):
                    widget.setStyleSheet(
                        "border: 1px solid #4BD7D6 ; /* light blue */")
                    if key:
                        new_config[key] = text
                    else:
                        self.kuksa_token = text
                else:
                    widget.setStyleSheet("border: 1px solid red;")
                    return None

        new_config = {}
        new_config["ip"] = self.IPAddrInput.text()
        new_config["port"] = self.PortInput.text()
        new_config["protocol"] = self.get_protocol()
        new_config["insecure"] = not self.SSL_toggle.isChecked()
        new_config["tls_server_name"] = self.TLS_Server_Name.text(
        ) if self.Protocol_toggle.isChecked() else None
        validate_and_set_style(self, self.CA_File, "cacertificate")
        validate_and_set_style(self, self.Auth_Token)

        config.save_session_config(
            new_config, self.kuksa_token, self.CA_File.text())

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
        self.Protocol_toggle.setChecked(
            self.kuksa_config["protocol"] == 'grpc')
        self.CA_File.setText(self.kuksa_config["cacertificate"])
        self.TLS_Server_Name.setText(
            self.kuksa_config["tls_server_name"] if self.kuksa_config["tls_server_name"] is not None else "")
        self.Auth_Token.setText(self.kuksa_token)

    def Hide_Pages(self):
        pass


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
