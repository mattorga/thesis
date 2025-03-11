import os
import toml
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal
from Pose2Sim import Pose2Sim
from utils.gait_classification import gait_classification
from poseConfiguration import Ui_Dialog
from PyQt5.QtWidgets import QDialog

class PoseConfigurationDialog(QDialog):
    def __init__(self, parent=None, session_path=None, trial_path=None, initial_config=None):
        super(PoseConfigurationDialog, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        # Store paths to update Config.toml and check process status
        self.session_path = session_path
        self.trial_path = trial_path
        
        # Connect radio buttons to page switching
        self.ui.openPoseButton.toggled.connect(self.onPoseButtonToggled)
        self.ui.rtmPoseButton.toggled.connect(self.onPoseButtonToggled)
        
        # Connect path buttons to file dialog handlers
        self.ui.openPosePathButton.clicked.connect(self.selectOpenPosePath)
        self.ui.modelPathButton.clicked.connect(self.selectModelPath)
        
        # Initialize paths
        self.openpose_path = ""
        self.model_path = ""
        self.algorithm = "openpose"  # Default algorithm
        
        # Set initial page to match default radio button (OpenPose)
        self.ui.poseEstimationPage.setCurrentIndex(0)
        
        # Apply initial configuration if provided
        if initial_config:
            self.apply_configuration(initial_config)
        else:
            # Otherwise, load any existing configuration
            self.loadConfiguration()
            
        # Update process status labels if trial_path is provided
        if self.trial_path:
            self.updateProcessStatus()
    
    def updateProcessStatus(self):
        """
        Check if each process has been completed by looking for specific files/folders
        and update the status labels accordingly.
        """
        if not self.trial_path or not os.path.exists(self.trial_path):
            return
            
        # Check for pose estimation (pose folder with JSON files)
        pose_dir = os.path.join(self.trial_path, "pose")
        if os.path.exists(pose_dir) and os.path.isdir(pose_dir):
            # Check for JSON files in the pose directory
            json_files = False
            for root, dirs, files in os.walk(pose_dir):
                if any(f.endswith('.json') for f in files):
                    json_files = True
                    break
                    
            if json_files:
                # The UI has no direct label for pose estimation status
                print(f"Pose estimation has been performed for {self.trial_path}")
            
        # Check for synchronization (pose-sync folder exists)
        sync_dir = os.path.join(self.trial_path, "pose-sync")
        if os.path.exists(sync_dir) and os.path.isdir(sync_dir) and len(os.listdir(sync_dir)) > 0:
            self.ui.syncPerformed.setText("Yes")
        else:
            self.ui.syncPerformed.setText("No")
            
        # Check for triangulation (pose-3d folder with .trc files)
        triangulation_dir = os.path.join(self.trial_path, "pose-3d")
        if os.path.exists(triangulation_dir) and os.path.isdir(triangulation_dir):
            trc_files = [f for f in os.listdir(triangulation_dir) if f.endswith('.trc')]
            if trc_files:
                self.ui.triangulationPerformed.setText("Yes")
            else:
                self.ui.triangulationPerformed.setText("No")
        else:
            self.ui.triangulationPerformed.setText("No")
            
        # Check for filtering (pose-3d folder with 'filt' in the filename of .trc files)
        if os.path.exists(triangulation_dir) and os.path.isdir(triangulation_dir):
            filt_files = [f for f in os.listdir(triangulation_dir) if f.endswith('.trc') and 'filt' in f]
            if filt_files:
                self.ui.filteringPerformed.setText("Yes")
            else:
                self.ui.filteringPerformed.setText("No")
        else:
            self.ui.filteringPerformed.setText("No")
            
        # Check for marker augmentation (pose-3d folder with 'LSTM' in the filename of .trc files)
        if os.path.exists(triangulation_dir) and os.path.isdir(triangulation_dir):
            lstm_files = [f for f in os.listdir(triangulation_dir) if f.endswith('.trc') and 'LSTM' in f]
            if lstm_files:
                self.ui.markerAugmentationPerformed.setText("Yes")
            else:
                self.ui.markerAugmentationPerformed.setText("No")
        else:
            self.ui.markerAugmentationPerformed.setText("No")
            
        # Check for kinematics (kinematics folder with .mot and .osim files)
        kinematics_dir = os.path.join(self.trial_path, "kinematics")
        if os.path.exists(kinematics_dir) and os.path.isdir(kinematics_dir):
            mot_files = [f for f in os.listdir(kinematics_dir) if f.endswith('.mot')]
            osim_files = [f for f in os.listdir(kinematics_dir) if f.endswith('.osim')]
            if mot_files and osim_files:
                self.ui.kinematicsPerformed.setText("Yes")
            else:
                self.ui.kinematicsPerformed.setText("No")
        else:
            self.ui.kinematicsPerformed.setText("No")
        
    def get_configuration(self):
        """
        Get the current configuration from the dialog, including the process checkboxes
        
        Returns:
            dict: Dictionary containing OpenPose configuration and process states
        """
        # Get OpenPose configuration
        config = {
            "algorithm": "rtmpose" if self.ui.rtmPoseButton.isChecked() else "openpose",
            "openpose_path": self.openpose_path,
            "model_path": self.model_path,
            # Add process checkbox states
            "pose_estimation": self.ui.poseEstimationCheck.isChecked(),
            "synchronization": self.ui.syncCheck.isChecked(),
            "triangulation": self.ui.triangulationCheck.isChecked(),
            "filtering": self.ui.filteringCheck.isChecked(),
            "marker_augmentation": self.ui.markerAugCheck.isChecked()
        }
        
        return config
            
    def apply_configuration(self, config):
        """Apply the provided configuration to the dialog"""
        # Set algorithm
        if config.get("algorithm") == "rtmpose":
            self.ui.rtmPoseButton.setChecked(True)
        else:
            self.ui.openPoseButton.setChecked(True)
        
        # Set paths
        if "openpose_path" in config and config["openpose_path"]:
            self.openpose_path = config["openpose_path"]
            self.ui.openPosePathLabel.setText(self.truncatePath(self.openpose_path))
            self.ui.openPosePathLabel.setToolTip(self.openpose_path)
        
        if "model_path" in config and config["model_path"]:
            self.model_path = config["model_path"]
            self.ui.modelPathLabel.setText(self.truncatePath(self.model_path))
            self.ui.modelPathLabel.setToolTip(self.model_path)
            
        # Set process checkboxes if provided
        if "pose_estimation" in config:
            self.ui.poseEstimationCheck.setChecked(config["pose_estimation"])
        
        if "synchronization" in config:
            self.ui.syncCheck.setChecked(config["synchronization"])
            
        if "triangulation" in config:
            self.ui.triangulationCheck.setChecked(config["triangulation"])
            
        if "filtering" in config:
            self.ui.filteringCheck.setChecked(config["filtering"])
            
        if "marker_augmentation" in config:
            self.ui.markerAugCheck.setChecked(config["marker_augmentation"])
            
    def get_configuration(self):
        """Get the current configuration from the dialog"""
        return {
            "algorithm": "rtmpose" if self.ui.rtmPoseButton.isChecked() else "openpose",
            "openpose_path": self.openpose_path,
            "model_path": self.model_path
        }
            
    def onPoseButtonToggled(self):
        """Switch the stacked widget page based on which radio button is selected"""
        if self.ui.openPoseButton.isChecked():
            self.ui.poseEstimationPage.setCurrentIndex(0)  # OpenPose configuration page
            self.algorithm = "openpose"
        else:
            self.ui.poseEstimationPage.setCurrentIndex(1)  # RTMPose configuration page
            self.algorithm = "rtmpose"
    
    def selectOpenPosePath(self):
        """Open a file dialog to select the OpenPose installation directory"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select OpenPose Directory",
            os.path.expanduser("~"),  # Start in home directory
            QFileDialog.ShowDirsOnly
        )
        
        if directory:
            self.openpose_path = directory
            self.ui.openPosePathLabel.setText(self.truncatePath(directory))
            self.ui.openPosePathLabel.setToolTip(directory)  # Show full path on hover
    
    def selectModelPath(self):
        """Open a file dialog to select the model directory"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Model Directory",
            os.path.expanduser("~"),  # Start in home directory
            QFileDialog.ShowDirsOnly
        )
        
        if directory:
            self.model_path = directory
            self.ui.modelPathLabel.setText(self.truncatePath(directory))
            self.ui.modelPathLabel.setToolTip(directory)  # Show full path on hover
    
    def truncatePath(self, path, max_length=25):
        """Truncate a path for display, keeping the beginning and end parts"""
        if len(path) <= max_length:
            return path
        
        # Keep first and last parts of the path
        first_part = path[:10]
        last_part = path[-15:]
        return f"{first_part}...{last_part}"
    
    def loadConfiguration(self):
        """Load existing configuration from both app config and openpose.toml"""
        try:
            # Look for app config file first
            app_config_file = os.path.join(os.path.expanduser("~"), ".gaitscape", "pose_config.toml")
            
            if os.path.exists(app_config_file):
                config = toml.load(app_config_file)
                
                # Load algorithm if it exists
                if "algorithm" in config:
                    self.algorithm = config["algorithm"]
                    if self.algorithm == "rtmpose":
                        self.ui.rtmPoseButton.setChecked(True)
                    else:
                        self.ui.openPoseButton.setChecked(True)
                
                # Load OpenPose path if it exists
                if "openpose_path" in config:
                    self.openpose_path = config["openpose_path"]
                    self.ui.openPosePathLabel.setText(self.truncatePath(self.openpose_path))
                    self.ui.openPosePathLabel.setToolTip(self.openpose_path)
                
                # Load model path if it exists
                if "model_path" in config:
                    self.model_path = config["model_path"]
                    self.ui.modelPathLabel.setText(self.truncatePath(self.model_path))
                    self.ui.modelPathLabel.setToolTip(self.model_path)
            
            # Now check if there's a session openpose.toml to override with
            if self.session_path:
                openpose_config_path = os.path.join(self.session_path, "openpose.toml")
                if os.path.exists(openpose_config_path):
                    openpose_config = toml.load(openpose_config_path)
                    
                    # Update OpenPose path if it exists and is not "none"
                    if "OpenPose_path" in openpose_config and openpose_config["OpenPose_path"] != "none":
                        self.openpose_path = openpose_config["OpenPose_path"]
                        self.ui.openPosePathLabel.setText(self.truncatePath(self.openpose_path))
                        self.ui.openPosePathLabel.setToolTip(self.openpose_path)
                    
                    # Update model path if it exists and is not "none"
                    if "model_path" in openpose_config and openpose_config["model_path"] != "none":
                        self.model_path = openpose_config["model_path"]
                        self.ui.modelPathLabel.setText(self.truncatePath(self.model_path))
                        self.ui.modelPathLabel.setToolTip(self.model_path)
        
        except Exception as e:
            print(f"Error loading configuration: {str(e)}")
    
    def saveConfiguration(self):
        """Save the current configuration to both app config and openpose.toml"""
        try:
            # Prepare the configuration dictionary
            config = self.get_configuration()
            
            # First, save to app config directory
            config_dir = os.path.join(os.path.expanduser("~"), ".gaitscape")
            os.makedirs(config_dir, exist_ok=True)
            
            config_file = os.path.join(config_dir, "pose_config.toml")
            
            # Save to app config file
            with open(config_file, "w") as f:
                toml.dump(config, f)
            
            # Next, update openpose.toml if a session path was provided
            if self.session_path:
                self.updateOpenposeToml()
        
        except Exception as e:
            QMessageBox.warning(
                self,
                "Configuration Error",
                f"Failed to save configuration: {str(e)}"
            )

    def updateOpenposeToml(self):
        """Update only the OpenPose_path and model_path in openpose.toml while preserving all other content"""
        if not self.session_path:
            return
                
        try:
            # Path to openpose.toml in the session directory
            openpose_config_path = os.path.join(self.session_path, "openpose.toml")
            
            # Check if openpose.toml already exists
            if os.path.exists(openpose_config_path):
                # Read the existing file content to preserve comments and other settings
                with open(openpose_config_path, 'r') as f:
                    content = f.read()
                
                # Update the OpenPose_path and model_path using regex
                import re
                
                # Update OpenPose_path
                openpose_pattern = r'(OpenPose_path\s*=\s*)(?:"[^"]*"|\'[^\']*\'|[^\s\n]+)'
                if re.search(openpose_pattern, content):
                    # Update existing value
                    content = re.sub(
                        openpose_pattern,
                        f'\\1\'{self.openpose_path or "none"}\'',
                        content
                    )
                else:
                    # Add the setting if it doesn't exist
                    content = f'OpenPose_path = \'{self.openpose_path or "none"}\'\n' + content
                
                # Update model_path
                model_pattern = r'(model_path\s*=\s*)(?:"[^"]*"|\'[^\']*\'|[^\s\n]+)'
                if re.search(model_pattern, content):
                    # Update existing value
                    content = re.sub(
                        model_pattern,
                        f'\\1\'{self.model_path or "none"}\'',
                        content
                    )
                else:
                    # Add the setting after OpenPose_path if it doesn't exist
                    openpose_path_line = re.search(r'OpenPose_path.*\n', content)
                    if openpose_path_line:
                        # Insert after the OpenPose_path line
                        insert_point = openpose_path_line.end()
                        content = content[:insert_point] + f'model_path = \'{self.model_path or "none"}\'\n' + content[insert_point:]
                    else:
                        # Add at the beginning if OpenPose_path wasn't found (shouldn't happen)
                        content = f'model_path = \'{self.model_path or "none"}\'\n' + content
            else:
                # Create a new openpose.toml with default settings if it doesn't exist
                content = f'''OpenPose_path = '{self.openpose_path or "none"}'
model_path = '{self.model_path or "none"}'
face = false
hand = false
net_resolution = "480x640" # default -1x368
model_pose = "BODY_25"
number_people_max = 5
'''
            
            # Write the updated content back to the file
            with open(openpose_config_path, 'w') as f:
                f.write(content)
                
            print(f"Updated openpose.toml at {openpose_config_path}")
            
            # Propagate the openpose.toml to participant and trial directories
            self.propagateOpenposeToml()
            
        except Exception as e:
            print(f"Error updating openpose.toml: {str(e)}")
            import traceback
            traceback.print_exc()

    def propagateOpenposeToml(self):
        """Copy the openpose.toml to participant and trial directories"""
        try:
            # Get the source openpose.toml path
            source_openpose_path = os.path.join(self.session_path, "openpose.toml")
            
            if not os.path.exists(source_openpose_path):
                print(f"Error: openpose.toml not found at {source_openpose_path}")
                return
                
            # Scan for participants in the session directory
            for participant_dir in [d for d in os.listdir(self.session_path) 
                                if os.path.isdir(os.path.join(self.session_path, d))]:
                
                participant_path = os.path.join(self.session_path, participant_dir)
                
                # Check if this is a participant directory (should start with P followed by numbers)
                if not (participant_dir.startswith('P') and participant_dir.split('_')[0][1:].isdigit()):
                    continue
                
                # Copy openpose.toml to participant directory
                participant_openpose_path = os.path.join(participant_path, "openpose.toml")
                import shutil
                shutil.copy2(source_openpose_path, participant_openpose_path)
                
                # Now copy to trial directories
                for trial_dir in [d for d in os.listdir(participant_path) 
                                if os.path.isdir(os.path.join(participant_path, d))]:
                    
                    # Check if this is a trial directory (should start with T followed by numbers)
                    if not (trial_dir.startswith('T') and trial_dir.split('_')[0][1:].isdigit()):
                        continue
                    
                    trial_path = os.path.join(participant_path, trial_dir)
                    trial_openpose_path = os.path.join(trial_path, "openpose.toml")
                    
                    shutil.copy2(source_openpose_path, trial_openpose_path)
        
        except Exception as e:
            print(f"Error propagating openpose.toml: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def accept(self):
        """Called when OK button is clicked"""
        # Validate paths before accepting
        if self.ui.openPoseButton.isChecked():
            if not self.openpose_path:
                QMessageBox.warning(
                    self,
                    "Validation Error",
                    "Please select an OpenPose path."
                )
                return
            
            if not self.model_path:
                QMessageBox.warning(
                    self,
                    "Validation Error",
                    "Please select a model path."
                )
                return
        
        # Save configuration before closing
        self.saveConfiguration()
        
        # Call parent accept method to close the dialog
        super().accept()


class ProcessThread(QThread):
    """Thread to handle processing operations without blocking the UI"""
    progress_update = pyqtSignal(str)
    process_complete = pyqtSignal(bool, str)
    
    def __init__(self, directory_manager):
        super().__init__()
        self.directory_manager = directory_manager
        self.should_stop = False
        
    def run(self):
        """Run the processing operations in a separate thread"""
        try:
            # Load configuration files
            participant_config_path = os.path.join(self.directory_manager.participant_path, "Config.toml")
            participant_config_dict = toml.load(participant_config_path)
            participant_config_dict.get("project").update({"project_dir": os.path.join(self.directory_manager.participant_path)})

            trial_config_path = os.path.join(self.directory_manager.trial_path, "Config.toml")
            trial_config_dict = toml.load(trial_config_path)
            trial_config_dict.get("project").update({"project_dir": self.directory_manager.trial_path})
            
            # Apply OpenPose configuration from directory manager
            self.apply_openpose_configuration(trial_config_dict)
            
            # Run the Pose2Sim pipeline
            self.progress_update.emit("Starting pose estimation...")
            Pose2Sim.poseEstimation(trial_config_dict)
            if self.should_stop:
                return
                
            self.progress_update.emit("Starting synchronization...")
            Pose2Sim.synchronization(trial_config_dict)
            if self.should_stop:
                return
                
            self.progress_update.emit("Starting triangulation...")
            Pose2Sim.triangulation(trial_config_dict)
            if self.should_stop:
                return
                
            self.progress_update.emit("Starting filtering...")
            Pose2Sim.filtering(trial_config_dict)
            if self.should_stop:
                return
                
            self.progress_update.emit("Starting marker augmentation...")
            Pose2Sim.markerAugmentation(trial_config_dict)
            if self.should_stop:
                return
                
            self.progress_update.emit("Starting kinematics...")
            Pose2Sim.kinematics(trial_config_dict)
            if self.should_stop:
                return
                
            self.progress_update.emit("Running gait classification...")
            gait_classification(self.directory_manager.trial_path)
            
            # Signal successful completion
            self.process_complete.emit(True, "Processing completed successfully.")
            
        except Exception as e:
            # Signal failure with error message
            self.process_complete.emit(False, f"Error during processing: {str(e)}")
    
    def apply_openpose_configuration(self, config_dict):
        """Apply OpenPose configuration from directory manager to the processing configuration"""
        try:
            # Get OpenPose configuration from directory manager
            openpose_path = self.directory_manager.openpose_path
            model_path = self.directory_manager.model_path
            algorithm = self.directory_manager.algorithm
            
            # Make sure the openpose section exists in config_dict
            if "openpose" not in config_dict:
                config_dict["openpose"] = {}
            
            # Update OpenPose section with paths
            if openpose_path:
                config_dict["openpose"]["OpenPose_path"] = openpose_path
            
            if model_path:
                config_dict["openpose"]["model_path"] = model_path
            
            # Make sure the pose_estimation section exists in config_dict
            if "pose_estimation" not in config_dict:
                config_dict["pose_estimation"] = {}
            
            # Update pose_estimation section with algorithm and paths
            config_dict["pose_estimation"]["algorithm"] = algorithm
            
            if openpose_path:
                config_dict["pose_estimation"]["openpose_path"] = openpose_path
            
            if model_path:
                config_dict["pose_estimation"]["model_path"] = model_path
            
            print(f"Applied OpenPose configuration: algorithm={algorithm}, openpose_path={openpose_path}, model_path={model_path}")
        
        except Exception as e:
            print(f"Error applying OpenPose configuration: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def stop(self):
        """Signal the thread to stop processing"""
        self.should_stop = True


class ProcessManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.process_thread = None
        self.configuration_dialog = None
        # Initialize default process configuration
        self.process_config = {
            'pose_estimation': True,
            'synchronization': True,
            'triangulation': True,
            'filtering': True,
            'marker_augmentation': True,
            'kinematics': True
        }
        
    def get_process_configuration(self):
        """
        Get the current process configuration
        
        Returns:
            dict: Dictionary containing process configuration settings
        """
        # Simply return the stored process configuration
        return self.process_config
    
    def update_process_status(self):
        """
        Update the process status labels in the configuration dialog if it's open
        """
        if self.configuration_dialog and hasattr(self.main_window, 'directory_manager'):
            trial_path = self.main_window.directory_manager.trial_path
            if trial_path:
                self.configuration_dialog.trial_path = trial_path
                self.configuration_dialog.updateProcessStatus()
    
    def open_configuration_dialog(self, openpose_config=None):
        """
        Open the pose configuration dialog
        
        Args:
            openpose_config (dict, optional): Current OpenPose configuration
        """
        # Pass the session path to the dialog so it can update the Config.toml file
        session_path = None
        trial_path = None
        if hasattr(self.main_window, 'directory_manager'):
            session_path = self.main_window.directory_manager.session_path
            trial_path = self.main_window.directory_manager.trial_path
            
        # Use provided config or get it from directory manager
        if openpose_config is None and hasattr(self.main_window, 'directory_manager'):
            openpose_config = self.main_window.directory_manager.get_openpose_config_dict()
            
        # Create the dialog and set its checkbox states from the current process_config
        self.configuration_dialog = PoseConfigurationDialog(
            self.main_window, 
            session_path, 
            trial_path,  # Pass trial_path to check process status
            openpose_config
        )
        
        # Apply our current process configuration to the dialog's checkboxes
        self.configuration_dialog.ui.poseEstimationCheck.setChecked(self.process_config['pose_estimation'])
        self.configuration_dialog.ui.syncCheck.setChecked(self.process_config['synchronization'])
        self.configuration_dialog.ui.triangulationCheck.setChecked(self.process_config['triangulation'])
        self.configuration_dialog.ui.filteringCheck.setChecked(self.process_config['filtering'])
        self.configuration_dialog.ui.markerAugCheck.setChecked(self.process_config['marker_augmentation'])
        self.configuration_dialog.ui.kinematicsCheck.setChecked(self.process_config['kinematics'])
        
        if self.configuration_dialog.exec_():
            # If dialog was accepted, get the updated configuration
            updated_config = self.configuration_dialog.get_configuration()
            
            # Update our stored process configuration
            self.process_config['pose_estimation'] = self.configuration_dialog.ui.poseEstimationCheck.isChecked()
            self.process_config['synchronization'] = self.configuration_dialog.ui.syncCheck.isChecked()
            self.process_config['triangulation'] = self.configuration_dialog.ui.triangulationCheck.isChecked()
            self.process_config['filtering'] = self.configuration_dialog.ui.filteringCheck.isChecked()
            self.process_config['marker_augmentation'] = self.configuration_dialog.ui.markerAugCheck.isChecked()
            self.process_config['kinematics'] = self.configuration_dialog.ui.kinematicsCheck.isChecked()
            
            # Save the updated OpenPose configuration using the directory manager
            if hasattr(self.main_window, 'directory_manager'):
                # Only pass the openpose-related config, not the process states
                openpose_only_config = {
                    "algorithm": updated_config.get("algorithm", "openpose"),
                    "openpose_path": updated_config.get("openpose_path", ""),
                    "model_path": updated_config.get("model_path", "")
                }
                self.main_window.directory_manager.save_openpose_config(openpose_only_config)
    
    def cleanup(self):
        """Clean up resources when the application is closing"""
        if self.process_thread and self.process_thread.isRunning():
            # Request the thread to stop
            self.process_thread.stop()
            
            # Wait for the thread to finish (with timeout)
            if not self.process_thread.wait(3000):  # 3 second timeout
                # If thread doesn't stop within timeout, terminate it forcefully
                self.process_thread.terminate()
                print("Warning: Process thread had to be terminated forcefully.")
        
        # Also clean up any dialog resources
        if self.configuration_dialog:
            self.configuration_dialog = None