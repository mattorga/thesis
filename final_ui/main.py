import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2

from final import Ui_MainWindow

class MainWindow(QMainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()

    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    self.ui.stackedWidget.setCurrentIndex(0)

    self.Worker1 = None
    self.Worker2 = None

  # Page Changing Functions
  def on_dashboardButton_clicked(self):
    self.ui.stackedWidget.setCurrentIndex(0)
  def on_camerasButton_clicked(self):
    self.ui.stackedWidget.setCurrentIndex(1)
  def on_simulationButton_clicked(self):
    self.ui.stackedWidget.setCurrentIndex(2)
  def on_jointAnalyticsButton_clicked(self):
    self.ui.stackedWidget.setCurrentIndex(3)

  # --- Cameras Page Functionality--- #
  def on_detectCamerasButton_clicked(self):
    if self.Worker1 is not None:
      self.Worker1.stop()
    if self.Worker2 is not None:
      self.Worker2.stop

    self.Worker1 = Worker(0)
    self.Worker1.start()
    self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot1)

    self.Worker2 = Worker(1)
    self.Worker2.start()
    self.Worker2.ImageUpdate.connect(self.ImageUpdateSlot2)

  def on_closeCamerasButton_clicked(self):
    self.Worker1.stop()
    self.Worker2.stop()

  def ImageUpdateSlot1(self, Image):
    self.ui.camera1Label.setPixmap(QPixmap.fromImage(Image))

  def ImageUpdateSlot2(self, Image):
    self.ui.camera2Label.setPixmap(QPixmap.fromImage(Image))

# Used in: Cameras Page
class Worker(QThread):
  def __init__(self, camera_number=0):
    super().__init__()
    self.camera_number = camera_number

  ImageUpdate = pyqtSignal(QImage)

  def run(self):
    self.ThreadActive = True
    Capture = cv2.VideoCapture(self.camera_number)
    while self.ThreadActive == True:
      ret, frame = Capture.read()
      if ret:
        Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FlippedImage = cv2.flip(Image, 1)
        ConvertToQtFormat = QImage(
          FlippedImage.data,            
          FlippedImage.shape[1], 
          FlippedImage.shape[0],
          QImage.Format_RGB888
        )
        Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
        self.ImageUpdate.emit(Pic)

  def stop(self):
    self.ThreadActive = False
    self.quit()

if __name__ == "__main__":
  app = QApplication(sys.argv)

  window = MainWindow()
  window.show()

  sys.exit(app.exec()) 