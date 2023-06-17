import os
import sys
import time
import json
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLineEdit, QPushButton, QLabel

current_dir = os.path.dirname(os.path.abspath(__file__))

# ========================================

sys.path.append(os.path.dirname(current_dir))

import extras.Kuksa_Instance as kuksa_instance

Form, Base = uic.loadUiType(os.path.join(current_dir, "../ui/Settings_Window.ui"))

# ========================================

class settings(Base, Form):
	def __init__(self, parent=None):
		super(self.__class__, self).__init__(parent)
		self.setupUi(self)

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

		self.refreshStatus()
		self.show()
		
	def set_instance(self):
		self.kuksa = kuksa_instance.KuksaClientSingleton.get_instance()
		self.client = self.kuksa.get_client()
		
		self.config = self.kuksa.get_config()
		self.token = self.kuksa.get_token()

		self.IPAddrInput.setText(self.config["ip"])
		self.tokenPathInput.setText(self.token)

		time.sleep(2)
		self.refreshStatus()

	def refreshStatus(self):
		try:
			if(self.client is None):
				self.connectionStatus.setText('Not Connected')
				self.connectionLogo.setStyleSheet("background-color: red")

			if(self.client.checkConnection() == True):
				self.connectionStatus.setText('Connected')
				self.connectionLogo.setStyleSheet("background-color: green")
				self.client.start()
			
			if(self.client.checkConnection() == False):
				self.client.stop()
				self.connectionStatus.setText('Disconnected')
				self.connectionLogo.setStyleSheet("background-color: yellow")			
		except:
			pass

	def reconnectClient(self):
		try:
			self.config["ip"] = self.IPAddrInput.text()
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