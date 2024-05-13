from PyQt5.QtWidgets import (
    QApplication, QDialog, QWidget, QVBoxLayout, QPushButton, QListWidget,
    QListWidgetItem, QFileDialog, QMessageBox, QTabWidget, QToolTip, QLabel,
    QGridLayout, QMainWindow, QRadioButton,QHBoxLayout
)
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QEvent
import os
import sys
import toml
import shutil
from threading import *


# Evaluate 
from database.S00_V501.pose2sim import calibrate
from database.S00_V501.S00_P04_Yu.S00_P04_T01.simulation.opensim import simulate

#Add a separate class here for the OpenPose tab
# class OpenPose(QWidget):

class DataProcessor(QWidget):
    def __init__(self):
        super(DataProcessor, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 200)
        self.layout = QVBoxLayout(self)
        self.local_mode_radio = QRadioButton("Local Computing", self)
        self.cloud_mode_radio = QRadioButton("Cloud Computing", self)
        self.local_mode_radio.setChecked(True)
        self.layout.addWidget(self.local_mode_radio)
        self.layout.addWidget(self.cloud_mode_radio)
        self.process_button = QPushButton('Save Settings', self)
        self.process_button.clicked.connect(self.process_data)
        self.layout.addWidget(self.process_button)
        self.process_button.setFixedSize(120, 40) 

    def process_data(self):
        if self.process_button.isChecked():
            print("Cloud Computing Mode is used")
            QMessageBox.information(self, "Cloud Computing", "Cloud Computing Mode is used")
            #Add code here that uses cloud computing in the edit config popup window
        else:
            print("Local Computing Mode is used")
            QMessageBox.information(self, "Local Computing", "Local Computing Mode is used")
            #Add code here that uses local computing in the edit config popup window

class ConfigEditor(QDialog):
    def __init__(self, file_path=''):
        super().__init__()
        self.file_path = file_path
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Configuration Editor for Markerless Gait Analysis')
        self.setGeometry(300, 300, 600, 300)
        layout = QVBoxLayout()
        self.tabs = QTabWidget()
        project_tab = QWidget()
        processing_tab = DataProcessor()  
        opensim_tab = QWidget() #Modify this to Opensim Class
        self.tabs.addTab(project_tab, "Project")
        self.tabs.addTab(processing_tab, "Processing")  
        self.tabs.addTab(opensim_tab, "OpenSim")

       #Lines 60-73 may be modified to add functions for reading data from a toml file
        project_layout = QGridLayout()
        project_tab.setLayout(project_layout)
        frame_rate_label = QLabel('Frame rate:')
        self.frame_rate_display = QLabel('')  # Placeholder for frame rate value, add function here that displays these depending on the inputted toml file
        project_layout.addWidget(frame_rate_label, 0, 0)
        project_layout.addWidget(self.frame_rate_display, 0, 1)
        frame_range_label = QLabel('Frame range:')
        self.frame_range_display = QLabel('')  # Placeholder for frame range value, add function here that displays these depending on the inputted toml file
        project_layout.addWidget(frame_range_label, 1, 0)
        project_layout.addWidget(self.frame_range_display, 1, 1)
        self.info_button = QPushButton('i', self)
        self.info_button.setToolTip('Set n to limit processing frames')
        self.info_button.setFixedSize(15, 15)  # Set fixed size for a small circle
        self.info_button.setStyleSheet(
            "QPushButton {"
            "border-radius: 7px;"  # Half of width/height to make it circular
            "font-size: 8pt;"
            "padding: 2px;"
            "}"
        )
        self.info_button.setMouseTracking(True)
        self.info_button.installEventFilter(self)
        project_layout.addWidget(self.info_button, 1, 2, alignment=Qt.AlignRight)

        # Save button setup from Code 1
        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.saveConfig)
        layout.addWidget(self.tabs)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

    def eventFilter(self, source, event):
        # Event filter 
        if event.type() == QEvent.Enter and source is self.info_button:
            if self.tabs.currentIndex() == 0:
                QToolTip.showText(event.globalPos(), source.toolTip())
        elif event.type() == QEvent.Leave and source is self.info_button:
            QToolTip.hideText()
        return super().eventFilter(source, event)

    def saveConfig(self):
        # Save configuration 
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self,
                                                  "Save Configuration",
                                                  "",
                                                  "TOML Files (*.toml)",
                                                  options=options)
        if fileName:
            config = {'frame_rate': self.frame_rate_display.text(),
                      'frame_range': self.frame_range_display.text()}
            try:
                with open(fileName, 'w') as file:
                    toml.dump(config, file)
                QMessageBox.information(self, "Success", "File saved successfully.")
                self.accept()
            except Exception as e:
                QMessageBox.warning(self, "Save Error", f"An error occurred while saving the file: {e}")

    def loadConfig(self):
        # Load configuration 
        if os.path.exists(self.file_path):
            try:
                config = toml.load(self.file_path)
                self.frame_rate_display.setText(str(config.get('frame_rate', 'Unknown')))
                self.frame_range_display.setText(str(config.get('frame_range', 'Unknown')))
            except Exception as e:
                QMessageBox.warning(self, "Error", f"An error occurred while loading the file: {e}")
        else:
            QMessageBox.warning(self, "Error", "The configuration file does not exist.")

