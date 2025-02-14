# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\asus\Downloads\thesis-redesign (1)\thesis-redesign\final_ui\final.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(1280, 800)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1280, 800))
        MainWindow.setMaximumSize(QtCore.QSize(1280, 800))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: #FFFCF8")
        self.centralwidget.setObjectName("centralwidget")
        self.sidebar_full = QtWidgets.QWidget(self.centralwidget)
        self.sidebar_full.setEnabled(True)
        self.sidebar_full.setGeometry(QtCore.QRect(-20, 0, 230, 800))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sidebar_full.sizePolicy().hasHeightForWidth())
        self.sidebar_full.setSizePolicy(sizePolicy)
        self.sidebar_full.setMinimumSize(QtCore.QSize(200, 800))
        self.sidebar_full.setMaximumSize(QtCore.QSize(250, 800))
        self.sidebar_full.setAutoFillBackground(False)
        self.sidebar_full.setStyleSheet("QWidget{\n"
"    background-color: white;\n"
"    border-radius: 30px; /* Rounded corners */\n"
"    border: 0.4px solid gray; /* Light gray border */\n"
"\n"
"    /* Shadow effect */\n"
"    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);\n"
"\n"
"}")
        self.sidebar_full.setObjectName("sidebar_full")
        self.layoutWidget = QtWidgets.QWidget(self.sidebar_full)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 30, 211, 741))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setContentsMargins(21, 0, 21, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.Logo = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setBold(True)
        font.setWeight(75)
        self.Logo.setFont(font)
        self.Logo.setAlignment(QtCore.Qt.AlignCenter)
        self.Logo.setObjectName("Logo")
        self.verticalLayout_3.addWidget(self.Logo)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout_3.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.mainMenu = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(6)
        self.mainMenu.setFont(font)
        self.mainMenu.setStyleSheet("color: #B0B0B0;")
        self.mainMenu.setObjectName("mainMenu")
        self.verticalLayout.addWidget(self.mainMenu, 0, QtCore.Qt.AlignLeft)
        self.dashboardButton = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.dashboardButton.setFont(font)
        self.dashboardButton.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    outline: none; /* Removes any focus border */\n"
"    font: 8pt \"Microsoft JhengHei UI\";\n"
"    text-align: left;\n"
"    border-radius: 6px;\n"
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
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Dashboard.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.dashboardButton.setIcon(icon)
        self.dashboardButton.setDefault(False)
        self.dashboardButton.setFlat(False)
        self.dashboardButton.setObjectName("dashboardButton")
        self.verticalLayout.addWidget(self.dashboardButton)
        self.camerasButton = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.camerasButton.setFont(font)
        self.camerasButton.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    outline: none; /* Removes any focus border */\n"
"    font: 8pt \"Microsoft JhengHei UI\";\n"
"    text-align: left;\n"
"    border-radius: 6px;\n"
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
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Cameras.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.camerasButton.setIcon(icon1)
        self.camerasButton.setObjectName("camerasButton")
        self.verticalLayout.addWidget(self.camerasButton)
        self.simulationButton = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.simulationButton.setFont(font)
        self.simulationButton.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    outline: none; /* Removes any focus border */\n"
"    font: 8pt \"Microsoft JhengHei UI\";\n"
"    text-align: left;\n"
"    border-radius: 6px;\n"
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
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/3D Simulation.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.simulationButton.setIcon(icon2)
        self.simulationButton.setObjectName("simulationButton")
        self.verticalLayout.addWidget(self.simulationButton)
        self.jointAnalyticsButton = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.jointAnalyticsButton.setFont(font)
        self.jointAnalyticsButton.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    outline: none; /* Removes any focus border */\n"
"    font: 8pt \"Microsoft JhengHei UI\";\n"
"    text-align: left;\n"
"    border-radius: 6px;\n"
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
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/Joint Analytics.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.jointAnalyticsButton.setIcon(icon3)
        self.jointAnalyticsButton.setObjectName("jointAnalyticsButton")
        self.verticalLayout.addWidget(self.jointAnalyticsButton)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout_3.addItem(spacerItem1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.directoryMenu = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(6)
        self.directoryMenu.setFont(font)
        self.directoryMenu.setStyleSheet("QLabel {\n"
"    color: #B0B0B0;\n"
"}")
        self.directoryMenu.setObjectName("directoryMenu")
        self.verticalLayout_2.addWidget(self.directoryMenu, 0, QtCore.Qt.AlignLeft)
        self.sessionSelectButton = QtWidgets.QPushButton(self.layoutWidget)
        self.sessionSelectButton.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sessionSelectButton.sizePolicy().hasHeightForWidth())
        self.sessionSelectButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.sessionSelectButton.setFont(font)
        self.sessionSelectButton.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"border-radius: 6px;\n"
"    outline: none; /* Removes any focus border */\n"
"    font: 8pt \"Microsoft JhengHei UI\";\n"
"    text-align: left;\n"
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
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/Stacks.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.sessionSelectButton.setIcon(icon4)
        self.sessionSelectButton.setIconSize(QtCore.QSize(22, 22))
        self.sessionSelectButton.setObjectName("sessionSelectButton")
        self.verticalLayout_2.addWidget(self.sessionSelectButton)
        self.label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI Light")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet("QLabel {\n"
"    color: #B0B0B0;\n"
"    font: 6pt \"Microsoft JhengHei UI Light\";\n"
"}")
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.participantSelectButton = QtWidgets.QPushButton(self.layoutWidget)
        self.participantSelectButton.setEnabled(True)
        self.participantSelectButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.participantSelectButton.setFont(font)
        self.participantSelectButton.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    outline: none; /* Removes any focus border */\n"
"    font: 8pt \"Microsoft JhengHei UI\";\n"
"    text-align: left;\n"
"    background-color: transparent; /* Default background */\n"
"    color: black; /* Default text color */\n"
"    border-radius: 6px;\n"
"    padding: 5px; /* Optional: Add padding for better spacing */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #EAEAEA; /* Soft gray background on hover */\n"
"    color: black; /* Keep text black for readability */\n"
"}\n"
"")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/Group.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.participantSelectButton.setIcon(icon5)
        self.participantSelectButton.setIconSize(QtCore.QSize(22, 22))
        self.participantSelectButton.setObjectName("participantSelectButton")
        self.verticalLayout_2.addWidget(self.participantSelectButton)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setStyleSheet("QLabel {\n"
"    color: #B0B0B0;\n"
"    font: 6pt \"Microsoft JhengHei UI Light\";\n"
"}")
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.trialSelectButton = QtWidgets.QPushButton(self.layoutWidget)
        self.trialSelectButton.setEnabled(True)
        self.trialSelectButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.trialSelectButton.setFont(font)
        self.trialSelectButton.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    outline: none; /* Removes any focus border */\n"
