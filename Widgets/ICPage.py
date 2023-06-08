import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication


current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = uic.loadUiType(os.path.join(current_dir, "../ui/IC.ui"))

class ICWidget(Base, Form):
	def __init__(self, parent=None):
		super(self.__class__, self).__init__(parent)
		self.setupUi(self)


if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	w = ICWidget()
	w.show()
	sys.exit(app.exec_())