class FileManager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.currentPath = ''

    def initUI(self):
        self.setWindowTitle('File Management System for Markerless Gait Analysis')
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        self.fileList = QListWidget()
        self.browseButton = QPushButton('Browse Folder')
        self.openButton = QPushButton('Open')  # The "Open" button
        self.simulateButton = QPushButton('Simulate')
        self.calibrateButton = QPushButton('Calibrate')

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.browseButton)
        self.buttonLayout.addWidget(self.openButton)  # Add the "Open" button to the layout
        self.buttonLayout.addWidget(self.simulateButton)
        self.buttonLayout.addWidget(self.calibrateButton)

        self.layout.addWidget(self.fileList)
        self.layout.addLayout(self.buttonLayout)  # Add the button layout

        self.setLayout(self.layout)

        self.browseButton.clicked.connect(self.browseFolder)
        self.openButton.clicked.connect(self.openSelectedTOML)  # Connect the clicked signal to the new method
        self.simulateButton.clicked.connect(self.simulateSelected)
        self.calibrateButton.clicked.connect(self.calibrateSelected)
        self.fileList.itemDoubleClicked.connect(self.itemDoubleClicked)

    def browseFolder(self):
        folderPath = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folderPath:
            self.currentPath = folderPath
            self.listDirectoryContents(folderPath)

    def listDirectoryContents(self, folderPath):
        self.fileList.clear()
        self.fileList.addItem('../ [Folder]')  # Option to go up one directory
        allowed_extensions = ['.toml']
        dir_entries = sorted(os.listdir(folderPath))
        for entry in dir_entries:
            fullPath = os.path.join(folderPath, entry)
            if os.path.isdir(fullPath):
                item = QListWidgetItem(f'{entry} [Folder]')
                item.setForeground(QtCore.Qt.blue)
                self.fileList.addItem(item)
            elif entry.lower().endswith(tuple(allowed_extensions)):
                self.fileList.addItem(entry)

    def openSelectedTOML(self):
        selectedItems = self.fileList.selectedItems()
        if selectedItems:
            item = selectedItems[0]
            if item.text().lower().endswith('.toml'):
                editor = ConfigEditor(os.path.join(self.currentPath, item.text()))
                editor.loadConfig()
                editor.exec_()

    def simulateSelected(self):
        # Current path - path to simulation folder of the participant's trial
        simulate(self.currentPath)

    def calibrateSelected(self):
        # Current path - path to target session folder
        print(self.currentPath)
        calibrate(self.currentPath)
        
    def itemDoubleClicked(self, item):
        if '[Folder]' in item.text():
            folderName = item.text().replace(' [Folder]', '')
            if folderName == '..':
                self.currentPath = os.path.dirname(self.currentPath)  # Go up one directory
            else:
                self.currentPath = os.path.join(self.currentPath, folderName)
                self.listDirectoryContents(self.currentPath)
        elif item.text().lower().endswith('.toml'):
            self.openSelectedTOML()
    