import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Pose2Sim import Pose2Sim
import toml

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
    camera_slots = {
      0: self.ui.cameraSlot1,
      1: self.ui.cameraSlot2,
      2: self.ui.cameraSlot3
    }
    self.camera_manager.camera_slots = camera_slots
    
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
  
  # --- Directory, Page, Process Setup --- #
  def setup_connections(self):      
    # User Selection
    self.ui.sessionSelectButton.clicked.connect(self.on_select_session)
    self.ui.participantSelectButton.clicked.connect(self.on_select_participant)
    self.ui.trialSelectButton.clicked.connect(self.on_select_trial)

    # User Functions
    self.ui.participantAddButton.clicked.connect(self.add_participant)
    self.ui.trialAddButton.clicked.connect(self.add_trial)

    # Camera Page
    self.ui.detectCamerasButton.clicked.connect(self.on_detect_cameras)
    self.ui.closeCamerasButton.clicked.connect(self.on_close_cameras)
    self.ui.startRecordingButton.clicked.connect(self.on_start_recording)
    self.ui.stopRecordingButton.clicked.connect(self.on_stop_recording)

    # Process Button
    self.ui.processButton.clicked.connect(self.on_process)

  # --- User Selection Functions --- #
  def on_select_session(self):
    self.directory_manager.set_session()
    session_name = self.directory_manager.session_dir
    
    if session_name:
      # Update UI
      self.ui.sessionSelectedLabel.setText(session_name)

      self.ui.participantSelectedLabel.setText("")
      self.ui.participantSelectButton.setEnabled(True)
      self.ui.participantAddButton.setEnabled(True)

      self.ui.trialSelectedLabel.setText("")
      self.ui.trialSelectButton.setEnabled(False)
      self.ui.trialAddButton.setEnabled(False)

      self.ui.processButton.setEnabled(False)
  def on_select_participant(self):
    self.directory_manager.set_participant()
    participant_name = self.directory_manager.participant_dir
    
    if participant_name: 
      self.ui.participantSelectedLabel.setText(participant_name)
      self.ui.trialSelectButton.setEnabled(True)
      self.ui.trialAddButton.setEnabled(True)
  def on_select_trial(self):
    self.directory_manager.set_trial()
    trial_name = self.directory_manager.trial_dir

    if trial_name:
      self.ui.trialSelectedLabel.setText(trial_name)
      self.ui.processButton.setEnabled(True)
  def add_participant(self):
    self.directory_manager.add_participant()
  def add_trial(self):
    self.directory_manager.add_trial()

  # --- Cameras Page functions --- #
  def on_detect_cameras(self):
    self.camera_manager.detect_available_cameras()
    
    # Update UI elements
    self.ui.camerasValue.setText(str(self.camera_manager.camera_count))
    self.ui.framerateValue.setText(str(self.camera_manager.framerates))
  def on_close_cameras(self):
    self.camera_manager.close_all_cameras()
    self.ui.camerasValue.setText(str(self.camera_manager.camera_count))
  def on_start_recording(self):
    self.camera_manager.start_recording_all_cameras() 
  def on_stop_recording(self):
    self.camera_manager.stop_recording_all_cameras()

  def on_process(self):
    print(f"Process {self.directory_manager.trial_path}")

    session_config_path = os.path.join(self.directory_manager.session_path, "Config.toml")
    session_config_dict = toml.load(session_config_path)
    session_config_dict.get("project").update({"project_dir":os.path.join(self.directory_manager.session_path)})
    
    trial_config_path = os.path.join(self.directory_manager.trial_path, "Config.toml")
    trial_config_dict = toml.load(trial_config_path)
    trial_config_dict.get("project").update({"project_dir":self.directory_manager.trial_path})

    # Pose2Sim.calibration(session_config_dict) # Working
    # print("WORKING: Calibration")

    Pose2Sim.poseEstimation(trial_config_dict) # Working
    print("WORKING: Pose Estimation")
    Pose2Sim.synchronization(trial_config_dict)
    print("WORKING: Pose Synchronization")
    Pose2Sim.personAssociation(trial_config_dict)
    print("WORKING: Person Association")
    Pose2Sim.triangulation(trial_config_dict)
    print("WORKING: Triangulation")
    Pose2Sim.filtering(trial_config_dict)
    print("WORKING: Filtering")
    Pose2Sim.markerAugmentation(trial_config_dict)
    print("WORKING: Marker Augmentation")
    Pose2Sim.kinematics(trial_config_dict)
    print("WORKING: Kinematics")

if __name__ == "__main__":
  app = QApplication(sys.argv)

  window = MainWindow()
  window.show()

  sys.exit(app.exec()) 