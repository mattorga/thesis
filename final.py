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
        self.layoutWidget = QtWidgets.QWidget(self.sidebar_full)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 23, 181, 751))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.Logo = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setBold(True)
        font.setWeight(75)
        self.Logo.setFont(font)
        self.Logo.setAlignment(QtCore.Qt.AlignCenter)
        self.Logo.setObjectName("Logo")
        self.verticalLayout_4.addWidget(self.Logo)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout_4.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.mainMenu = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(10)
        self.mainMenu.setFont(font)
        self.mainMenu.setObjectName("mainMenu")
        self.verticalLayout.addWidget(self.mainMenu)
        self.camerasButton = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.camerasButton.setFont(font)
        self.camerasButton.setCheckable(False)
        self.camerasButton.setChecked(False)
        self.camerasButton.setObjectName("camerasButton")
        self.verticalLayout.addWidget(self.camerasButton)
        self.analyticsButton = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.analyticsButton.setFont(font)
        self.analyticsButton.setCheckable(False)
        self.analyticsButton.setChecked(False)
        self.analyticsButton.setObjectName("analyticsButton")
        self.verticalLayout.addWidget(self.analyticsButton)
        self.jointAnalyticsButton = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.jointAnalyticsButton.setFont(font)
        self.jointAnalyticsButton.setCheckable(False)
        self.jointAnalyticsButton.setChecked(False)
        self.jointAnalyticsButton.setObjectName("jointAnalyticsButton")
        self.verticalLayout.addWidget(self.jointAnalyticsButton)
        self.verticalLayout_4.addLayout(self.verticalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout_4.addItem(spacerItem1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.directoryMenu = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(10)
        self.directoryMenu.setFont(font)
        self.directoryMenu.setObjectName("directoryMenu")
        self.verticalLayout_2.addWidget(self.directoryMenu)
        self.sessionSelectButton = QtWidgets.QPushButton(self.layoutWidget)
        self.sessionSelectButton.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sessionSelectButton.sizePolicy().hasHeightForWidth())
        self.sessionSelectButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.sessionSelectButton.setFont(font)
        self.sessionSelectButton.setCheckable(False)
        self.sessionSelectButton.setChecked(False)
        self.sessionSelectButton.setObjectName("sessionSelectButton")
        self.verticalLayout_2.addWidget(self.sessionSelectButton)
        self.sessionSelectedLabel = QtWidgets.QLabel(self.layoutWidget)
        self.sessionSelectedLabel.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.sessionSelectedLabel.setFont(font)
        self.sessionSelectedLabel.setText("")
        self.sessionSelectedLabel.setObjectName("sessionSelectedLabel")
        self.verticalLayout_2.addWidget(self.sessionSelectedLabel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.participantSelectButton = QtWidgets.QPushButton(self.layoutWidget)
        self.participantSelectButton.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.participantSelectButton.setFont(font)
        self.participantSelectButton.setCheckable(False)
        self.participantSelectButton.setChecked(False)
        self.participantSelectButton.setObjectName("participantSelectButton")
        self.horizontalLayout.addWidget(self.participantSelectButton)
        self.participantAddButton = QtWidgets.QPushButton(self.layoutWidget)
        self.participantAddButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.participantAddButton.sizePolicy().hasHeightForWidth())
        self.participantAddButton.setSizePolicy(sizePolicy)
        self.participantAddButton.setCheckable(False)
        self.participantAddButton.setChecked(False)
        self.participantAddButton.setObjectName("participantAddButton")
        self.horizontalLayout.addWidget(self.participantAddButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.participantSelectedLabel = QtWidgets.QLabel(self.layoutWidget)
        self.participantSelectedLabel.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.participantSelectedLabel.setFont(font)
        self.participantSelectedLabel.setText("")
        self.participantSelectedLabel.setObjectName("participantSelectedLabel")
        self.verticalLayout_2.addWidget(self.participantSelectedLabel)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.trialSelectButton = QtWidgets.QPushButton(self.layoutWidget)
        self.trialSelectButton.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.trialSelectButton.setFont(font)
        self.trialSelectButton.setCheckable(False)
        self.trialSelectButton.setChecked(False)
        self.trialSelectButton.setObjectName("trialSelectButton")
        self.horizontalLayout_2.addWidget(self.trialSelectButton)
        self.trialAddButton = QtWidgets.QPushButton(self.layoutWidget)
        self.trialAddButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trialAddButton.sizePolicy().hasHeightForWidth())
        self.trialAddButton.setSizePolicy(sizePolicy)
        self.trialAddButton.setCheckable(False)
        self.trialAddButton.setChecked(False)
        self.trialAddButton.setObjectName("trialAddButton")
        self.horizontalLayout_2.addWidget(self.trialAddButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.trialSelectedLabel = QtWidgets.QLabel(self.layoutWidget)
        self.trialSelectedLabel.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.trialSelectedLabel.setFont(font)
        self.trialSelectedLabel.setText("")
        self.trialSelectedLabel.setObjectName("trialSelectedLabel")
        self.verticalLayout_2.addWidget(self.trialSelectedLabel)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout_4.addItem(spacerItem2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.processButton = QtWidgets.QPushButton(self.layoutWidget)
        self.processButton.setEnabled(False)
        self.processButton.setCheckable(False)
        self.processButton.setChecked(False)
        self.processButton.setObjectName("processButton")
        self.horizontalLayout_7.addWidget(self.processButton)
        self.processConfiguration = QtWidgets.QPushButton(self.layoutWidget)
        self.processConfiguration.setEnabled(False)
        self.processConfiguration.setMaximumSize(QtCore.QSize(50, 16777215))
        self.processConfiguration.setCheckable(False)
        self.processConfiguration.setChecked(False)
        self.processConfiguration.setObjectName("processConfiguration")
        self.horizontalLayout_7.addWidget(self.processConfiguration)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem3)
        self.exitButton = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.exitButton.setFont(font)
        self.exitButton.setCheckable(False)
        self.exitButton.setChecked(False)
        self.exitButton.setObjectName("exitButton")
        self.verticalLayout_4.addWidget(self.exitButton)
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(210, 30, 1051, 751))
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
"")
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
        font.setFamily("Helvetica")
        self.detectCamerasButton.setFont(font)
        self.detectCamerasButton.setObjectName("detectCamerasButton")
        self.startRecordingButton = QtWidgets.QPushButton(self.camerasPage)
        self.startRecordingButton.setGeometry(QtCore.QRect(250, 630, 161, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.startRecordingButton.setFont(font)
        self.startRecordingButton.setObjectName("startRecordingButton")
        self.closeCamerasButton = QtWidgets.QPushButton(self.camerasPage)
        self.closeCamerasButton.setGeometry(QtCore.QRect(90, 690, 161, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.closeCamerasButton.setFont(font)
        self.closeCamerasButton.setObjectName("closeCamerasButton")
        self.stopRecordingButton = QtWidgets.QPushButton(self.camerasPage)
        self.stopRecordingButton.setGeometry(QtCore.QRect(250, 690, 161, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.stopRecordingButton.setFont(font)
        self.stopRecordingButton.setObjectName("stopRecordingButton")
        self.directoryLabel = QtWidgets.QLabel(self.camerasPage)
        self.directoryLabel.setGeometry(QtCore.QRect(470, 650, 60, 16))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.directoryLabel.setFont(font)
        self.directoryLabel.setObjectName("directoryLabel")
        self.camerasLabel = QtWidgets.QLabel(self.camerasPage)
        self.camerasLabel.setGeometry(QtCore.QRect(470, 670, 60, 16))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.camerasLabel.setFont(font)
        self.camerasLabel.setObjectName("camerasLabel")
        self.resolutionLabel_2 = QtWidgets.QLabel(self.camerasPage)
        self.resolutionLabel_2.setGeometry(QtCore.QRect(470, 690, 71, 16))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.resolutionLabel_2.setFont(font)
        self.resolutionLabel_2.setObjectName("resolutionLabel_2")
        self.framerateLabel = QtWidgets.QLabel(self.camerasPage)
        self.framerateLabel.setGeometry(QtCore.QRect(470, 710, 71, 16))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.framerateLabel.setFont(font)
        self.framerateLabel.setObjectName("framerateLabel")
        self.directoryValue = QtWidgets.QLabel(self.camerasPage)
        self.directoryValue.setGeometry(QtCore.QRect(550, 650, 351, 16))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.directoryValue.setFont(font)
        self.directoryValue.setText("")
        self.directoryValue.setObjectName("directoryValue")
        self.camerasValue = QtWidgets.QLabel(self.camerasPage)
        self.camerasValue.setGeometry(QtCore.QRect(550, 670, 391, 16))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.camerasValue.setFont(font)
        self.camerasValue.setText("")
        self.camerasValue.setObjectName("camerasValue")
        self.resolutionValue = QtWidgets.QLabel(self.camerasPage)
        self.resolutionValue.setGeometry(QtCore.QRect(550, 690, 371, 16))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.resolutionValue.setFont(font)
        self.resolutionValue.setText("")
        self.resolutionValue.setObjectName("resolutionValue")
        self.framerateValue = QtWidgets.QLabel(self.camerasPage)
        self.framerateValue.setGeometry(QtCore.QRect(550, 710, 371, 16))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.framerateValue.setFont(font)
        self.framerateValue.setText("")
        self.framerateValue.setObjectName("framerateValue")
        self.stackedWidget.addWidget(self.camerasPage)
        self.simulationPage = QtWidgets.QWidget()
        self.simulationPage.setObjectName("simulationPage")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.simulationPage)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 1021, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.analyticsAllButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.analyticsAllButton.setEnabled(True)
        self.analyticsAllButton.setCheckable(True)
        self.analyticsAllButton.setChecked(True)
        self.analyticsAllButton.setObjectName("analyticsAllButton")
        self.horizontalLayout_3.addWidget(self.analyticsAllButton)
        self.analyticsHipButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.analyticsHipButton.setEnabled(True)
        self.analyticsHipButton.setCheckable(True)
        self.analyticsHipButton.setChecked(False)
        self.analyticsHipButton.setObjectName("analyticsHipButton")
        self.horizontalLayout_3.addWidget(self.analyticsHipButton)
        self.analyticsKneeButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.analyticsKneeButton.setEnabled(True)
        self.analyticsKneeButton.setCheckable(True)
        self.analyticsKneeButton.setObjectName("analyticsKneeButton")
        self.horizontalLayout_3.addWidget(self.analyticsKneeButton)
        self.analyticsAnkleButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.analyticsAnkleButton.setEnabled(True)
        self.analyticsAnkleButton.setCheckable(True)
        self.analyticsAnkleButton.setObjectName("analyticsAnkleButton")
        self.horizontalLayout_3.addWidget(self.analyticsAnkleButton)
        self.jointsTable = QtWidgets.QTableWidget(self.simulationPage)
        self.jointsTable.setEnabled(True)
        self.jointsTable.setGeometry(QtCore.QRect(530, 50, 501, 291))
        self.jointsTable.setObjectName("jointsTable")
        self.jointsTable.setColumnCount(0)
        self.jointsTable.setRowCount(0)
        self.trialChart = QtWidgets.QWidget(self.simulationPage)
        self.trialChart.setEnabled(True)
        self.trialChart.setGeometry(QtCore.QRect(529, 350, 501, 251))
        self.trialChart.setObjectName("trialChart")
        self.slider = QtWidgets.QSlider(self.simulationPage)
        self.slider.setGeometry(QtCore.QRect(10, 670, 1021, 22))
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName("slider")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.simulationPage)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 700, 1021, 41))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.rewindButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.rewindButton.setEnabled(True)
        self.rewindButton.setMinimumSize(QtCore.QSize(80, 0))
        self.rewindButton.setCheckable(False)
        self.rewindButton.setChecked(False)
        self.rewindButton.setObjectName("rewindButton")
        self.horizontalLayout_4.addWidget(self.rewindButton)
        self.fastForwardButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.fastForwardButton.setEnabled(True)
        self.fastForwardButton.setCheckable(False)
        self.fastForwardButton.setChecked(False)
        self.fastForwardButton.setObjectName("fastForwardButton")
        self.horizontalLayout_4.addWidget(self.fastForwardButton)
        self.speedLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.speedLabel.setEnabled(True)
        self.speedLabel.setMinimumSize(QtCore.QSize(40, 0))
        self.speedLabel.setMaximumSize(QtCore.QSize(40, 16777215))
        self.speedLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.speedLabel.setObjectName("speedLabel")
        self.horizontalLayout_4.addWidget(self.speedLabel)
        spacerItem4 = QtWidgets.QSpacerItem(140, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.pauseButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pauseButton.setEnabled(True)
        self.pauseButton.setCheckable(False)
        self.pauseButton.setChecked(False)
        self.pauseButton.setObjectName("pauseButton")
        self.horizontalLayout_4.addWidget(self.pauseButton)
        self.playButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.playButton.setEnabled(True)
        self.playButton.setCheckable(False)
        self.playButton.setChecked(False)
        self.playButton.setObjectName("playButton")
        self.horizontalLayout_4.addWidget(self.playButton)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.backButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.backButton.setEnabled(True)
        self.backButton.setCheckable(False)
        self.backButton.setChecked(False)
        self.backButton.setObjectName("backButton")
        self.horizontalLayout_4.addWidget(self.backButton)
        self.skipButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.skipButton.setEnabled(True)
        self.skipButton.setCheckable(False)
        self.skipButton.setChecked(False)
        self.skipButton.setObjectName("skipButton")
        self.horizontalLayout_4.addWidget(self.skipButton)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.simulationPage)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 620, 1021, 41))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.centerAnimationButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.centerAnimationButton.setEnabled(True)
        self.centerAnimationButton.setCheckable(True)
        self.centerAnimationButton.setObjectName("centerAnimationButton")
        self.horizontalLayout_6.addWidget(self.centerAnimationButton)
        self.axisButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.axisButton.setEnabled(True)
        self.axisButton.setCheckable(True)
        self.axisButton.setObjectName("axisButton")
        self.horizontalLayout_6.addWidget(self.axisButton)
        spacerItem6 = QtWidgets.QSpacerItem(250, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem6)
        self.gaitStageLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.gaitStageLabel.setEnabled(True)
        self.gaitStageLabel.setObjectName("gaitStageLabel")
        self.horizontalLayout_6.addWidget(self.gaitStageLabel)
        self.gaitStageValue = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.gaitStageValue.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gaitStageValue.sizePolicy().hasHeightForWidth())
        self.gaitStageValue.setSizePolicy(sizePolicy)
        self.gaitStageValue.setMinimumSize(QtCore.QSize(100, 0))
        self.gaitStageValue.setMaximumSize(QtCore.QSize(100, 16777215))
        self.gaitStageValue.setAlignment(QtCore.Qt.AlignCenter)
        self.gaitStageValue.setObjectName("gaitStageValue")
        self.horizontalLayout_6.addWidget(self.gaitStageValue)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem7)
        self.bothButton = QtWidgets.QRadioButton(self.horizontalLayoutWidget_3)
        self.bothButton.setEnabled(True)
        self.bothButton.setObjectName("bothButton")
        self.horizontalLayout_6.addWidget(self.bothButton)
        self.rightOnlyButton = QtWidgets.QRadioButton(self.horizontalLayoutWidget_3)
        self.rightOnlyButton.setEnabled(True)
        self.rightOnlyButton.setObjectName("rightOnlyButton")
        self.horizontalLayout_6.addWidget(self.rightOnlyButton)
        self.leftOnlyButton = QtWidgets.QRadioButton(self.horizontalLayoutWidget_3)
        self.leftOnlyButton.setEnabled(True)
        self.leftOnlyButton.setObjectName("leftOnlyButton")
        self.horizontalLayout_6.addWidget(self.leftOnlyButton)
        self.visualizationWidget = QtWidgets.QWidget(self.simulationPage)
        self.visualizationWidget.setEnabled(True)
        self.visualizationWidget.setGeometry(QtCore.QRect(10, 50, 501, 551))
        self.visualizationWidget.setObjectName("visualizationWidget")
        self.stackedWidget.addWidget(self.simulationPage)
        self.analyticsPage = QtWidgets.QWidget()
        self.analyticsPage.setObjectName("analyticsPage")
        self.baseTrialTable = QtWidgets.QTableWidget(self.analyticsPage)
        self.baseTrialTable.setGeometry(QtCore.QRect(10, 100, 431, 221))
        self.baseTrialTable.setObjectName("baseTrialTable")
        self.baseTrialTable.setColumnCount(0)
        self.baseTrialTable.setRowCount(0)
        self.versusTrialTable = QtWidgets.QTableWidget(self.analyticsPage)
        self.versusTrialTable.setGeometry(QtCore.QRect(10, 390, 431, 241))
        self.versusTrialTable.setObjectName("versusTrialTable")
        self.versusTrialTable.setColumnCount(0)
        self.versusTrialTable.setRowCount(0)
        self.baseTrialChart = QtWidgets.QWidget(self.analyticsPage)
        self.baseTrialChart.setGeometry(QtCore.QRect(450, 100, 581, 221))
        self.baseTrialChart.setObjectName("baseTrialChart")
        self.versusTrialChart = QtWidgets.QWidget(self.analyticsPage)
        self.versusTrialChart.setGeometry(QtCore.QRect(450, 390, 581, 241))
        self.versusTrialChart.setObjectName("versusTrialChart")
        self.comparativeSlider = QtWidgets.QSlider(self.analyticsPage)
        self.comparativeSlider.setGeometry(QtCore.QRect(10, 680, 1021, 22))
        self.comparativeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.comparativeSlider.setObjectName("comparativeSlider")
        self.baseGSLabel = QtWidgets.QLabel(self.analyticsPage)
        self.baseGSLabel.setGeometry(QtCore.QRect(590, 60, 90, 39))
        self.baseGSLabel.setObjectName("baseGSLabel")
        self.versusGSLabel = QtWidgets.QLabel(self.analyticsPage)
        self.versusGSLabel.setGeometry(QtCore.QRect(590, 350, 90, 39))
        self.versusGSLabel.setObjectName("versusGSLabel")
        self.baseTrialValue = QtWidgets.QLabel(self.analyticsPage)
        self.baseTrialValue.setGeometry(QtCore.QRect(90, 60, 151, 39))
        self.baseTrialValue.setObjectName("baseTrialValue")
        self.versusTrialValue = QtWidgets.QLabel(self.analyticsPage)
        self.versusTrialValue.setGeometry(QtCore.QRect(90, 350, 151, 39))
        self.versusTrialValue.setObjectName("versusTrialValue")
        self.baseTrialLabel = QtWidgets.QLabel(self.analyticsPage)
        self.baseTrialLabel.setGeometry(QtCore.QRect(10, 60, 71, 39))
        self.baseTrialLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.baseTrialLabel.setObjectName("baseTrialLabel")
        self.baseTrialLabel_2 = QtWidgets.QLabel(self.analyticsPage)
        self.baseTrialLabel_2.setGeometry(QtCore.QRect(10, 350, 71, 39))
        self.baseTrialLabel_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.baseTrialLabel_2.setObjectName("baseTrialLabel_2")
        self.newVerseButton = QtWidgets.QPushButton(self.analyticsPage)
        self.newVerseButton.setGeometry(QtCore.QRect(240, 350, 201, 41))
        self.newVerseButton.setObjectName("newVerseButton")
        self.layoutWidget1 = QtWidgets.QWidget(self.analyticsPage)
        self.layoutWidget1.setGeometry(QtCore.QRect(3, 20, 1031, 32))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.comparativeAllButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.comparativeAllButton.setCheckable(True)
        self.comparativeAllButton.setChecked(True)
        self.comparativeAllButton.setObjectName("comparativeAllButton")
        self.horizontalLayout_5.addWidget(self.comparativeAllButton)
        self.comparativeHipButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.comparativeHipButton.setEnabled(True)
        self.comparativeHipButton.setCheckable(True)
        self.comparativeHipButton.setChecked(False)
        self.comparativeHipButton.setObjectName("comparativeHipButton")
        self.horizontalLayout_5.addWidget(self.comparativeHipButton)
        self.comparativeKneeButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.comparativeKneeButton.setCheckable(True)
        self.comparativeKneeButton.setObjectName("comparativeKneeButton")
        self.horizontalLayout_5.addWidget(self.comparativeKneeButton)
        self.comparativeAnkleButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.comparativeAnkleButton.setCheckable(True)
        self.comparativeAnkleButton.setObjectName("comparativeAnkleButton")
        self.horizontalLayout_5.addWidget(self.comparativeAnkleButton)
        self.label = QtWidgets.QLabel(self.analyticsPage)
        self.label.setGeometry(QtCore.QRect(680, 70, 351, 16))
        self.label.setObjectName("label")
        self.label_5 = QtWidgets.QLabel(self.analyticsPage)
        self.label_5.setGeometry(QtCore.QRect(680, 360, 60, 16))
        self.label_5.setObjectName("label_5")
        self.stackedWidget.addWidget(self.analyticsPage)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Logo.setText(_translate("MainWindow", "GaitScape"))
        self.mainMenu.setText(_translate("MainWindow", "Main Menu"))
        self.camerasButton.setText(_translate("MainWindow", "Cameras"))
        self.analyticsButton.setText(_translate("MainWindow", "Simulation"))
        self.jointAnalyticsButton.setText(_translate("MainWindow", "Comparative"))
        self.directoryMenu.setText(_translate("MainWindow", "Directory"))
        self.sessionSelectButton.setText(_translate("MainWindow", "Session"))
        self.participantSelectButton.setText(_translate("MainWindow", "Participant"))
        self.participantAddButton.setText(_translate("MainWindow", "+"))
        self.trialSelectButton.setText(_translate("MainWindow", "Trial"))
        self.trialAddButton.setText(_translate("MainWindow", "+"))
        self.processButton.setText(_translate("MainWindow", "Process"))
        self.processConfiguration.setText(_translate("MainWindow", "..."))
        self.exitButton.setText(_translate("MainWindow", "Exit"))
        self.dashboardLabel.setText(_translate("MainWindow", "dashboard"))
        self.cameraSlot1.setText(_translate("MainWindow", "Camera 1"))
        self.cameraSlot2.setText(_translate("MainWindow", "Camera 2"))
        self.cameraSlot3.setText(_translate("MainWindow", "Camera 3"))
        self.detectCamerasButton.setText(_translate("MainWindow", "Detect Cameras"))
        self.startRecordingButton.setText(_translate("MainWindow", "Start Recording"))
        self.closeCamerasButton.setText(_translate("MainWindow", "Close Cameras"))
        self.stopRecordingButton.setText(_translate("MainWindow", "Stop Recording"))
        self.directoryLabel.setText(_translate("MainWindow", "Directory"))
        self.camerasLabel.setText(_translate("MainWindow", "Cameras"))
        self.resolutionLabel_2.setText(_translate("MainWindow", "Resolution"))
        self.framerateLabel.setText(_translate("MainWindow", "Frame Rate"))
        self.analyticsAllButton.setText(_translate("MainWindow", "All"))
        self.analyticsHipButton.setText(_translate("MainWindow", "Hip"))
        self.analyticsKneeButton.setText(_translate("MainWindow", "Knee"))
        self.analyticsAnkleButton.setText(_translate("MainWindow", "Ankle"))
        self.rewindButton.setText(_translate("MainWindow", "Speed Down"))
        self.fastForwardButton.setText(_translate("MainWindow", "Speed Up"))
        self.speedLabel.setText(_translate("MainWindow", "1x"))
        self.pauseButton.setText(_translate("MainWindow", "Pause"))
        self.playButton.setText(_translate("MainWindow", "Play"))
        self.backButton.setText(_translate("MainWindow", "Back"))
        self.skipButton.setText(_translate("MainWindow", "Skip"))
        self.centerAnimationButton.setText(_translate("MainWindow", "Center"))
        self.axisButton.setText(_translate("MainWindow", "Axis"))
        self.gaitStageLabel.setText(_translate("MainWindow", "Gait Stage: "))
        self.gaitStageValue.setText(_translate("MainWindow", "-"))
        self.bothButton.setText(_translate("MainWindow", "Both"))
        self.rightOnlyButton.setText(_translate("MainWindow", "Right"))
        self.leftOnlyButton.setText(_translate("MainWindow", "Left"))
        self.baseGSLabel.setText(_translate("MainWindow", "Gait Stage (°): "))
        self.versusGSLabel.setText(_translate("MainWindow", "Gait Stage (°): "))
        self.baseTrialValue.setText(_translate("MainWindow", "T00_antalgic"))
        self.versusTrialValue.setText(_translate("MainWindow", "-"))
        self.baseTrialLabel.setText(_translate("MainWindow", "Base Trial:"))
        self.baseTrialLabel_2.setText(_translate("MainWindow", "Versus:"))
        self.newVerseButton.setText(_translate("MainWindow", "Choose Verse"))
        self.comparativeAllButton.setText(_translate("MainWindow", "All"))
        self.comparativeHipButton.setText(_translate("MainWindow", "Hip"))
        self.comparativeKneeButton.setText(_translate("MainWindow", "Knee"))
        self.comparativeAnkleButton.setText(_translate("MainWindow", "Ankle"))
        self.label.setText(_translate("MainWindow", "Toe Off"))
        self.label_5.setText(_translate("MainWindow", "-"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
