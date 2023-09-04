from main import *
from PyQt5 import QtCore
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QEasingCurve
from PyQt5.QtWidgets import QGraphicsOpacityEffect

class UI_Handeler(MainWindow):
    def Hide_Navbar(self, bool_arg):
        height = self.BottomMenuSubContainer.height()
        heightExtended = 75 if bool_arg else 0

        self.animation = QPropertyAnimation(self.BottomMenuSubContainer, b"minimumHeight")
        self.animation.setDuration(400)
        self.animation.setStartValue(height)
        self.animation.setEndValue(heightExtended)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    # animate switching pages for QstackedWidget with the animation being a fade in and out
    def animateSwitch(self, index):
        self.fader_widget = FaderWidget(self.stackedWidget.currentWidget(), self.stackedWidget.widget(index))
        self.stackedWidget.setCurrentIndex(index)

    # add window resizing to the UI
    def toggleMaximized(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    # move the window by dragging the header
    def moveWindow(self, event):

        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.clickPosition)
            self.clickPosition = event.globalPos()
            event.accept()

    # get the position of the mouse when clicked
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
        event.accept()

    # get the position of the mouse when released
    def mouseReleaseEvent(self, event):
        self.clickPosition = None
        event.accept()

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