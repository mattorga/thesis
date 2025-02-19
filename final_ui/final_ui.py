# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'final.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSlider, QSpacerItem, QStackedWidget, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)
import resources_final_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.NonModal)
        MainWindow.resize(1280, 800)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1280, 800))
        MainWindow.setMaximumSize(QSize(1280, 800))
        MainWindow.setStyleSheet(u"background-color: #FFFCF8")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.sidebar_full = QWidget(self.centralwidget)
        self.sidebar_full.setObjectName(u"sidebar_full")
        self.sidebar_full.setGeometry(QRect(0, 0, 195, 800))
        self.sidebar_full.setMinimumSize(QSize(195, 800))
        self.sidebar_full.setMaximumSize(QSize(195, 800))
        self.sidebar_full.setAutoFillBackground(False)
        self.sidebar_full_2 = QWidget(self.sidebar_full)
        self.sidebar_full_2.setObjectName(u"sidebar_full_2")
        self.sidebar_full_2.setEnabled(True)
        self.sidebar_full_2.setGeometry(QRect(-30, 0, 230, 800))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.sidebar_full_2.sizePolicy().hasHeightForWidth())
        self.sidebar_full_2.setSizePolicy(sizePolicy1)
        self.sidebar_full_2.setMinimumSize(QSize(200, 800))
        self.sidebar_full_2.setMaximumSize(QSize(250, 800))
        self.sidebar_full_2.setAutoFillBackground(False)
        self.sidebar_full_2.setStyleSheet(u"QWidget{\n"
"	background-color: white;\n"
"	border-radius: 30px; /* Rounded corners */\n"
"	border: 0.4px solid gray; /* Light gray border */\n"
"\n"
"    /* Shadow effect */\n"
"	box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);\n"
"\n"
"}")
        self.layoutWidget = QWidget(self.sidebar_full_2)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 30, 211, 741))
        self.verticalLayout_3 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(21, 0, 21, 0)
        self.Logo = QLabel(self.layoutWidget)
        self.Logo.setObjectName(u"Logo")
        font = QFont()
        font.setFamilies([u"Helvetica"])
        font.setBold(True)
        self.Logo.setFont(font)
        self.Logo.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.Logo)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(7, -1, 7, -1)
        self.mainMenu = QLabel(self.layoutWidget)
        self.mainMenu.setObjectName(u"mainMenu")
        font1 = QFont()
        font1.setFamilies([u"Microsoft YaHei UI"])
        font1.setPointSize(6)
        self.mainMenu.setFont(font1)
        self.mainMenu.setStyleSheet(u"color: #B0B0B0;")

        self.verticalLayout.addWidget(self.mainMenu, 0, Qt.AlignLeft)

        self.dashboardButton = QPushButton(self.layoutWidget)
        self.dashboardButton.setObjectName(u"dashboardButton")
        self.dashboardButton.setMaximumSize(QSize(16777213, 16777215))
        font2 = QFont()
        font2.setFamilies([u"Microsoft JhengHei UI"])
        font2.setPointSize(8)
        font2.setBold(False)
        font2.setItalic(False)
        self.dashboardButton.setFont(font2)
        self.dashboardButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    outline: none; /* Removes any focus border */\n"
