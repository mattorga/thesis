# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'final.ui'
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
        self.centralwidget.setObjectName("centralwidget")
        self.sidebar_full = QtWidgets.QWidget(self.centralwidget)
        self.sidebar_full.setGeometry(QtCore.QRect(0, 0, 195, 800))
        self.sidebar_full.setMinimumSize(QtCore.QSize(195, 800))
        self.sidebar_full.setMaximumSize(QtCore.QSize(195, 800))
        self.sidebar_full.setAutoFillBackground(False)
        self.sidebar_full.setObjectName("sidebar_full")
        self.Logo = QtWidgets.QLabel(self.sidebar_full)
        self.Logo.setGeometry(QtCore.QRect(70, 30, 71, 31))
        self.Logo.setObjectName("Logo")
        self.layoutWidget = QtWidgets.QWidget(self.sidebar_full)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 90, 143, 661))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.dashboardButton = QtWidgets.QPushButton(self.layoutWidget)
        self.dashboardButton.setDefault(False)
        self.dashboardButton.setFlat(False)
        self.dashboardButton.setObjectName("dashboardButton")
        self.verticalLayout.addWidget(self.dashboardButton)
        self.camerasButton = QtWidgets.QPushButton(self.layoutWidget)
        self.camerasButton.setObjectName("camerasButton")
        self.verticalLayout.addWidget(self.camerasButton)
        self.simulationButton = QtWidgets.QPushButton(self.layoutWidget)
        self.simulationButton.setObjectName("simulationButton")
        self.verticalLayout.addWidget(self.simulationButton)
        self.jointAnalyticsButton = QtWidgets.QPushButton(self.layoutWidget)
        self.jointAnalyticsButton.setObjectName("jointAnalyticsButton")
        self.verticalLayout.addWidget(self.jointAnalyticsButton)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(13, 368, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.exitBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.exitBtn.setObjectName("exitBtn")
        self.verticalLayout_2.addWidget(self.exitBtn)
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(210, 20, 1051, 761))
        self.stackedWidget.setObjectName("stackedWidget")
        self.dashboardPage = QtWidgets.QWidget()
        self.dashboardPage.setObjectName("dashboardPage")
        self.dashboardLabel = QtWidgets.QLabel(self.dashboardPage)
        self.dashboardLabel.setGeometry(QtCore.QRect(490, 300, 131, 61))
        self.dashboardLabel.setObjectName("dashboardLabel")
        self.stackedWidget.addWidget(self.dashboardPage)
        self.camerasPage = QtWidgets.QWidget()
        self.camerasPage.setObjectName("camerasPage")
        self.camera1Label = QtWidgets.QLabel(self.camerasPage)
        self.camera1Label.setGeometry(QtCore.QRect(90, 10, 391, 291))
        self.camera1Label.setAutoFillBackground(False)
        self.camera1Label.setStyleSheet("border: 3px solid black\n"
"")
        self.camera1Label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.camera1Label.setObjectName("camera1Label")
        self.camera2Label = QtWidgets.QLabel(self.camerasPage)
        self.camera2Label.setGeometry(QtCore.QRect(500, 10, 391, 291))
        self.camera2Label.setAutoFillBackground(False)
        self.camera2Label.setStyleSheet("border: 3px solid black\n"
"")
        self.camera2Label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.camera2Label.setObjectName("camera2Label")
        self.camera3Label = QtWidgets.QLabel(self.camerasPage)
        self.camera3Label.setGeometry(QtCore.QRect(290, 320, 391, 291))
        self.camera3Label.setAutoFillBackground(False)
        self.camera3Label.setStyleSheet("border: 3px solid black\n"
"")
        self.camera3Label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.camera3Label.setObjectName("camera3Label")
        self.detectCamerasButton = QtWidgets.QPushButton(self.camerasPage)
        self.detectCamerasButton.setGeometry(QtCore.QRect(90, 630, 161, 61))
        self.detectCamerasButton.setObjectName("detectCamerasButton")
        self.startRecordingButton = QtWidgets.QPushButton(self.camerasPage)
        self.startRecordingButton.setGeometry(QtCore.QRect(250, 630, 161, 61))
        self.startRecordingButton.setObjectName("startRecordingButton")
        self.closeCamerasButton = QtWidgets.QPushButton(self.camerasPage)
        self.closeCamerasButton.setGeometry(QtCore.QRect(90, 690, 161, 61))
        self.closeCamerasButton.setObjectName("closeCamerasButton")
        self.stopRecordingButton = QtWidgets.QPushButton(self.camerasPage)
        self.stopRecordingButton.setGeometry(QtCore.QRect(250, 690, 161, 61))
        self.stopRecordingButton.setObjectName("stopRecordingButton")
        self.directoryLabel = QtWidgets.QLabel(self.camerasPage)
        self.directoryLabel.setGeometry(QtCore.QRect(470, 650, 60, 16))
        self.directoryLabel.setObjectName("directoryLabel")
        self.camerasLabel = QtWidgets.QLabel(self.camerasPage)
        self.camerasLabel.setGeometry(QtCore.QRect(470, 670, 60, 16))
        self.camerasLabel.setObjectName("camerasLabel")
        self.resolutionLabel_2 = QtWidgets.QLabel(self.camerasPage)
        self.resolutionLabel_2.setGeometry(QtCore.QRect(470, 690, 71, 16))
        self.resolutionLabel_2.setObjectName("resolutionLabel_2")
        self.frameRateLabel = QtWidgets.QLabel(self.camerasPage)
        self.frameRateLabel.setGeometry(QtCore.QRect(470, 710, 71, 16))
        self.frameRateLabel.setObjectName("frameRateLabel")
        self.directoryValue = QtWidgets.QLabel(self.camerasPage)
        self.directoryValue.setGeometry(QtCore.QRect(550, 650, 60, 16))
        self.directoryValue.setObjectName("directoryValue")
        self.camerasValue = QtWidgets.QLabel(self.camerasPage)
        self.camerasValue.setGeometry(QtCore.QRect(550, 670, 60, 16))
        self.camerasValue.setObjectName("camerasValue")
        self.resolutionValue = QtWidgets.QLabel(self.camerasPage)
        self.resolutionValue.setGeometry(QtCore.QRect(550, 690, 60, 16))
        self.resolutionValue.setObjectName("resolutionValue")
        self.frameRateValue = QtWidgets.QLabel(self.camerasPage)
        self.frameRateValue.setGeometry(QtCore.QRect(550, 710, 60, 16))
        self.frameRateValue.setObjectName("frameRateValue")
        self.stackedWidget.addWidget(self.camerasPage)
        self.simulationPage = QtWidgets.QWidget()
        self.simulationPage.setObjectName("simulationPage")
        self.simulationLabel = QtWidgets.QLabel(self.simulationPage)
        self.simulationLabel.setGeometry(QtCore.QRect(440, 350, 131, 61))
        self.simulationLabel.setObjectName("simulationLabel")
        self.stackedWidget.addWidget(self.simulationPage)
        self.analyticsPage = QtWidgets.QWidget()
        self.analyticsPage.setObjectName("analyticsPage")
        self.analyticsLabel = QtWidgets.QLabel(self.analyticsPage)
        self.analyticsLabel.setGeometry(QtCore.QRect(430, 310, 131, 61))
        self.analyticsLabel.setObjectName("analyticsLabel")
        self.stackedWidget.addWidget(self.analyticsPage)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Logo.setText(_translate("MainWindow", "GaitScape"))
        self.dashboardButton.setText(_translate("MainWindow", "Dashboard"))
        self.camerasButton.setText(_translate("MainWindow", "Cameras"))
        self.simulationButton.setText(_translate("MainWindow", "3D Simulation"))
        self.jointAnalyticsButton.setText(_translate("MainWindow", "Joint Analytics"))
        self.exitBtn.setText(_translate("MainWindow", "Exit"))
        self.dashboardLabel.setText(_translate("MainWindow", "dashboard"))
        self.camera1Label.setText(_translate("MainWindow", "Camera 1"))
        self.camera2Label.setText(_translate("MainWindow", "Camera 2"))
        self.camera3Label.setText(_translate("MainWindow", "Camera 3"))
        self.detectCamerasButton.setText(_translate("MainWindow", "Detect Cameras"))
        self.startRecordingButton.setText(_translate("MainWindow", "Start Recording"))
        self.closeCamerasButton.setText(_translate("MainWindow", "Close Cameras"))
        self.stopRecordingButton.setText(_translate("MainWindow", "Stop Recording"))
        self.directoryLabel.setText(_translate("MainWindow", "Directory"))
        self.camerasLabel.setText(_translate("MainWindow", "Cameras"))
        self.resolutionLabel_2.setText(_translate("MainWindow", "Resolution"))
        self.frameRateLabel.setText(_translate("MainWindow", "Frame Rate"))
        self.directoryValue.setText(_translate("MainWindow", "-"))
        self.camerasValue.setText(_translate("MainWindow", "-"))
        self.resolutionValue.setText(_translate("MainWindow", "-"))
        self.frameRateValue.setText(_translate("MainWindow", "-"))
        self.simulationLabel.setText(_translate("MainWindow", "simulation"))
        self.analyticsLabel.setText(_translate("MainWindow", "analytics"))
