import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from final import Ui_MainWindow
from camera_manager import Camera, CameraManager

class MainWindow(QMainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.ui.stackedWidget.setCurrentIndex(0)
    self.camera_manager = CameraManager(self)

    self.setup_connections()
 
  # --- Page Changing Functions --- #
  def on_dashboardButton_clicked(self):
    self.ui.stackedWidget.setCurrentIndex(0)
  def on_camerasButton_clicked(self):
    self.ui.stackedWidget.setCurrentIndex(1)
  def on_simulationButton_clicked(self):
    self.ui.stackedWidget.setCurrentIndex(2)
  def on_jointAnalyticsButton_clicked(self):
    self.ui.stackedWidget.setCurrentIndex(3)
  
  def setup_connections(self):      
    # Camera control connections
    self.ui.detectCamerasButton.clicked.connect(self.detect_cameras)
    self.ui.closeCamerasButton.clicked.connect(self.close_cameras)
    self.ui.startRecordingButton.clicked.connect(self.start_recording)
    self.ui.stopRecordingButton.clicked.connect(self.stop_recording)

  # Camera control handlers
  def detect_cameras(self):
    self.camera_manager.detect_available_cameras()
      
  def close_cameras(self):
    self.camera_manager.close_all_cameras()
      
  def start_recording(self):
    self.camera_manager.start_recording_all_cameras()
      
  def stop_recording(self):
    self.camera_manager.stop_recording_all_cameras()

if __name__ == "__main__":
  app = QApplication(sys.argv)

  window = MainWindow()
  window.show()

  sys.exit(app.exec()) 