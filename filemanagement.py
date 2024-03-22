from PyQt5.QtWidgets import (
    QApplication, QDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QListWidget, QListWidgetItem, QFileDialog, QMessageBox, QTabWidget, QToolTip, QPushButton,
    QLabel, QGridLayout
)


from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QEvent
import os
import sys
import toml
import shutil


class ConfigEditor(QDialog):
    def __init__(self, file_path=''):
        super().__init__()
        self.file_path = file_path
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Configuration Editor for Markerless Gait Analysis')
        self.setGeometry(300, 300, 600, 300)
        
        layout = QVBoxLayout()  # Create the QVBoxLayout object

        # Tabs
        self.tabs = QTabWidget()  # Changed to instance attribute to access in eventFilter
        project_tab = QWidget()
        processing_tab = QWidget()
        opensim_tab = QWidget()

        self.tabs.addTab(project_tab, "Project")
        self.tabs.addTab(processing_tab, "Processing")
        self.tabs.addTab(opensim_tab, "OpenSim")

        # Project Tab Layout
        project_layout = QGridLayout()
        project_tab.setLayout(project_layout)

        # Frame rate display (not an input)
        frame_rate_label = QLabel('Frame rate:')
        self.frame_rate_display = QLabel('')  # Placeholder for frame rate value
        project_layout.addWidget(frame_rate_label, 0, 0)
        project_layout.addWidget(self.frame_rate_display, 0, 1)

        # Frame range display (not an input)
        frame_range_label = QLabel('Frame range:')
        self.frame_range_display = QLabel('')  # Placeholder for frame range value
        project_layout.addWidget(frame_range_label, 1, 0)
        project_layout.addWidget(self.frame_range_display, 1, 1)

        # Create info_button as a small circular button
        self.info_button = QPushButton('i', self)
        self.info_button.setToolTip('Set n to limit processing frames') ###Modify this when other codes are integrated
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
        
        # Position the button horizontally opposite the frame range display
        project_layout.addWidget(self.info_button, 1, 2, alignment=Qt.AlignRight)

        # Save button
        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.saveConfig)

        layout.addWidget(self.tabs)
        layout.addWidget(self.save_button)

        self.setLayout(layout)  # Apply the layout to the ConfigEditor dialog

    def eventFilter(self, source, event):
        if event.type() == QEvent.Enter and source is self.info_button:
            if self.tabs.currentIndex() == 0:  # Check if the current tab is "Project"
                QToolTip.showText(event.globalPos(), source.toolTip())
        elif event.type() == QEvent.Leave and source is self.info_button:
            QToolTip.hideText()
        return super().eventFilter(source, event)

    def saveConfig(self):
        # Open file dialog to choose where to save the file
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
                self.accept()  # Close the dialog
            except Exception as e:
                QMessageBox.warning(self, "Save Error", f"An error occurred while saving the file: {e}")
    def loadConfig(self):
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
        self.openButton = QPushButton('Open')  # The new "Open" button
        self.createFolderButton = QPushButton('Create New Folder')
        self.deleteButton = QPushButton('Delete Selected')

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.browseButton)
        self.buttonLayout.addWidget(self.openButton)  # Add the "Open" button to the layout
        self.buttonLayout.addWidget(self.createFolderButton)
        self.buttonLayout.addWidget(self.deleteButton)

        self.layout.addWidget(self.fileList)
        self.layout.addLayout(self.buttonLayout)  # Add the button layout

        self.setLayout(self.layout)

        self.browseButton.clicked.connect(self.browseFolder)
        self.openButton.clicked.connect(self.openSelectedTOML)  # Connect the clicked signal to the new method
        self.createFolderButton.clicked.connect(self.createFolder)
        self.deleteButton.clicked.connect(self.deleteSelected)
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

    def createFolder(self):
        if self.currentPath:
            folderName, ok = QFileDialog.getSaveFileName(self, "Create Folder", self.currentPath, "")
            if ok and folderName:
                os.makedirs(folderName, exist_ok=True)
                self.listDirectoryContents(self.currentPath)
        else:
            QMessageBox.warning(self, "Warning", "Please select a directory first.")

    def deleteSelected(self):
        selectedItems = self.fileList.selectedItems()
        if not selectedItems:
            QMessageBox.warning(self, "Warning", "No file selected for deletion.")
            return
        reply = QMessageBox.question(self, 'Delete Files', 'Are you sure you want to delete selected files?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for item in selectedItems:
                itemName = item.text().replace(' [Folder]', '')  # Remove the [Folder] tag if present
                filePath = os.path.join(self.currentPath, itemName)
                try:
                    if os.path.isfile(filePath):
                        os.remove(filePath)
                    elif os.path.isdir(filePath):
                        shutil.rmtree(filePath)
                except OSError as e:
                    QMessageBox.warning(self, "Warning", f"Error deleting {itemName}: {e}")
            self.listDirectoryContents(self.currentPath)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileManager()
    ex.show()
    sys.exit(app.exec_())
