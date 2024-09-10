# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'thesis(3).ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSlider, QSpacerItem, QSpinBox,
    QStackedWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1230, 867)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.icon_widget = QWidget(self.centralwidget)
        self.icon_widget.setObjectName(u"icon_widget")
        self.icon_widget.setGeometry(QRect(10, 0, 281, 929))
        self.icon_widget.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(self.icon_widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.icon_widget)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(25)
        sizePolicy.setVerticalStretch(25)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QSize(100, 100))
        self.label.setPixmap(QPixmap(u":/resources/directions_walk_72dp_F0F0F0_FILL0_wght400_GRAD0_opsz20.png"))
        self.label.setScaledContents(True)

        self.verticalLayout.addWidget(self.label)

        self.verticalSpacer_2 = QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.home_button = QPushButton(self.icon_widget)
        self.home_button.setObjectName(u"home_button")
        self.home_button.setAutoFillBackground(False)
        self.home_button.setStyleSheet(u"QPushButton {\n"
"        border: none;\n"
"        background-color: transparent;\n"
"        color: black;\n"
"text-align: left;\n"
"    padding-left: 10px;\n"
"    }\n"
"    QPushButton:hover {\n"
"        background-color: #87CEEB; /* Optional: Light sky blue hover effect */\n"
"    }\n"
"	font: 75 8pt \"Microsoft JhengHei UI\";")
        icon = QIcon()
        icon.addFile(u"../../[QT Designer] Thesis UI/resources/home.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.home_button.setIcon(icon)
        self.home_button.setIconSize(QSize(40, 40))
        self.home_button.setCheckable(True)

        self.verticalLayout.addWidget(self.home_button)

        self.horizontalSpacer = QSpacerItem(256, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.verticalLayout.addItem(self.horizontalSpacer)

        self.cameras_button = QPushButton(self.icon_widget)
        self.cameras_button.setObjectName(u"cameras_button")
        self.cameras_button.setAutoFillBackground(False)
        self.cameras_button.setStyleSheet(u"QPushButton {\n"
"        border: none;\n"
"        background-color: transparent;\n"
"        color: black;\n"
"text-align: left;\n"
"    padding-left: 10px;\n"
"    }\n"
"    QPushButton:hover {\n"
"        background-color: #87CEEB; /* Optional: Light sky blue hover effect */\n"
"    }")
        icon1 = QIcon()
        icon1.addFile(u"../../[QT Designer] Thesis UI/resources/photo_camera_72dp_F0F0F0_FILL0_wght400_GRAD0_opsz48.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.cameras_button.setIcon(icon1)
        self.cameras_button.setIconSize(QSize(40, 40))
        self.cameras_button.setCheckable(True)

        self.verticalLayout.addWidget(self.cameras_button)

        self.horizontalSpacer_2 = QSpacerItem(256, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.verticalLayout.addItem(self.horizontalSpacer_2)

        self.dataviewer_button = QPushButton(self.icon_widget)
        self.dataviewer_button.setObjectName(u"dataviewer_button")
        self.dataviewer_button.setAutoFillBackground(False)
        self.dataviewer_button.setStyleSheet(u"QPushButton {\n"
"        border: none;\n"
"        background-color: transparent;\n"
"        color: black;\n"
"text-align: left;\n"
"    padding-left: 10px;\n"
"    }\n"
"    QPushButton:hover {\n"
"        background-color: #87CEEB; /* Optional: Light sky blue hover effect */\n"
"    }")
        icon2 = QIcon()
        icon2.addFile(u"../../[QT Designer] Thesis UI/resources/lists_72dp_F0F0F0_FILL0_wght400_GRAD0_opsz48.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.dataviewer_button.setIcon(icon2)
        self.dataviewer_button.setIconSize(QSize(40, 40))
        self.dataviewer_button.setCheckable(True)

        self.verticalLayout.addWidget(self.dataviewer_button)

        self.horizontalSpacer_3 = QSpacerItem(256, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.verticalLayout.addItem(self.horizontalSpacer_3)

        self.verticalSpacer = QSpacerItem(20, 238, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.activerecording_button_3 = QPushButton(self.icon_widget)
        self.activerecording_button_3.setObjectName(u"activerecording_button_3")
        self.activerecording_button_3.setAutoFillBackground(False)
        self.activerecording_button_3.setStyleSheet(u"QPushButton {\n"
"        border: none;\n"
"        background-color: transparent;\n"
"        color: black;\n"
"text-align: left;\n"
"    padding-left: 10px;\n"
"    }\n"
"    QPushButton:hover {\n"
"        background-color: #87CEEB; /* Optional: Light sky blue hover effect */\n"
"    }")
        icon3 = QIcon()
        icon3.addFile(u"../../[QT Designer] Thesis UI/resources/exittoapp.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.activerecording_button_3.setIcon(icon3)
        self.activerecording_button_3.setIconSize(QSize(40, 40))
        self.activerecording_button_3.setCheckable(True)

        self.verticalLayout.addWidget(self.activerecording_button_3)

        self.label_7 = QLabel(self.icon_widget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setStyleSheet(u"font: 150 12pt \"Microsoft YaHei UI\";\n"
"\n"
"color: #f0f0f0;\n"
"")

        self.verticalLayout.addWidget(self.label_7)

        self.horizontalSpacer_6 = QSpacerItem(256, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.verticalLayout.addItem(self.horizontalSpacer_6)

        self.frame_widget = QWidget(self.centralwidget)
        self.frame_widget.setObjectName(u"frame_widget")
        self.frame_widget.setGeometry(QRect(290, 0, 941, 121))
        self.frame_widget.setStyleSheet(u"")
        self.pushButton = QPushButton(self.frame_widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(10, 40, 93, 51))
        self.pushButton.setStyleSheet(u"QPushButton {\n"
"        border: none;\n"
"        background-color: transparent;\n"
"        color: white;\n"
"    }\n"
"    QPushButton:hover {\n"
"        background-color: #87CEEB; /* Optional: Light sky blue hover effect */\n"
"    }\n"
"	font: 75 8pt \"Microsoft JhengHei UI\";")
        icon4 = QIcon()
        icon4.addFile(u":/resources/menu.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.pushButton.setIcon(icon4)
        self.pushButton.setIconSize(QSize(60, 60))
        self.pushButton.setCheckable(True)
        self.label_2 = QLabel(self.frame_widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(120, 30, 611, 71))
        self.label_2.setStyleSheet(u"font: 75 26pt \"Microsoft JhengHei UI\";\n"
"color: black;")
        self.main_widget = QWidget(self.centralwidget)
        self.main_widget.setObjectName(u"main_widget")
        self.main_widget.setGeometry(QRect(290, 120, 941, 771))
        self.main_widget.setStyleSheet(u"")
        self.stackedWidget = QStackedWidget(self.main_widget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(0, 0, 931, 731))
        self.stackedWidget.setStyleSheet(u"QLineEdit {\n"
"    border: none;\n"
"    background-color: transparent;\n"
"    color: black;  /* Adjust the text color as needed */\n"
"    padding: 0;    /* Remove any padding if necessary */\n"
"}\n"
"")
        self.home_page = QWidget()
        self.home_page.setObjectName(u"home_page")
        self.home_page.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(self.home_page)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_2 = QFrame(self.home_page)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)

        self.verticalLayout_2.addWidget(self.frame_2)

        self.pushButton_2 = QPushButton(self.home_page)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setStyleSheet(u" QPushButton {\n"
"        background-color: #FFFFFF;  /* Darker shade */\n"
"        color: black\n"
";  /* Text color */\n"
"     \n"
"    }")

        self.verticalLayout_2.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.home_page)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setStyleSheet(u" QPushButton {\n"
"        background-color: #FFFFFF;  /* Darker shade */\n"
"        color: black\n"
";  /* Text color */\n"
"     \n"
"    }")

        self.verticalLayout_2.addWidget(self.pushButton_3)

        self.pushButton_13 = QPushButton(self.home_page)
        self.pushButton_13.setObjectName(u"pushButton_13")
        self.pushButton_13.setStyleSheet(u" QPushButton {\n"
"        background-color: #FFFFFF;  /* Darker shade */\n"
"        color: black\n"
";  /* Text color */\n"
"     \n"
"    }")

        self.verticalLayout_2.addWidget(self.pushButton_13)

        self.pushButton_4 = QPushButton(self.home_page)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setStyleSheet(u" QPushButton {\n"
"        background-color: #FFFFFF;  /* Darker shade */\n"
"        color: black\n"
";  /* Text color */\n"
"     \n"
"    }")

        self.verticalLayout_2.addWidget(self.pushButton_4)

        self.stackedWidget.addWidget(self.home_page)
        self.cameras_page = QWidget()
        self.cameras_page.setObjectName(u"cameras_page")
        self.verticalLayoutWidget = QWidget(self.cameras_page)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(70, 40, 201, 181))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.pushButton_5 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setStyleSheet(u" QPushButton {\n"
"        background-color: #FFFFFF;  /* Darker shade */\n"
"        color: black\n"
";  /* Text color */\n"
"     \n"
"    }")

        self.verticalLayout_3.addWidget(self.pushButton_5)

        self.pushButton_7 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setStyleSheet(u" QPushButton {\n"
"        background-color: #FFFFFF;  /* Darker shade */\n"
"        color: black\n"
";  /* Text color */\n"
"     \n"
"    }")

        self.verticalLayout_3.addWidget(self.pushButton_7)

        self.pushButton_8 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setStyleSheet(u" QPushButton {\n"
"        background-color: #FFFFFF;  /* Darker shade */\n"
"        color: black\n"
";  /* Text color */\n"
"     \n"
"    }")

        self.verticalLayout_3.addWidget(self.pushButton_8)

        self.pushButton_6 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setStyleSheet(u" QPushButton {\n"
"        background-color: #FFFFFF;  /* Darker shade */\n"
"        color: black\n"
";  /* Text color */\n"
"     \n"
"    }")

        self.verticalLayout_3.addWidget(self.pushButton_6)

        self.verticalLayoutWidget_2 = QWidget(self.cameras_page)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(70, 320, 221, 191))
        self.verticalLayout_4 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.checkBox = QCheckBox(self.verticalLayoutWidget_2)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setStyleSheet(u"")

        self.verticalLayout_4.addWidget(self.checkBox)

        self.checkBox_4 = QCheckBox(self.verticalLayoutWidget_2)
        self.checkBox_4.setObjectName(u"checkBox_4")
        self.checkBox_4.setStyleSheet(u"")

        self.verticalLayout_4.addWidget(self.checkBox_4)

        self.checkBox_3 = QCheckBox(self.verticalLayoutWidget_2)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setStyleSheet(u"")

        self.verticalLayout_4.addWidget(self.checkBox_3)

        self.checkBox_2 = QCheckBox(self.verticalLayoutWidget_2)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setStyleSheet(u"")

        self.verticalLayout_4.addWidget(self.checkBox_2)

        self.CharucoSquareSize = QSpinBox(self.cameras_page)
        self.CharucoSquareSize.setObjectName(u"CharucoSquareSize")
        self.CharucoSquareSize.setGeometry(QRect(240, 530, 61, 20))
        self.CharucoSquareSize.setStyleSheet(u"")
        self.label_3 = QLabel(self.cameras_page)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(70, 530, 161, 16))
        self.label_3.setStyleSheet(u"")
        self.verticalLayoutWidget_3 = QWidget(self.cameras_page)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(70, 570, 160, 80))
        self.verticalLayout_5 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.verticalLayoutWidget_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"")

        self.verticalLayout_5.addWidget(self.label_4)

        self.label_5 = QLabel(self.verticalLayoutWidget_3)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setStyleSheet(u"")

        self.verticalLayout_5.addWidget(self.label_5)

        self.label_6 = QLabel(self.verticalLayoutWidget_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setStyleSheet(u"")

        self.verticalLayout_5.addWidget(self.label_6)

        self.verticalLayoutWidget_4 = QWidget(self.cameras_page)
        self.verticalLayoutWidget_4.setObjectName(u"verticalLayoutWidget_4")
        self.verticalLayoutWidget_4.setGeometry(QRect(240, 570, 541, 82))
        self.verticalLayout_6 = QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_2 = QLineEdit(self.verticalLayoutWidget_4)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setStyleSheet(u"QLineEdit {\n"
"    border: none;\n"
"    background-color: transparent;\n"
"    color: black;  /* Adjust the text color as needed */\n"
"    padding: 0;    /* Remove any padding if necessary */\n"
"}\n"
"")

        self.verticalLayout_6.addWidget(self.lineEdit_2)

        self.lineEdit_3 = QLineEdit(self.verticalLayoutWidget_4)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setStyleSheet(u"QLineEdit {\n"
"    border: none;\n"
"    background-color: transparent;\n"
"    color: black;  /* Adjust the text color as needed */\n"
"    padding: 0;    /* Remove any padding if necessary */\n"
"}\n"
"")

        self.verticalLayout_6.addWidget(self.lineEdit_3)

        self.lineEdit = QLineEdit(self.verticalLayoutWidget_4)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setStyleSheet(u"QLineEdit {\n"
"    border: none;\n"
"    background-color: transparent;\n"
"    color: black;  /* Adjust the text color as needed */\n"
"    padding: 0;    /* Remove any padding if necessary */\n"
"}\n"
"")

        self.verticalLayout_6.addWidget(self.lineEdit)

        self.stackedWidget.addWidget(self.cameras_page)
        self.dataviewer_page = QWidget()
        self.dataviewer_page.setObjectName(u"dataviewer_page")
        self.pushButton_9 = QPushButton(self.dataviewer_page)
        self.pushButton_9.setObjectName(u"pushButton_9")
        self.pushButton_9.setGeometry(QRect(420, 610, 71, 28))
        self.pushButton_9.setStyleSheet(u" QPushButton {\n"
"        background-color: white;/* Darker shade */\n"
"        color: white;  /* Text color */\n"
"     \n"
"    }")
        icon5 = QIcon()
        icon5.addFile(u":/resources/pause_24dp_E8EAED_FILL0_wght400_GRAD0_opsz24.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon5.addFile(u":/resources/play_arrow_24dp_E8EAED_FILL0_wght400_GRAD0_opsz24.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        icon5.addFile(u"../thesis-FrontEnd/thesis-FrontEnd/resources/pause_24dp_E8EAED_FILL0_wght400_GRAD0_opsz24.png", QSize(), QIcon.Mode.Selected, QIcon.State.Off)
        icon5.addFile(u"../thesis-FrontEnd/thesis-FrontEnd/resources/play_arrow_24dp_E8EAED_FILL0_wght400_GRAD0_opsz24.png", QSize(), QIcon.Mode.Selected, QIcon.State.On)
        self.pushButton_9.setIcon(icon5)
        self.pushButton_9.setCheckable(True)
        self.pushButton_10 = QPushButton(self.dataviewer_page)
        self.pushButton_10.setObjectName(u"pushButton_10")
        self.pushButton_10.setGeometry(QRect(80, 610, 71, 28))
        self.pushButton_10.setStyleSheet(u" QPushButton {\n"
"        background-color: white; /* Darker shade */\n"
"        color: white;  /* Text color */\n"
"     \n"
"    }")
        icon6 = QIcon()
        icon6.addFile(u":/resources/fast_rewind_24dp_E8EAED_FILL0_wght400_GRAD0_opsz24.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_10.setIcon(icon6)
        self.pushButton_11 = QPushButton(self.dataviewer_page)
        self.pushButton_11.setObjectName(u"pushButton_11")
        self.pushButton_11.setGeometry(QRect(740, 610, 71, 28))
        self.pushButton_11.setStyleSheet(u" QPushButton {\n"
"        background-color: white;  /* Darker shade */\n"
"        color: white;  /* Text color */\n"
"     \n"
"    }")
        icon7 = QIcon()
        icon7.addFile(u"../thesis-FrontEnd/thesis-FrontEnd/resources/last_page_24dp_E8EAED_FILL0_wght400_GRAD0_opsz24.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_11.setIcon(icon7)
        self.horizontalSlider = QSlider(self.dataviewer_page)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setGeometry(QRect(80, 570, 731, 22))
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.graph = QWidget(self.dataviewer_page)
        self.graph.setObjectName(u"graph")
        self.graph.setGeometry(QRect(80, 70, 731, 491))
        self.label_8 = QLabel(self.dataviewer_page)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(80, 660, 141, 16))
        self.label_8.setStyleSheet(u"")
        self.lineEdit_4 = QLineEdit(self.dataviewer_page)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setGeometry(QRect(190, 660, 113, 22))
        self.stackedWidget.addWidget(self.dataviewer_page)
        self.directoryviewer_page = QWidget()
        self.directoryviewer_page.setObjectName(u"directoryviewer_page")
        self.pushButton_12 = QPushButton(self.directoryviewer_page)
        self.pushButton_12.setObjectName(u"pushButton_12")
        self.pushButton_12.setGeometry(QRect(30, 450, 199, 28))
        self.pushButton_12.setStyleSheet(u" QPushButton {\n"
"        background-color: #688DA4;  /* Darker shade */\n"
"        color: white;  /* Text color */\n"
"     \n"
"    }")
        self.label_9 = QLabel(self.directoryviewer_page)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(30, 500, 141, 16))
        self.label_9.setStyleSheet(u"color: white\n"
"")
        self.tableWidget_2 = QTableWidget(self.directoryviewer_page)
        if (self.tableWidget_2.columnCount() < 1):
            self.tableWidget_2.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, __qtablewidgetitem)
        self.tableWidget_2.setObjectName(u"tableWidget_2")
        self.tableWidget_2.setGeometry(QRect(20, 40, 891, 391))
        self.lineEdit_5 = QLineEdit(self.directoryviewer_page)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setGeometry(QRect(120, 500, 601, 22))
        self.stackedWidget.addWidget(self.directoryviewer_page)
        self.activerecording_page = QWidget()
        self.activerecording_page.setObjectName(u"activerecording_page")
        self.tableWidget = QTableWidget(self.activerecording_page)
        if (self.tableWidget.columnCount() < 3):
            self.tableWidget.setColumnCount(3)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem3)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(20, 30, 881, 521))
        self.stackedWidget.addWidget(self.activerecording_page)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.pushButton.toggled.connect(self.icon_widget.setHidden)
        self.activerecording_button_3.clicked.connect(MainWindow.close)

        self.stackedWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText("")
        self.home_button.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.cameras_button.setText(QCoreApplication.translate("MainWindow", u"Cameras", None))
        self.dataviewer_button.setText(QCoreApplication.translate("MainWindow", u"Data Viewer", None))
        self.activerecording_button_3.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.pushButton.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Markerless Gait Analysis", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"New Recording", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Load Recording", None))
        self.pushButton_13.setText(QCoreApplication.translate("MainWindow", u"Process", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Import Videos", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Start Motion Capture Recording", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"Stop Recording", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"Detect Available Cameras", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"Start Calibration Recording", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"Auto Process Videos on Save", None))
        self.checkBox_4.setText(QCoreApplication.translate("MainWindow", u"Generate Jupyter Notebook", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"Auto Open in Blender", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"Display Charuco Overlay", None))
#if QT_CONFIG(tooltip)
        self.CharucoSquareSize.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Charuco Square Size (mm)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.CharucoSquareSize.setWhatsThis(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Charuco Square Size (mm)</p><p><br/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Charuco Square Size (mm):", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Recording Name:", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Tag (Optional):", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Full Path:", None))
        self.pushButton_9.setText("")
        self.pushButton_10.setText("")
        self.pushButton_11.setText("")
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Frame Number:", None))
        self.pushButton_12.setText(QCoreApplication.translate("MainWindow", u"Show FreeMoCap Data Folder", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Session Path:", None))
        ___qtablewidgetitem = self.tableWidget_2.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Directory", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Recording Name", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Status", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Type", None));
    # retranslateUi

