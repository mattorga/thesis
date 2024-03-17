from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, 
    QListWidgetItem, QFileDialog, QMessageBox, QHBoxLayout
)
from PyQt5 import QtCore
import os
import sys
import shutil

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
        self.saveConfigButton = QPushButton('Save Config')
        self.createFolderButton = QPushButton('Create New Folder')
        self.deleteButton = QPushButton('Delete Selected')

        # New layout for buttons
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.browseButton)
        self.buttonLayout.addWidget(self.saveConfigButton)
        self.buttonLayout.addWidget(self.createFolderButton)
        self.buttonLayout.addWidget(self.deleteButton)

        self.layout.addWidget(self.fileList)
        self.layout.addLayout(self.buttonLayout)  # Add the button layout instead

        self.setLayout(self.layout)

        # Connect signals
        self.browseButton.clicked.connect(self.browseFolder)
        self.saveConfigButton.clicked.connect(self.saveConfig)
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
        allowed_extensions = ['.trc', '.mot', '.sto', '.mp4', '.toml']
        dir_entries = sorted(os.listdir(folderPath))  # Sort directory entries
        for entry in dir_entries:
            fullPath = os.path.join(folderPath, entry)
            if os.path.isdir(fullPath):
                item = QListWidgetItem(f'{entry} [Folder]')
                item.setForeground(QtCore.Qt.blue)  # Optional: Change color to distinguish folders
                self.fileList.addItem(item)
            elif any(entry.lower().endswith(ext) for ext in allowed_extensions):
                self.fileList.addItem(entry)

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
                        # Use shutil.rmtree to remove non-empty directories
                        shutil.rmtree(filePath)
                except OSError as e:
                    QMessageBox.warning(self, "Warning", f"Error deleting {itemName}: {e}")
            self.listDirectoryContents(self.currentPath)

    def saveConfig(self):
        # Ensure the config.toml is being saved after sorting folders alphabetically
        if self.currentPath and self.isSortedAlphabetically(self.currentPath):
            fileName, _ = QFileDialog.getSaveFileName(self, "Save Config", self.currentPath, "TOML files (*.toml)")
            if fileName:
                # Logic to save config.toml goes here
                # This is just a placeholder as an example
                with open(fileName, 'w') as file:
                    file.write("# Add your TOML configuration here")
                QMessageBox.information(self, "Success", "Config file saved successfully.")
        else:
            QMessageBox.warning(self, "Warning", "Please ensure the directory is sorted alphabetically by participant's name.")

    def isSortedAlphabetically(self, path):
        dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        return dirs == sorted(dirs)

    def itemDoubleClicked(self, item):
        if '[Folder]' in item.text():
            folderName = item.text().replace(' [Folder]', '')
            if folderName == '..':
                self.currentPath = os.path.dirname(self.currentPath)  # Go up one directory
            else:
                self.currentPath = os.path.join(self.currentPath, folderName)
            self.listDirectoryContents(self.currentPath)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileManager()
    ex.show()
    sys.exit(app.exec_())