"    font: 8pt \"Microsoft JhengHei UI\";\n"
"    text-align: left;\n"
"    border-radius: 6px;\n"
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
        self.trialSelectButton.setIcon(icon3)
        self.trialSelectButton.setObjectName("trialSelectButton")
        self.verticalLayout_2.addWidget(self.trialSelectButton)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setStyleSheet("QLabel {\n"
"    color: #B0B0B0;\n"
"    font: 6pt \"Microsoft JhengHei UI Light\";\n"
"}")
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.exitButton = QtWidgets.QPushButton(self.layoutWidget)
        self.exitButton.setMinimumSize(QtCore.QSize(164, 40))
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.exitButton.setFont(font)
        self.exitButton.setStyleSheet("QPushButton {\n"
"   \n"
"    outline: none; /* Removes any focus border */\n"
"    font: 8pt \"Microsoft JhengHei UI\";\n"
"    text-align: center;\n"
"    background-color: #FFFCF8; \n"
"    color: black; /* Default text color */\n"
"    padding: 5px; /* Optional: Add padding for better spacing */\n"
"    border-radius: 6px; /* Rounded corners */\n"
"    border: 0.5px solid #c8c8c8; /* Light gray border */\n"
"    \n"
"\n"
"    /* Shadow effect */\n"
"    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #EAEAEA; /* Soft gray background on hover */\n"
"    color: black; /* Keep text black for readability */\n"
"}\n"
"")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/Exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exitButton.setIcon(icon6)
        self.exitButton.setObjectName("exitButton")
        self.verticalLayout_3.addWidget(self.exitButton, 0, QtCore.Qt.AlignHCenter)
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(195, 0, 1081, 811))
        self.stackedWidget.setStyleSheet("background-color: #FFFCF8")
        self.stackedWidget.setObjectName("stackedWidget")
        self.dashboardPage = QtWidgets.QWidget()
        self.dashboardPage.setObjectName("dashboardPage")
        self.dashboardLabel = QtWidgets.QLabel(self.dashboardPage)
        self.dashboardLabel.setGeometry(QtCore.QRect(490, 300, 131, 61))
        self.dashboardLabel.setObjectName("dashboardLabel")
        self.stackedWidget.addWidget(self.dashboardPage)
        self.camerasPage = QtWidgets.QWidget()
        self.camerasPage.setObjectName("camerasPage")
        self.cameraSlot1 = QtWidgets.QLabel(self.camerasPage)
        self.cameraSlot1.setGeometry(QtCore.QRect(90, 10, 391, 291))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.cameraSlot1.setFont(font)
        self.cameraSlot1.setAutoFillBackground(False)
        self.cameraSlot1.setStyleSheet("border: 3px solid black\n"
"rgb(152, 152, 152)")
        self.cameraSlot1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cameraSlot1.setAlignment(QtCore.Qt.AlignCenter)
        self.cameraSlot1.setObjectName("cameraSlot1")
        self.cameraSlot2 = QtWidgets.QLabel(self.camerasPage)
        self.cameraSlot2.setGeometry(QtCore.QRect(500, 10, 391, 291))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.cameraSlot2.setFont(font)
        self.cameraSlot2.setAutoFillBackground(False)
        self.cameraSlot2.setStyleSheet("border: 3px solid black\n"
"")
        self.cameraSlot2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cameraSlot2.setAlignment(QtCore.Qt.AlignCenter)
        self.cameraSlot2.setObjectName("cameraSlot2")
        self.cameraSlot3 = QtWidgets.QLabel(self.camerasPage)
        self.cameraSlot3.setGeometry(QtCore.QRect(290, 320, 391, 291))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.cameraSlot3.setFont(font)
        self.cameraSlot3.setAutoFillBackground(False)
        self.cameraSlot3.setStyleSheet("border: 3px solid black\n"
"")
        self.cameraSlot3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cameraSlot3.setAlignment(QtCore.Qt.AlignCenter)
        self.cameraSlot3.setObjectName("cameraSlot3")
        self.detectCamerasButton = QtWidgets.QPushButton(self.camerasPage)
        self.detectCamerasButton.setGeometry(QtCore.QRect(90, 630, 161, 61))
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.detectCamerasButton.setFont(font)
        self.detectCamerasButton.setStyleSheet("QPushButton {\n"
"    font: 8pt \"MS Reference Sans Serif\";\n"
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
        self.detectCamerasButton.setObjectName("detectCamerasButton")
        self.startRecordingButton = QtWidgets.QPushButton(self.camerasPage)
        self.startRecordingButton.setGeometry(QtCore.QRect(260, 630, 161, 61))
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.startRecordingButton.setFont(font)
        self.startRecordingButton.setStyleSheet("QPushButton {\n"
"    font: 8pt \"MS Reference Sans Serif\";\n"
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
        self.startRecordingButton.setObjectName("startRecordingButton")
        self.closeCamerasButton = QtWidgets.QPushButton(self.camerasPage)
        self.closeCamerasButton.setGeometry(QtCore.QRect(90, 700, 161, 61))
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.closeCamerasButton.setFont(font)
        self.closeCamerasButton.setStyleSheet("QPushButton {\n"
"    font: 8pt \"MS Reference Sans Serif\";\n"
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
        self.closeCamerasButton.setObjectName("closeCamerasButton")
        self.stopRecordingButton = QtWidgets.QPushButton(self.camerasPage)
        self.stopRecordingButton.setGeometry(QtCore.QRect(260, 700, 161, 61))
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.stopRecordingButton.setFont(font)
        self.stopRecordingButton.setStyleSheet("QPushButton {\n"
"    font: 8pt \"MS Reference Sans Serif\";\n"
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
        self.stopRecordingButton.setObjectName("stopRecordingButton")
        self.directoryLabel = QtWidgets.QLabel(self.camerasPage)
        self.directoryLabel.setGeometry(QtCore.QRect(570, 650, 60, 16))
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.directoryLabel.setFont(font)
        self.directoryLabel.setStyleSheet("font: 8pt \"Microsoft JhengHei UI\";")
        self.directoryLabel.setObjectName("directoryLabel")
        self.camerasLabel = QtWidgets.QLabel(self.camerasPage)
        self.camerasLabel.setGeometry(QtCore.QRect(570, 670, 60, 16))
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.camerasLabel.setFont(font)
        self.camerasLabel.setStyleSheet("font: 8pt \"Microsoft JhengHei UI\";")
        self.camerasLabel.setObjectName("camerasLabel")
        self.resolutionLabel_2 = QtWidgets.QLabel(self.camerasPage)
        self.resolutionLabel_2.setGeometry(QtCore.QRect(570, 690, 71, 16))
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.resolutionLabel_2.setFont(font)
        self.resolutionLabel_2.setStyleSheet("font: 8pt \"Microsoft JhengHei UI\";")
        self.resolutionLabel_2.setObjectName("resolutionLabel_2")
        self.framerateLabel = QtWidgets.QLabel(self.camerasPage)
        self.framerateLabel.setGeometry(QtCore.QRect(570, 710, 71, 16))
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.framerateLabel.setFont(font)
        self.framerateLabel.setStyleSheet("font: 8pt \"Microsoft JhengHei UI\";")
        self.framerateLabel.setObjectName("framerateLabel")
        self.directoryValue = QtWidgets.QLabel(self.camerasPage)
        self.directoryValue.setGeometry(QtCore.QRect(650, 650, 60, 16))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.directoryValue.setFont(font)
        self.directoryValue.setText("")
        self.directoryValue.setObjectName("directoryValue")
        self.camerasValue = QtWidgets.QLabel(self.camerasPage)
        self.camerasValue.setGeometry(QtCore.QRect(650, 670, 60, 16))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.camerasValue.setFont(font)
        self.camerasValue.setText("")
        self.camerasValue.setObjectName("camerasValue")
        self.resolutionValue = QtWidgets.QLabel(self.camerasPage)
        self.resolutionValue.setGeometry(QtCore.QRect(650, 690, 60, 16))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.resolutionValue.setFont(font)
        self.resolutionValue.setText("")
        self.resolutionValue.setObjectName("resolutionValue")
        self.framerateValue = QtWidgets.QLabel(self.camerasPage)
        self.framerateValue.setGeometry(QtCore.QRect(650, 710, 60, 16))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.framerateValue.setFont(font)
        self.framerateValue.setText("")
        self.framerateValue.setObjectName("framerateValue")
        self.stackedWidget.addWidget(self.camerasPage)
        self.simulationPage = QtWidgets.QWidget()
        self.simulationPage.setObjectName("simulationPage")
        self.simulationLabel = QtWidgets.QLabel(self.simulationPage)
        self.simulationLabel.setGeometry(QtCore.QRect(440, 350, 131, 61))
        self.simulationLabel.setObjectName("simulationLabel")
        self.stackedWidget.addWidget(self.simulationPage)
        self.analyticsPage = QtWidgets.QWidget()
        self.analyticsPage.setObjectName("analyticsPage")
        self.tableWidget = QtWidgets.QTableWidget(self.analyticsPage)
        self.tableWidget.setGeometry(QtCore.QRect(30, 70, 256, 192))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget_2 = QtWidgets.QTableWidget(self.analyticsPage)
        self.tableWidget_2.setGeometry(QtCore.QRect(30, 270, 256, 192))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_3 = QtWidgets.QTableWidget(self.analyticsPage)
        self.tableWidget_3.setGeometry(QtCore.QRect(30, 470, 256, 192))
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(0)
        self.tableWidget_3.setRowCount(0)
        self.stackedWidget.addWidget(self.analyticsPage)
        self.stackedWidget.raise_()
        self.sidebar_full.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Logo.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/Logo Text.png\"/></p></body></html>"))
        self.mainMenu.setText(_translate("MainWindow", "MAIN MENU"))
        self.dashboardButton.setText(_translate("MainWindow", "Dashboard"))
        self.camerasButton.setText(_translate("MainWindow", "Cameras"))
        self.simulationButton.setText(_translate("MainWindow", "3D Simulation"))
        self.jointAnalyticsButton.setText(_translate("MainWindow", "Joint Analytics"))
        self.directoryMenu.setText(_translate("MainWindow", "DIRECTORY"))
        self.sessionSelectButton.setText(_translate("MainWindow", "Session"))
        self.label.setText(_translate("MainWindow", "          Session Name"))
        self.participantSelectButton.setText(_translate("MainWindow", "Participant"))
        self.label_2.setText(_translate("MainWindow", "          Participant Name"))
        self.trialSelectButton.setText(_translate("MainWindow", "Trial"))
        self.label_3.setText(_translate("MainWindow", "           Trial Name"))
        self.exitButton.setText(_translate("MainWindow", "Exit"))
        self.dashboardLabel.setText(_translate("MainWindow", "dashboard"))
        self.cameraSlot1.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/Videocam Off.png\"/></p></body></html>"))
        self.cameraSlot2.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/Videocam Off.png\"/></p></body></html>"))
        self.cameraSlot3.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/Videocam Off.png\"/></p></body></html>"))
        self.detectCamerasButton.setText(_translate("MainWindow", "Detect Cameras"))
        self.startRecordingButton.setText(_translate("MainWindow", "Start Recording"))
        self.closeCamerasButton.setText(_translate("MainWindow", "Close Cameras"))
        self.stopRecordingButton.setText(_translate("MainWindow", "Stop Recording"))
        self.directoryLabel.setText(_translate("MainWindow", "Directory"))
        self.camerasLabel.setText(_translate("MainWindow", "Cameras"))
        self.resolutionLabel_2.setText(_translate("MainWindow", "Resolution"))
        self.framerateLabel.setText(_translate("MainWindow", "Frame Rate"))
        self.simulationLabel.setText(_translate("MainWindow", "simulation"))
import resources_rc
