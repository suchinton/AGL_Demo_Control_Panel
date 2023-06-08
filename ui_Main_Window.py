# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Main_WindowRdYfVZ.ui'
##
## Created by: Qt User Interface Compiler version 5.15.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import res_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.NonModal)
        MainWindow.resize(913, 664)
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Active, QPalette.Button, brush)
        palette.setBrush(QPalette.Active, QPalette.Light, brush)
        palette.setBrush(QPalette.Active, QPalette.Midlight, brush)
        brush1 = QBrush(QColor(127, 127, 127, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Dark, brush1)
        brush2 = QBrush(QColor(170, 170, 170, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Mid, brush2)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        palette.setBrush(QPalette.Active, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        brush3 = QBrush(QColor(0, 0, 0, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Shadow, brush3)
        palette.setBrush(QPalette.Active, QPalette.AlternateBase, brush)
        brush4 = QBrush(QColor(255, 255, 220, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ToolTipBase, brush4)
        palette.setBrush(QPalette.Active, QPalette.ToolTipText, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush)
#endif
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Light, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Midlight, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Dark, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Mid, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Shadow, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush)
#endif
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Light, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Midlight, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Dark, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Mid, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette.setBrush(QPalette.Disabled, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Shadow, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush)
#endif
        MainWindow.setPalette(palette)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(u"*{\n"
"	border: none;\n"
"	background-color: transparent;\n"
"	background: none;\n"
"	padding: 0;\n"
"	margin: 0;\n"
"	color: #fff;\n"
"}\n"
"\n"
"#centralwidget{\n"
"	background-color: rgb(29, 29, 29);\n"
"}\n"
"\n"
"#leftMenuSubContainer{\n"
"	border-radius: 10px;\n"
"	background-color: rgb(48, 59, 59);\n"
"}\n"
"\n"
"#leftMenuSubContainer QPushButton{\n"
"	background-color: rgb(107, 127, 124);\n"
"	text-align: left;\n"
"	padding: 5px 10px;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"#headerContainer{\n"
"	border-radius: 10px;\n"
"	background-color: rgb(48, 59, 59);\n"
"} \n"
"")
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QTabWidget.Rounded)
        MainWindow.setDockOptions(QMainWindow.AllowTabbedDocks|QMainWindow.AnimatedDocks)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.action127_0_0_1 = QAction(MainWindow)
        self.action127_0_0_1.setObjectName(u"action127_0_0_1")
        self.actionOther = QAction(MainWindow)
        self.actionOther.setObjectName(u"actionOther")
        self.actionDefault_127_0_0_1 = QAction(MainWindow)
        self.actionDefault_127_0_0_1.setObjectName(u"actionDefault_127_0_0_1")
        self.actionDefault_127_0_0_1.setCheckable(True)
        self.actionOther_2 = QAction(MainWindow)
        self.actionOther_2.setObjectName(u"actionOther_2")
        self.actionOther_2.setCheckable(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setAutoFillBackground(False)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.leftMenuContainer = QWidget(self.centralwidget)
        self.leftMenuContainer.setObjectName(u"leftMenuContainer")
        self.leftMenuContainer.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(self.leftMenuContainer)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.leftMenuSubContainer = QWidget(self.leftMenuContainer)
        self.leftMenuSubContainer.setObjectName(u"leftMenuSubContainer")
        self.verticalLayout_3 = QVBoxLayout(self.leftMenuSubContainer)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frame = QFrame(self.leftMenuSubContainer)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.menuButton = QPushButton(self.frame)
        self.menuButton.setObjectName(u"menuButton")
        icon = QIcon()
        icon.addFile(u":/icons/feather/menu.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.menuButton.setIcon(icon)

        self.horizontalLayout.addWidget(self.menuButton)


        self.verticalLayout_3.addWidget(self.frame, 0, Qt.AlignTop)

        self.frame_2 = QFrame(self.leftMenuSubContainer)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.icButton = QPushButton(self.frame_2)
        self.icButton.setObjectName(u"icButton")
        icon1 = QIcon()
        icon1.addFile(u":/icons/feather/disc.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.icButton.setIcon(icon1)

        self.verticalLayout_4.addWidget(self.icButton)

        self.hvacButton = QPushButton(self.frame_2)
        self.hvacButton.setObjectName(u"hvacButton")
        icon2 = QIcon()
        icon2.addFile(u":/icons/feather/wind.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.hvacButton.setIcon(icon2)

        self.verticalLayout_4.addWidget(self.hvacButton)

        self.newButton = QPushButton(self.frame_2)
        self.newButton.setObjectName(u"newButton")
        icon3 = QIcon()
        icon3.addFile(u":/icons/feather/plus.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.newButton.setIcon(icon3)

        self.verticalLayout_4.addWidget(self.newButton)


        self.verticalLayout_3.addWidget(self.frame_2, 0, Qt.AlignTop)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.frame_3 = QFrame(self.leftMenuSubContainer)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.configureButton = QPushButton(self.frame_3)
        self.configureButton.setObjectName(u"configureButton")
        icon4 = QIcon()
        icon4.addFile(u":/icons/feather/settings.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.configureButton.setIcon(icon4)

        self.verticalLayout_5.addWidget(self.configureButton)


        self.verticalLayout_3.addWidget(self.frame_3, 0, Qt.AlignBottom)


        self.verticalLayout_2.addWidget(self.leftMenuSubContainer)


        self.gridLayout.addWidget(self.leftMenuContainer, 0, 0, 2, 1, Qt.AlignLeft)

        self.mainContainer = QWidget(self.centralwidget)
        self.mainContainer.setObjectName(u"mainContainer")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.mainContainer.sizePolicy().hasHeightForWidth())
        self.mainContainer.setSizePolicy(sizePolicy1)
        self.verticalLayout_6 = QVBoxLayout(self.mainContainer)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.headerContainer = QWidget(self.mainContainer)
        self.headerContainer.setObjectName(u"headerContainer")
        self.horizontalLayout_3 = QHBoxLayout(self.headerContainer)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.headerContainer)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.aglLogo = QLabel(self.frame_4)
        self.aglLogo.setObjectName(u"aglLogo")
        self.aglLogo.setMaximumSize(QSize(90, 55))
        self.aglLogo.setPixmap(QPixmap(u":/Images/Images/logo_agl.png"))
        self.aglLogo.setScaledContents(True)

        self.horizontalLayout_4.addWidget(self.aglLogo)

        self.aglLabel = QLabel(self.frame_4)
        self.aglLabel.setObjectName(u"aglLabel")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.aglLabel.setFont(font)

        self.horizontalLayout_4.addWidget(self.aglLabel)


        self.horizontalLayout_3.addWidget(self.frame_4, 0, Qt.AlignLeft)

        self.frame_6 = QFrame(self.headerContainer)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 6, 0)
        self.pushButton_2 = QPushButton(self.frame_6)
        self.pushButton_2.setObjectName(u"pushButton_2")
        icon5 = QIcon()
        icon5.addFile(u":/icons/feather/minus.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_2.setIcon(icon5)

        self.horizontalLayout_2.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.frame_6)
        self.pushButton_3.setObjectName(u"pushButton_3")
        icon6 = QIcon()
        icon6.addFile(u":/icons/feather/square.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_3.setIcon(icon6)

        self.horizontalLayout_2.addWidget(self.pushButton_3)

        self.pushButton = QPushButton(self.frame_6)
        self.pushButton.setObjectName(u"pushButton")
        icon7 = QIcon()
        icon7.addFile(u":/icons/feather/x.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton.setIcon(icon7)

        self.horizontalLayout_2.addWidget(self.pushButton)


        self.horizontalLayout_3.addWidget(self.frame_6, 0, Qt.AlignRight|Qt.AlignVCenter)


        self.verticalLayout_6.addWidget(self.headerContainer, 0, Qt.AlignTop)

        self.mainBodyContent = QWidget(self.mainContainer)
        self.mainBodyContent.setObjectName(u"mainBodyContent")
        sizePolicy.setHeightForWidth(self.mainBodyContent.sizePolicy().hasHeightForWidth())
        self.mainBodyContent.setSizePolicy(sizePolicy)
        self.horizontalLayout_5 = QHBoxLayout(self.mainBodyContent)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.widget = QWidget(self.mainBodyContent)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_6 = QHBoxLayout(self.widget)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.stackedWidget = QStackedWidget(self.widget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.stackedWidget.addWidget(self.page_2)

        self.horizontalLayout_6.addWidget(self.stackedWidget)


        self.horizontalLayout_5.addWidget(self.widget)


        self.verticalLayout_6.addWidget(self.mainBodyContent)


        self.gridLayout.addWidget(self.mainContainer, 0, 2, 2, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action127_0_0_1.setText(QCoreApplication.translate("MainWindow", u"127.0.0.1", None))
        self.actionOther.setText(QCoreApplication.translate("MainWindow", u"Other", None))
        self.actionDefault_127_0_0_1.setText(QCoreApplication.translate("MainWindow", u"Default: 127.0.0.1", None))
        self.actionOther_2.setText(QCoreApplication.translate("MainWindow", u"Other", None))
        self.menuButton.setText("")
        self.icButton.setText(QCoreApplication.translate("MainWindow", u"Instrument Cluster", None))
        self.hvacButton.setText(QCoreApplication.translate("MainWindow", u"HVAC", None))
        self.newButton.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.configureButton.setText(QCoreApplication.translate("MainWindow", u"Configure", None))
        self.aglLogo.setText("")
        self.aglLabel.setText(QCoreApplication.translate("MainWindow", u"AGL Kuksa Wizard", None))
        self.pushButton_2.setText("")
        self.pushButton_3.setText("")
        self.pushButton.setText("")
    # retranslateUi