"    font: 8pt \"Microsoft JhengHei UI\";\n"
"    text-align: left;\n"
"	border-radius: 6px;\n"
"    background-color: transparent; /* Default background */\n"
"    color: black; /* Default text color */\n"
"    padding: 5px; /* Optional: Add padding for better spacing */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #EAEAEA; /* Soft gray background on hover */\n"
"    color: black; /* Keep text black for readability */\n"
"}\n"
"")
        icon = QIcon()
        icon.addFile(u":/resourcesnew/Dashboard.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.dashboardButton.setIcon(icon)
        self.dashboardButton.setFlat(False)

        self.verticalLayout.addWidget(self.dashboardButton)

        self.camerasButton = QPushButton(self.layoutWidget)
        self.camerasButton.setObjectName(u"camerasButton")
        self.camerasButton.setFont(font2)
        self.camerasButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    outline: none; /* Removes any focus border */\n"
"    font: 8pt \"Microsoft JhengHei UI\";\n"
"    text-align: left;\n"
"	border-radius: 6px;\n"
"    background-color: transparent; /* Default background */\n"
"    color: black; /* Default text color */\n"
"    padding: 5px; /* Optional: Add padding for better spacing */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #EAEAEA; /* Soft gray background on hover */\n"
"    color: black; /* Keep text black for readability */\n"
"}\n"
"")
        icon1 = QIcon()
        icon1.addFile(u":/resourcesnew/Cameras.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.camerasButton.setIcon(icon1)

        self.verticalLayout.addWidget(self.camerasButton)

        self.simulationButton = QPushButton(self.layoutWidget)
        self.simulationButton.setObjectName(u"simulationButton")
        self.simulationButton.setFont(font2)
        self.simulationButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    outline: none; /* Removes any focus border */\n"
"    font: 8pt \"Microsoft JhengHei UI\";\n"
"    text-align: left;\n"
"	border-radius: 6px;\n"
"    background-color: transparent; /* Default background */\n"
"    color: black; /* Default text color */\n"
"    padding: 5px; /* Optional: Add padding for better spacing */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #EAEAEA; /* Soft gray background on hover */\n"
"    color: black; /* Keep text black for readability */\n"
"}\n"
"")
        icon2 = QIcon()
        icon2.addFile(u":/resourcesnew/analytics.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.simulationButton.setIcon(icon2)

        self.verticalLayout.addWidget(self.simulationButton)

        self.jointAnalyticsButton = QPushButton(self.layoutWidget)
        self.jointAnalyticsButton.setObjectName(u"jointAnalyticsButton")
        self.jointAnalyticsButton.setFont(font2)
        self.jointAnalyticsButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    outline: none; /* Removes any focus border */\n"
"    font: 8pt \"Microsoft JhengHei UI\";\n"
"    text-align: left;\n"
"	border-radius: 6px;\n"
"    background-color: transparent; /* Default background */\n"
"    color: black; /* Default text color */\n"
"    padding: 5px; /* Optional: Add padding for better spacing */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #EAEAEA; /* Soft gray background on hover */\n"
"    color: black; /* Keep text black for readability */\n"
"}\n"
"")
        icon3 = QIcon()
        icon3.addFile(u":/resourcesnew/compare.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.jointAnalyticsButton.setIcon(icon3)

        self.verticalLayout.addWidget(self.jointAnalyticsButton)


        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.verticalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(7, -1, 7, -1)
        self.directoryMenu = QLabel(self.layoutWidget)
        self.directoryMenu.setObjectName(u"directoryMenu")
        self.directoryMenu.setMinimumSize(QSize(62, 16))
        self.directoryMenu.setMaximumSize(QSize(62, 16))
        font3 = QFont()
        font3.setFamilies([u"Helvetica"])
        font3.setPointSize(6)
        self.directoryMenu.setFont(font3)
        self.directoryMenu.setStyleSheet(u"color: #B0B0B0;")

        self.verticalLayout_2.addWidget(self.directoryMenu)

        self.sessionSelectButton = QPushButton(self.layoutWidget)
        self.sessionSelectButton.setObjectName(u"sessionSelectButton")
        self.sessionSelectButton.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.sessionSelectButton.sizePolicy().hasHeightForWidth())
        self.sessionSelectButton.setSizePolicy(sizePolicy2)
        self.sessionSelectButton.setBaseSize(QSize(0, -1))
        self.sessionSelectButton.setFont(font2)
        self.sessionSelectButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    outline: none; /* Removes any focus border */\n"
