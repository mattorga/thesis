import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import os

from final import Ui_MainWindow

from camera_manager import Camera, CameraManager
from directory_manager import DirectoryManager

from patient_form import Ui_patient_form

class MainWindow(QMainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()
    
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    self.ui.stackedWidget.setCurrentIndex(0)
    
    self.camera_manager = CameraManager(self)
    self.directory_manager = DirectoryManager(self)

    self.setup_connections()
 
  # --- Page Changing Functions --- #
  # Note: Simple enough to not need signal/slot implementation
  def on_dashboardButton_clicked(self):
    self.ui.stackedWidget.setCurrentIndex(0)
  def on_camerasButton_clicked(self):
    self.ui.stackedWidget.setCurrentIndex(1)
  def on_simulationButton_clicked(self):
    self.ui.stackedWidget.setCurrentIndex(2)
  def on_jointAnalyticsButton_clicked(self):
    self.ui.stackedWidget.setCurrentIndex(3)

  # --- Exit Program --- #
  def on_exitButton_clicked(self):
    self.close()
  
  # --- Directory and Page Setup --- #
  def setup_connections(self):      
    # User Selection
    self.ui.sessionSelectButton.clicked.connect(self.on_select_session)
    self.ui.participantSelectButton.clicked.connect(self.select_participant)
    self.ui.trialSelectButton.clicked.connect(self.select_trial)

    # User Functions
    self.ui.participantAddButton.clicked.connect(self.add_participant)

    # Camera Page
    self.ui.detectCamerasButton.clicked.connect(self.detect_cameras)
    self.ui.closeCamerasButton.clicked.connect(self.close_cameras)
    self.ui.startRecordingButton.clicked.connect(self.start_recording)
    self.ui.stopRecordingButton.clicked.connect(self.stop_recording)

  # --- User Selection Functions --- #
  def on_select_session(self):
    self.directory_manager.set_session()
    session_name = self.directory_manager.get_session()
    
    # Update UI
    self.ui.sessionSelectedLabel.setText(session_name)
    self.ui.participantSelectButton.setEnabled(True)
    self.ui.participantAddButton.setEnabled(True)

    self.ui.sessionSelectedLabel.setText(session_name)
    self.ui.participantSelectButton.setEnabled(True)
    self.ui.participantAddButton.setEnabled(True)


  def select_participant(self):
    if not self.sessionDirectory:
        return
        
    dialog = QFileDialog(self)
    dialog.setFileMode(QFileDialog.Directory)
    dialog.setOption(QFileDialog.ShowDirsOnly, True)
    dialog.setDirectory(self.sessionDirectory)
    
    if dialog.exec_():
        selected_path = dialog.selectedFiles()[0]
        # Verify selected folder is directly under session folder
        if os.path.dirname(selected_path) == self.sessionDirectory:
            self.participantDirectory = selected_path
            participant_name = os.path.basename(selected_path)
            
            # Update UI
            self.ui.participantSelectedLabel.setText(participant_name)
            self.ui.trialSelectButton.setEnabled(True)
            self.ui.trialAddButton.setEnabled(True)

            print(self.participantDirectory)
            
            # Reset trial selection
            self.trialDirectory = None
            self.ui.trialSelectedLabel.setText("")
        else:
            QMessageBox.warning(self, "Invalid Selection", 
                              "Please select a participant folder directly under the session folder.")
  def select_trial(self):
    if not self.participantDirectory:
        return
        
    dialog = QFileDialog(self)
    dialog.setFileMode(QFileDialog.Directory)
    dialog.setOption(QFileDialog.ShowDirsOnly, True)
    dialog.setDirectory(self.participantDirectory)
    
    if dialog.exec_():
        selected_path = dialog.selectedFiles()[0]
        # Verify selected folder is directly under participant folder
        if os.path.dirname(selected_path) == self.participantDirectory:
            self.trialDirectory = selected_path
            trial_name = os.path.basename(selected_path)
            
            # Update UI
            self.ui.trialSelectedLabel.setText(trial_name)
            
            print(self.trialDirectory)

        else:
            QMessageBox.warning(self, "Invalid Selection", 
                              "Please select a trial folder directly under the participant folder.")
  def add_participant(self):
    dialog = QDialog(self)  # Create dialog with main window as parent
    form = Ui_patient_form()  # Create the form
    form.setupUi(dialog)  # Setup the form UI on the dialog
    
    # Show the dialog modally and get result
    if dialog.exec_() == QDialog.Accepted:
        first_name = form.firstNameField.text()
        last_name = form.lastNameField.text()
        height = form.heightField.text()
        weight = form.weightField.text()
        
  # --- Cameras Page functions --- #
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