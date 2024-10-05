import sys
import toml
import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication
from qt_material import apply_stylesheet

from Pose2Sim import Pose2Sim
from utils import pose2sim_custom
from ui_process import Ui_MainWindow

# Hardcoded for the meantime
root_path = "/Users/mattheworga/Documents/Git/DLSU/thesis/database"

session_folder = "S00_Demo-Batch"
participant_folder = "P00_Demo-man"
trial_folder = "T00_Trial"

session_config_path = os.path.join(root_path, session_folder, "Config.toml")
session_config_dict = toml.load(session_config_path)
session_config_dict.get("project").update({"project_dir":os.path.join(root_path, session_folder)})

trial_config_path = os.path.join(root_path, session_folder, participant_folder, trial_folder, "Config.toml")
trial_config_dict = toml.load(trial_config_path)
trial_config_dict.get("project").update({"project_dir":os.path.join(root_path, session_folder, participant_folder, trial_folder)})

class MainWindow(QMainWindow, Ui_MainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()
    self.setWindowTitle("Pose2Sim Processes")
    self.setupUi(self)
    self.initUI()
    self.click_count = 0

  def initUI(self):
    self.sessionFolderText.setText(session_folder)
    self.trialFolderText.setText(trial_folder)
  
    self.processButton.clicked.connect(lambda: pose2sim_custom.calibration(session_config_dict))

    self.poseEstimationButton.clicked.connect(lambda: pose2sim_custom.poseEstimation(trial_config_dict))
    self.synchronizationButton.clicked.connect(lambda: pose2sim_custom.synchronization(trial_config_dict))
    self.personAssociationButton.clicked.connect(lambda: Pose2Sim.personAssociation(trial_config_dict))
    self.triangulationButton.clicked.connect(lambda: Pose2Sim.triangulation(trial_config_dict))
    self.filteringButton.clicked.connect(lambda: Pose2Sim.filtering(trial_config_dict))
    self.markerAugmentationButton.clicked.connect(lambda: Pose2Sim.markerAugmentation(trial_config_dict))
    self.kinematicsButton.clicked.connect(lambda: Pose2Sim.kinematics(trial_config_dict))

    self.threadCheckButton.clicked.connect(self.handleThreadCheckButton)

  @pyqtSlot()
  def handleThreadCheckButton(self): 
    self.click_count += 1
    self.textEdit.append(f"{self.click_count}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWindow = MainWindow()

    apply_stylesheet(app, theme='dark_teal.xml')

    mainWindow.show()
    sys.exit(app.exec_())