from main import *
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import QTimeLine
from PyQt5.QtWidgets import QWidget, QStackedWidget, QPushButton
from functools import partial

class UI_Handeler(MainWindow):
    def toggleNavigationBar(self, maxWidth, enable):
        if enable:
            width = self.leftMenuSubContainer.width()
            maxExtend = maxWidth
            standard = 80

            if width == 80:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            self.animation = QPropertyAnimation(self.leftMenuSubContainer, b"minimumWidth")
            self.animation.setDuration(400)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
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
        QWidget.__init__(self, new_widget)    
        self.old_pixmap = QPixmap(new_widget.size())
        old_widget.render(self.old_pixmap)
        self.pixmap_opacity = 1.0  
        self.timeline = QTimeLine()
        self.timeline.valueChanged.connect(self.animate)
        self.timeline.finished.connect(self.close)
        self.timeline.setDuration(250)
        self.timeline.start()  
        self.resize(new_widget.size())
        self.show()
    
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setOpacity(self.pixmap_opacity)
        painter.drawPixmap(0, 0, self.old_pixmap)
        painter.end()
    
    def animate(self, value):
        self.pixmap_opacity = 1.0 - value
        self.repaint()