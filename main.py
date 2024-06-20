from PyQt5.QtWidgets import (
    QApplication, QDialog, QWidget, QVBoxLayout, QPushButton, QListWidget,
    QListWidgetItem, QFileDialog, QMessageBox, QTabWidget, QToolTip, QLabel,
    QGridLayout, QMainWindow, QRadioButton,QHBoxLayout
)
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QEvent
import os
import sys
#import toml
import shutil
from modules import ui_filemanagement

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ui_filemanagement.FileManager()
    ex.show()
    sys.exit(app.exec_())