"    font: 8pt \"Microsoft JhengHei UI\";\n"
"    text-align: left;\n"
"	border-radius: 6px;\n"
"    background-color: transparent; /* Default background */\n"
"    color: black; /* Default text color */\n"
"    padding: 5px; /* Optional: Add padding for better spacing */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #EAEAEA; /* Soft gray background on hover */\n"
"    color: black; /* Keep text black for readability */\n"
"}")
        icon4 = QIcon()
        icon4.addFile(u":/resourcesnew/Stacks.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.sessionSelectButton.setIcon(icon4)

        self.verticalLayout_2.addWidget(self.sessionSelectButton)

        self.sessionSelectedLabel = QLabel(self.layoutWidget)
        self.sessionSelectedLabel.setObjectName(u"sessionSelectedLabel")
        self.sessionSelectedLabel.setEnabled(True)
        font4 = QFont()
        font4.setFamilies([u"Microsoft JhengHei UI Light"])
        font4.setPointSize(6)
        font4.setBold(False)
        font4.setItalic(False)
        self.sessionSelectedLabel.setFont(font4)
        self.sessionSelectedLabel.setStyleSheet(u"QLabel {\n"
"	color: #B0B0B0;\n"
"	font: 6pt \"Microsoft JhengHei UI Light\";\n"
"}")

        self.verticalLayout_2.addWidget(self.sessionSelectedLabel)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.participantSelectButton = QPushButton(self.layoutWidget)
        self.participantSelectButton.setObjectName(u"participantSelectButton")
        self.participantSelectButton.setEnabled(True)
        self.participantSelectButton.setFont(font2)
        self.participantSelectButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    outline: none; /* Removes any focus border */\n"
"    font: 8pt \"Microsoft JhengHei UI\";\n"
"    text-align: left;\n"
"	border-radius: 6px;\n"
"    background-color: transparent; /* Default background */\n"
"    color: black; /* Default text color */\n"
"    padding: 5px; /* Optional: Add padding for better spacing */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #EAEAEA; /* Soft gray background on hover */\n"
"    color: black; /* Keep text black for readability */\n"
"}")
        icon5 = QIcon()
        icon5.addFile(u":/resourcesnew/Group.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.participantSelectButton.setIcon(icon5)

        self.horizontalLayout.addWidget(self.participantSelectButton)

        self.horizontalSpacer_5 = QSpacerItem(18, 27, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)

        self.participantAddButton = QPushButton(self.layoutWidget)
        self.participantAddButton.setObjectName(u"participantAddButton")
        self.participantAddButton.setEnabled(True)
        sizePolicy.setHeightForWidth(self.participantAddButton.sizePolicy().hasHeightForWidth())
        self.participantAddButton.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.participantAddButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.participantSelectedLabel = QLabel(self.layoutWidget)
        self.participantSelectedLabel.setObjectName(u"participantSelectedLabel")
        self.participantSelectedLabel.setEnabled(True)
        self.participantSelectedLabel.setFont(font4)
        self.participantSelectedLabel.setStyleSheet(u"QLabel {\n"
"	color: #B0B0B0;\n"
"	font: 6pt \"Microsoft JhengHei UI Light\";\n"
"}")

        self.verticalLayout_2.addWidget(self.participantSelectedLabel)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.trialSelectButton = QPushButton(self.layoutWidget)
        self.trialSelectButton.setObjectName(u"trialSelectButton")
        self.trialSelectButton.setEnabled(True)
        self.trialSelectButton.setFont(font2)
        self.trialSelectButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    outline: none; /* Removes any focus border */\n"
"    font: 8pt \"Microsoft JhengHei UI\";\n"
"    text-align: left;\n"
"	border-radius: 6px;\n"
"    background-color: transparent; /* Default background */\n"
"    color: black; /* Default text color */\n"
"    padding: 5px; /* Optional: Add padding for better spacing */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #EAEAEA; /* Soft gray background on hover */\n"
"    color: black; /* Keep text black for readability */\n"
"}")
        icon6 = QIcon()
        icon6.addFile(u":/resourcesnew/session.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.trialSelectButton.setIcon(icon6)

        self.horizontalLayout_2.addWidget(self.trialSelectButton)

        self.horizontalSpacer_6 = QSpacerItem(18, 27, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)

        self.trialAddButton = QPushButton(self.layoutWidget)
        self.trialAddButton.setObjectName(u"trialAddButton")
        self.trialAddButton.setEnabled(True)
        sizePolicy.setHeightForWidth(self.trialAddButton.sizePolicy().hasHeightForWidth())
        self.trialAddButton.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.trialAddButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.trialSelectedLabel = QLabel(self.layoutWidget)
        self.trialSelectedLabel.setObjectName(u"trialSelectedLabel")
        self.trialSelectedLabel.setEnabled(True)
        self.trialSelectedLabel.setFont(font4)
        self.trialSelectedLabel.setStyleSheet(u"QLabel {\n"
"	color: #B0B0B0;\n"
"	font: 6pt \"Microsoft JhengHei UI Light\";\n"
"}")

        self.verticalLayout_2.addWidget(self.trialSelectedLabel)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.verticalLayout_2.addItem(self.verticalSpacer_4)

        self.processButton = QPushButton(self.layoutWidget)
        self.processButton.setObjectName(u"processButton")
        self.processButton.setEnabled(True)
        self.processButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    outline: none; /* Removes any focus border */\n"
"    font: 8pt \"Microsoft JhengHei UI\";\n"
"    text-align: left;\n"
"	border-radius: 6px;\n"
"    background-color: transparent; /* Default background */\n"
"    color: black; /* Default text color */\n"
"    padding: 5px; /* Optional: Add padding for better spacing */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #EAEAEA; /* Soft gray background on hover */\n"
"    color: black; /* Keep text black for readability */\n"
"}\n"
"")
        icon7 = QIcon()
        icon7.addFile(u":/resourcesnew/processing.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.processButton.setIcon(icon7)

        self.verticalLayout_2.addWidget(self.processButton)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.exitButton = QPushButton(self.layoutWidget)
        self.exitButton.setObjectName(u"exitButton")
        self.exitButton.setMinimumSize(QSize(164, 40))
        self.exitButton.setFont(font2)
        self.exitButton.setStyleSheet(u"QPushButton {\n"
"   \n"
"    outline: none; /* Removes any focus border */\n"
"    font: 8pt \"Microsoft JhengHei UI\";\n"
"    text-align: center;\n"
"    background-color: #FFFCF8; \n"
"    color: black; /* Default text color */\n"
"    padding: 5px; /* Optional: Add padding for better spacing */\n"
"	border-radius: 6px; /* Rounded corners */\n"
"	border: 0.5px solid #c8c8c8; /* Light gray border */\n"
"	\n"
"\n"
"    /* Shadow effect */\n"
"	box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #EAEAEA; /* Soft gray background on hover */\n"
"    color: black; /* Keep text black for readability */\n"
"}\n"
"")
        icon8 = QIcon()
        icon8.addFile(u":/Exit.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.exitButton.setIcon(icon8)

        self.verticalLayout_3.addWidget(self.exitButton, 0, Qt.AlignHCenter)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(210, 30, 1051, 751))
        self.processPage = QWidget()
        self.processPage.setObjectName(u"processPage")
        self.processLabel = QLabel(self.processPage)
        self.processLabel.setObjectName(u"processLabel")
        self.processLabel.setGeometry(QRect(490, 300, 131, 61))
        self.stackedWidget.addWidget(self.processPage)
        self.camerasPage = QWidget()
        self.camerasPage.setObjectName(u"camerasPage")
        self.cameraSlot1 = QLabel(self.camerasPage)
        self.cameraSlot1.setObjectName(u"cameraSlot1")
        self.cameraSlot1.setGeometry(QRect(90, 10, 391, 291))
        font5 = QFont()
        font5.setFamilies([u"Helvetica"])
        self.cameraSlot1.setFont(font5)
        self.cameraSlot1.setAutoFillBackground(False)
        self.cameraSlot1.setStyleSheet(u"border: 3px solid black\n"
"")
        self.cameraSlot1.setFrameShadow(QFrame.Raised)
        self.cameraSlot1.setAlignment(Qt.AlignCenter)
        self.cameraSlot2 = QLabel(self.camerasPage)
        self.cameraSlot2.setObjectName(u"cameraSlot2")
        self.cameraSlot2.setGeometry(QRect(500, 10, 391, 291))
        self.cameraSlot2.setFont(font5)
        self.cameraSlot2.setAutoFillBackground(False)
        self.cameraSlot2.setStyleSheet(u"border: 3px solid black\n"
"")
        self.cameraSlot2.setFrameShadow(QFrame.Raised)
        self.cameraSlot2.setAlignment(Qt.AlignCenter)
        self.cameraSlot3 = QLabel(self.camerasPage)
        self.cameraSlot3.setObjectName(u"cameraSlot3")
        self.cameraSlot3.setGeometry(QRect(290, 320, 391, 291))
        self.cameraSlot3.setFont(font5)
        self.cameraSlot3.setAutoFillBackground(False)
        self.cameraSlot3.setStyleSheet(u"border: 3px solid black\n"
"")
        self.cameraSlot3.setFrameShadow(QFrame.Raised)
        self.cameraSlot3.setAlignment(Qt.AlignCenter)
        self.directoryLabel = QLabel(self.camerasPage)
        self.directoryLabel.setObjectName(u"directoryLabel")
        self.directoryLabel.setGeometry(QRect(470, 650, 60, 16))
        self.directoryLabel.setFont(font5)
        self.camerasLabel = QLabel(self.camerasPage)
        self.camerasLabel.setObjectName(u"camerasLabel")
        self.camerasLabel.setGeometry(QRect(470, 670, 60, 16))
        self.camerasLabel.setFont(font5)
        self.resolutionLabel_2 = QLabel(self.camerasPage)
        self.resolutionLabel_2.setObjectName(u"resolutionLabel_2")
        self.resolutionLabel_2.setGeometry(QRect(470, 690, 71, 16))
        self.resolutionLabel_2.setFont(font5)
        self.framerateLabel = QLabel(self.camerasPage)
        self.framerateLabel.setObjectName(u"framerateLabel")
        self.framerateLabel.setGeometry(QRect(470, 710, 71, 16))
        self.framerateLabel.setFont(font5)
        self.directoryValue = QLabel(self.camerasPage)
        self.directoryValue.setObjectName(u"directoryValue")
        self.directoryValue.setGeometry(QRect(550, 650, 60, 16))
        self.directoryValue.setFont(font5)
        self.camerasValue = QLabel(self.camerasPage)
        self.camerasValue.setObjectName(u"camerasValue")
        self.camerasValue.setGeometry(QRect(550, 670, 60, 16))
        self.camerasValue.setFont(font5)
        self.resolutionValue = QLabel(self.camerasPage)
        self.resolutionValue.setObjectName(u"resolutionValue")
        self.resolutionValue.setGeometry(QRect(550, 690, 60, 16))
        self.resolutionValue.setFont(font5)
        self.framerateValue = QLabel(self.camerasPage)
        self.framerateValue.setObjectName(u"framerateValue")
        self.framerateValue.setGeometry(QRect(550, 710, 60, 16))
        self.framerateValue.setFont(font5)
        self.detectCamerasButton = QPushButton(self.camerasPage)
        self.detectCamerasButton.setObjectName(u"detectCamerasButton")
        self.detectCamerasButton.setGeometry(QRect(90, 630, 161, 50))
        font6 = QFont()
        font6.setFamilies([u"MS Reference Sans Serif"])
        font6.setBold(False)
        font6.setItalic(False)
        self.detectCamerasButton.setFont(font6)
        self.detectCamerasButton.setStyleSheet(u"QPushButton {\n"
"	font: 8pt \"MS Reference Sans Serif\";\n"
"    background-color: #231A16; /* Dark brown background */\n"
"    color: white; /* White text */\n"
"    font-size: 14px;\n"
"    border-radius: 15px; /* Rounded corners */\n"
"    padding: 10px 20px; /* Adjust padding for proper button size */\n"
"    border: none; /* No border */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #3A2C26; /* Lighter brown on hover */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #18120E; /* Even darker shade on press */\n"
"}\n"
"")
        self.detectCamerasButton.setIconSize(QSize(20, 15))
        self.startRecordingButton = QPushButton(self.camerasPage)
        self.startRecordingButton.setObjectName(u"startRecordingButton")
        self.startRecordingButton.setGeometry(QRect(260, 630, 161, 50))
        self.startRecordingButton.setFont(font6)
        self.startRecordingButton.setStyleSheet(u"QPushButton {\n"
"	font: 8pt \"MS Reference Sans Serif\";\n"
"    background-color: #231A16; /* Dark brown background */\n"
"    color: white; /* White text */\n"
"    font-size: 14px;\n"
"    border-radius: 15px; /* Rounded corners */\n"
"    padding: 10px 20px; /* Adjust padding for proper button size */\n"
"    border: none; /* No border */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #3A2C26; /* Lighter brown on hover */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #18120E; /* Even darker shade on press */\n"
"}\n"
"")
        self.closeCamerasButton = QPushButton(self.camerasPage)
        self.closeCamerasButton.setObjectName(u"closeCamerasButton")
        self.closeCamerasButton.setGeometry(QRect(90, 690, 161, 50))
        self.closeCamerasButton.setFont(font6)
        self.closeCamerasButton.setStyleSheet(u"QPushButton {\n"
"	font: 8pt \"MS Reference Sans Serif\";\n"
"    background-color: #231A16; /* Dark brown background */\n"
"    color: white; /* White text */\n"
"    font-size: 14px;\n"
"    border-radius: 15px; /* Rounded corners */\n"
"    padding: 10px 20px; /* Adjust padding for proper button size */\n"
"    border: none; /* No border */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #3A2C26; /* Lighter brown on hover */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #18120E; /* Even darker shade on press */\n"
"}\n"
"")
        self.closeCamerasButton.setIconSize(QSize(20, 15))
        self.stopRecordingButton = QPushButton(self.camerasPage)
        self.stopRecordingButton.setObjectName(u"stopRecordingButton")
        self.stopRecordingButton.setGeometry(QRect(260, 690, 161, 50))
        self.stopRecordingButton.setFont(font6)
        self.stopRecordingButton.setStyleSheet(u"QPushButton {\n"
"	font: 8pt \"MS Reference Sans Serif\";\n"
"    background-color: #231A16; /* Dark brown background */\n"
"    color: white; /* White text */\n"
"    font-size: 14px;\n"
"    border-radius: 15px; /* Rounded corners */\n"
"    padding: 10px 20px; /* Adjust padding for proper button size */\n"
"    border: none; /* No border */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #3A2C26; /* Lighter brown on hover */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #18120E; /* Even darker shade on press */\n"
"}\n"
"")
        self.stackedWidget.addWidget(self.camerasPage)
        self.simulationPage = QWidget()
        self.simulationPage.setObjectName(u"simulationPage")
        self.widget = QWidget(self.simulationPage)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 50, 500, 291))
        self.widget.setAutoFillBackground(False)
        self.widget.setStyleSheet(u"")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(220, 140, 91, 16))
        self.horizontalLayoutWidget = QWidget(self.simulationPage)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 0, 1021, 41))
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.allTabButton = QPushButton(self.horizontalLayoutWidget)
        self.allTabButton.setObjectName(u"allTabButton")
        self.allTabButton.setStyleSheet(u" font: 8pt \"Microsoft JhengHei UI\";")

        self.horizontalLayout_3.addWidget(self.allTabButton)

        self.hipTabButton = QPushButton(self.horizontalLayoutWidget)
        self.hipTabButton.setObjectName(u"hipTabButton")
        self.hipTabButton.setStyleSheet(u" font: 8pt \"Microsoft JhengHei UI\";")

        self.horizontalLayout_3.addWidget(self.hipTabButton)

        self.kneeTabButton = QPushButton(self.horizontalLayoutWidget)
        self.kneeTabButton.setObjectName(u"kneeTabButton")
        self.kneeTabButton.setStyleSheet(u" font: 8pt \"Microsoft JhengHei UI\";")

        self.horizontalLayout_3.addWidget(self.kneeTabButton)

        self.pushButton_4 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setStyleSheet(u" font: 8pt \"Microsoft JhengHei UI\";")

        self.horizontalLayout_3.addWidget(self.pushButton_4)

        self.jointsTable = QTableWidget(self.simulationPage)
        self.jointsTable.setObjectName(u"jointsTable")
        self.jointsTable.setGeometry(QRect(530, 50, 500, 291))
        self.chartsWidget = QWidget(self.simulationPage)
        self.chartsWidget.setObjectName(u"chartsWidget")
        self.chartsWidget.setGeometry(QRect(10, 350, 1020, 251))
        self.label_2 = QLabel(self.chartsWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(480, 120, 71, 16))
        self.slider = QSlider(self.simulationPage)
        self.slider.setObjectName(u"slider")
        self.slider.setGeometry(QRect(10, 670, 1021, 22))
        self.slider.setStyleSheet(u"QSlider::groove:horizontal {\n"
"    border: none;\n"
"    height: 8px;\n"
"    background: #E0E0E0;  /* Light gray background */\n"
"    border-radius: 4px;   /* Rounded groove */\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"    background: #8B4513;  /* Brown progress bar */\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal {\n"
"    background: #E0E0E0;  /* Gray remaining bar */\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background: white;\n"
"    border: 2px solid #8B4513;  /* Brown border */\n"
"    width: 14px;\n"
"    height: 14px;\n"
"    border-radius: 7px;   /* Circular handle */\n"
"    margin: -3px 0;       /* Center handle */\n"
"}\n"
"\n"
"QSlider::handle:horizontal:hover {\n"
"    background: #8B4513;  /* Brown on hover */\n"
"    border: 2px solid #5C3317;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:pressed {\n"
"    background: #5C3317;\n"
"    border: 2px solid #3D2309;\n"
"}\n"
"")
        self.slider.setOrientation(Qt.Horizontal)
        self.horizontalLayoutWidget_2 = QWidget(self.simulationPage)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(10, 700, 1021, 41))
        self.horizontalLayout_4 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.rewindButton = QPushButton(self.horizontalLayoutWidget_2)
        self.rewindButton.setObjectName(u"rewindButton")
        icon9 = QIcon()
        icon9.addFile(u":/resourcesnew/left.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.rewindButton.setIcon(icon9)

        self.horizontalLayout_4.addWidget(self.rewindButton)

        self.backButton = QPushButton(self.horizontalLayoutWidget_2)
        self.backButton.setObjectName(u"backButton")
        icon10 = QIcon()
        icon10.addFile(u":/resourcesnew/Icon (4).png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.backButton.setIcon(icon10)

        self.horizontalLayout_4.addWidget(self.backButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.pauseButton = QPushButton(self.horizontalLayoutWidget_2)
        self.pauseButton.setObjectName(u"pauseButton")
        icon11 = QIcon()
        icon11.addFile(u":/resourcesnew/Play.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pauseButton.setIcon(icon11)

        self.horizontalLayout_4.addWidget(self.pauseButton)

        self.playButton = QPushButton(self.horizontalLayoutWidget_2)
        self.playButton.setObjectName(u"playButton")
        icon12 = QIcon()
        icon12.addFile(u":/resourcesnew/Pause.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.playButton.setIcon(icon12)

        self.horizontalLayout_4.addWidget(self.playButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.skipButton = QPushButton(self.horizontalLayoutWidget_2)
        self.skipButton.setObjectName(u"skipButton")
        icon13 = QIcon()
        icon13.addFile(u":/resourcesnew/Icon (3).png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.skipButton.setIcon(icon13)

        self.horizontalLayout_4.addWidget(self.skipButton)

        self.fastForwardButton = QPushButton(self.horizontalLayoutWidget_2)
        self.fastForwardButton.setObjectName(u"fastForwardButton")
        icon14 = QIcon()
        icon14.addFile(u":/resourcesnew/right.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.fastForwardButton.setIcon(icon14)

        self.horizontalLayout_4.addWidget(self.fastForwardButton)

        self.horizontalLayoutWidget_3 = QWidget(self.simulationPage)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(10, 620, 1021, 41))
        self.horizontalLayout_6 = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.timeLabel = QLabel(self.horizontalLayoutWidget_3)
        self.timeLabel.setObjectName(u"timeLabel")
        font7 = QFont()
        font7.setFamilies([u"Yu Gothic UI Semibold"])
        font7.setPointSize(8)
        font7.setBold(False)
        font7.setItalic(False)
        self.timeLabel.setFont(font7)
        self.timeLabel.setStyleSheet(u"font: 63 8pt \"Yu Gothic UI Semibold\";")

        self.horizontalLayout_6.addWidget(self.timeLabel)

        self.timeValue = QLabel(self.horizontalLayoutWidget_3)
        self.timeValue.setObjectName(u"timeValue")
        font8 = QFont()
        font8.setFamilies([u"Microsoft YaHei UI Light"])
        font8.setPointSize(8)
        font8.setBold(False)
        font8.setItalic(False)
        self.timeValue.setFont(font8)
        self.timeValue.setStyleSheet(u"font: 25 8pt \"Microsoft YaHei UI Light\";")

        self.horizontalLayout_6.addWidget(self.timeValue)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_3)

        self.gaitStageLabel = QLabel(self.horizontalLayoutWidget_3)
        self.gaitStageLabel.setObjectName(u"gaitStageLabel")
        self.gaitStageLabel.setFont(font7)
        self.gaitStageLabel.setStyleSheet(u"font: 63 8pt \"Yu Gothic UI Semibold\";")

        self.horizontalLayout_6.addWidget(self.gaitStageLabel)

        self.gaitStageValue = QLabel(self.horizontalLayoutWidget_3)
        self.gaitStageValue.setObjectName(u"gaitStageValue")
        self.gaitStageValue.setFont(font8)
        self.gaitStageValue.setStyleSheet(u"font: 25 8pt \"Microsoft YaHei UI Light\";")

        self.horizontalLayout_6.addWidget(self.gaitStageValue)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)

        self.frameLabel = QLabel(self.horizontalLayoutWidget_3)
        self.frameLabel.setObjectName(u"frameLabel")
        self.frameLabel.setFont(font7)
        self.frameLabel.setStyleSheet(u"font: 63 8pt \"Yu Gothic UI Semibold\";")

        self.horizontalLayout_6.addWidget(self.frameLabel)

        self.frameValue = QLabel(self.horizontalLayoutWidget_3)
        self.frameValue.setObjectName(u"frameValue")
        font9 = QFont()
        font9.setFamilies([u"Microsoft YaHei UI Light"])
        self.frameValue.setFont(font9)

        self.horizontalLayout_6.addWidget(self.frameValue)

        self.stackedWidget.addWidget(self.simulationPage)
        self.analyticsPage = QWidget()
        self.analyticsPage.setObjectName(u"analyticsPage")
        self.tableWidget = QTableWidget(self.analyticsPage)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(30, 70, 256, 192))
        self.tableWidget_2 = QTableWidget(self.analyticsPage)
        self.tableWidget_2.setObjectName(u"tableWidget_2")
        self.tableWidget_2.setGeometry(QRect(30, 270, 256, 192))
        self.tableWidget_3 = QTableWidget(self.analyticsPage)
        self.tableWidget_3.setObjectName(u"tableWidget_3")
        self.tableWidget_3.setGeometry(QRect(30, 470, 256, 192))
        self.stackedWidget.addWidget(self.analyticsPage)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.dashboardButton.setDefault(False)
        self.stackedWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.Logo.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><img src=\":/resourcesnew/Logo Text.png\"/></p></body></html>", None))
        self.mainMenu.setText(QCoreApplication.translate("MainWindow", u"MAIN MENU", None))
        self.dashboardButton.setText(QCoreApplication.translate("MainWindow", u"Dashboard", None))
        self.camerasButton.setText(QCoreApplication.translate("MainWindow", u"Cameras", None))
        self.simulationButton.setText(QCoreApplication.translate("MainWindow", u"Analytics", None))
        self.jointAnalyticsButton.setText(QCoreApplication.translate("MainWindow", u"Compare", None))
        self.directoryMenu.setText(QCoreApplication.translate("MainWindow", u"DIRECTORY", None))
        self.sessionSelectButton.setText(QCoreApplication.translate("MainWindow", u"Session", None))
        self.sessionSelectedLabel.setText(QCoreApplication.translate("MainWindow", u"Session Name", None))
        self.participantSelectButton.setText(QCoreApplication.translate("MainWindow", u"Participant", None))
        self.participantAddButton.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.participantSelectedLabel.setText(QCoreApplication.translate("MainWindow", u"Participant Name", None))
        self.trialSelectButton.setText(QCoreApplication.translate("MainWindow", u"Trial", None))
        self.trialAddButton.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.trialSelectedLabel.setText(QCoreApplication.translate("MainWindow", u"Trial Name", None))
        self.processButton.setText(QCoreApplication.translate("MainWindow", u"Process", None))
        self.exitButton.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.processLabel.setText(QCoreApplication.translate("MainWindow", u"dashboard", None))
        self.cameraSlot1.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><img src=\":/resourcesnew/Videocam Off.png\"/></p></body></html>", None))
        self.cameraSlot2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><img src=\":/resourcesnew/Videocam Off.png\"/></p></body></html>", None))
        self.cameraSlot3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><img src=\":/resourcesnew/Videocam Off.png\"/></p></body></html>", None))
        self.directoryLabel.setText(QCoreApplication.translate("MainWindow", u"Directory", None))
        self.camerasLabel.setText(QCoreApplication.translate("MainWindow", u"Cameras", None))
        self.resolutionLabel_2.setText(QCoreApplication.translate("MainWindow", u"Resolution", None))
        self.framerateLabel.setText(QCoreApplication.translate("MainWindow", u"Frame Rate", None))
        self.directoryValue.setText("")
        self.camerasValue.setText("")
        self.resolutionValue.setText("")
        self.framerateValue.setText("")
        self.detectCamerasButton.setText(QCoreApplication.translate("MainWindow", u"Detect Cameras", None))
        self.startRecordingButton.setText(QCoreApplication.translate("MainWindow", u"Start Recording", None))
        self.closeCamerasButton.setText(QCoreApplication.translate("MainWindow", u"Close Cameras", None))
        self.stopRecordingButton.setText(QCoreApplication.translate("MainWindow", u"Stop Recording", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"QtWebEngine", None))
        self.allTabButton.setText(QCoreApplication.translate("MainWindow", u"All", None))
        self.hipTabButton.setText(QCoreApplication.translate("MainWindow", u"Hip", None))
        self.kneeTabButton.setText(QCoreApplication.translate("MainWindow", u"Knee", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Ankle", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"PyQtChart", None))
        self.rewindButton.setText("")
        self.backButton.setText("")
        self.pauseButton.setText("")
        self.playButton.setText("")
        self.skipButton.setText("")
        self.fastForwardButton.setText("")
        self.timeLabel.setText(QCoreApplication.translate("MainWindow", u"Time:", None))
        self.timeValue.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
        self.gaitStageLabel.setText(QCoreApplication.translate("MainWindow", u"Gait Stage (\u00b0): ", None))
        self.gaitStageValue.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.frameLabel.setText(QCoreApplication.translate("MainWindow", u"Frame:", None))
        self.frameValue.setText(QCoreApplication.translate("MainWindow", u"1/n", None))
    # retranslateUi

