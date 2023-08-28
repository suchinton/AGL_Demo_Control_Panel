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

current_dir = os.path.dirname(os.path.abspath(__file__))

# ========================================

sys.path.append(os.path.dirname(current_dir))

import extras.Kuksa_Instance as kuksa_instance

Form, Base = uic.loadUiType(os.path.join(
    current_dir, "../ui/Settings_Window.ui"))

# ========================================

Steering_Signal_Type = "Kuksa"

class settings(Base, Form):    
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)

        self.SSL_toggle = AnimatedToggle(
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
        self.tokenPathInput = self.findChild(QLineEdit, "tokenPathInput")

        self.reconnectBtn = self.findChild(QPushButton, "reconnectBtn")
        self.refreshBtn = self.findChild(QPushButton, "refreshBtn")
        self.startClientBtn = self.findChild(QPushButton, "startClientBtn")

        self.startClientBtn.clicked.connect(self.set_instance)
        self.reconnectBtn.clicked.connect(self.reconnectClient)
        self.refreshBtn.clicked.connect(self.refreshStatus)
        self.SSL_toggle.clicked.connect(self.toggleSSL)
        self.CAN_Kuksa_toggle.clicked.connect(self.toggle_CAN_Kuksa)
    
        Frame3 = self.findChild(QWidget, "frame_3")
        layout = Frame3.layout()
        
        layout.replaceWidget(self.place_holder_toggle_1, self.SSL_toggle)
        layout.replaceWidget(self.place_holder_toggle_2, self.CAN_Kuksa_toggle)
        
        self.place_holder_toggle_1.deleteLater()
        self.place_holder_toggle_2.deleteLater()

        self.refreshStatus()
        #self.show()

    def toggleSSL(self):
        self.config["insecure"] = self.SSL_toggle.isChecked()
        print(self.config)

    def toggle_CAN_Kuksa(self):
        global Steering_Signal_Type
        if (self.CAN_Kuksa_toggle.isChecked()):
            Steering_Signal_Type = "CAN"
        else:
            Steering_Signal_Type = "Kuksa"

    def set_instance(self):
        self.kuksa = kuksa_instance.KuksaClientSingleton.get_instance()
        self.client = self.kuksa.get_client()

        self.config = self.kuksa.get_config()
        self.token = self.kuksa.get_token()

        self.IPAddrInput.setText(self.config["ip"])
        self.SSL_toggle.setChecked(self.config["insecure"])
        self.tokenPathInput.setText(self.token)

        time.sleep(2)

        if (self.client is None):
            self.connectionStatus.setText('Not Connected')
            self.connectionLogo.setStyleSheet("background-color: red")

        self.refreshStatus()

    def refreshStatus(self):
        try:
            if (self.client is None):
                self.connectionStatus.setText('Not Connected')
                self.connectionLogo.setStyleSheet("background-color: red")
                return None

            if (self.client.checkConnection() == True):
                self.connectionStatus.setText('Connected')
                self.connectionLogo.setPixmap(":/icons/feather/check-circle.svg")
                self.connectionLogo.setStyleSheet("background-color: green")
                self.client.start()
                return True

            if (self.client.checkConnection() == False):
                self.client.stop()
                self.connectionStatus.setText('Disconnected')
                self.connectionLogo.setStyleSheet("background-color: yellow")
                return False
        except:
            pass

    def reconnectClient(self):
        try:
            self.config["ip"] = self.IPAddrInput.text()
            self.config["insecure"] = self.SSL_toggle.isChecked()
            self.token = self.tokenPathInput.text()
            self.client = self.kuksa.reconnect_client(self.config, self.token)
            self.client.start()
            self.refreshStatus()
        except Exception as e:
            print(e)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = settings()
    w.show()
    sys.exit(app.exec_())
