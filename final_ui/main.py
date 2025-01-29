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
 
  # --- Page Changing Functions --- #
  def on_dashboardButton_clicked(self):
    self.ui.stackedWidget.setCurrentIndex(0)
  def on_camerasButton_clicked(self):
    self.ui.stackedWidget.setCurrentIndex(1)
  def on_simulationButton_clicked(self):
    self.ui.stackedWidget.setCurrentIndex(2)
  def on_jointAnalyticsButton_clicked(self):
    self.ui.stackedWidget.setCurrentIndex(3)
  
  # --- Cameras Page Functionality --- #
  def on_detectCamerasButton_clicked(self):
    self.camera_manager.detect_available_cameras()
  def on_closeCamerasButton_clicked(self):
    self.camera_manager.stop_all_cameras()
  def on_startRecordingButton_clicked(self):
    self.camera_manager.start_recording_all_cameras() # Not yet implemented
  
if __name__ == "__main__":
  app = QApplication(sys.argv)

  window = MainWindow()
  window.show()

  sys.exit(app.exec()) 