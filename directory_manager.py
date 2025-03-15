import os
import re
import toml
from datetime import datetime

from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDialog, QDialogButtonBox
from PyQt5.QtGui import QDoubleValidator

from patient_form import Ui_patient_form
from trial_form import Ui_trial_form

class TrialForm(QDialog):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.ui = Ui_trial_form()
    self.ui.setupUi(self)    

class PatientForm(QDialog):
  def __init__(self, parent=None):
      super().__init__(parent)
      self.ui = Ui_patient_form()
      self.ui.setupUi(self)
      
  def setup_validators(self):
      # Height validator (0.5m to 2.5m, 2 decimal places)
      height_validator = QDoubleValidator(0.5, 2.5, 2)
      self.ui.heightField.setValidator(height_validator)
      
      # Weight validator (20kg to 300kg, 1 decimal place)
      weight_validator = QDoubleValidator(20.0, 300.0, 1)
      self.ui.weightField.setValidator(weight_validator)
      
  def validate_and_accept(self):
      if self.validate_form():
          self.accept()
          
  def validate_form(self):
      # Validate first name
      first_name = self.ui.firstNameField.text().strip()
      if not first_name or not first_name.replace(" ", "").isalpha():
          QMessageBox.warning(self, "Validation Error", 
                            "First name must contain only letters.")
          return False
          
      # Validate last name
      last_name = self.ui.lastNameField.text().strip()
      if not last_name or not last_name.replace(" ", "").isalpha():
          QMessageBox.warning(self, "Validation Error", 
                            "Last name must contain only letters.")
          return False
          
      # Validate height
      height = self.ui.heightField.text()
      if not height or not 0.5 <= float(height) <= 2.5:
          QMessageBox.warning(self, "Validation Error", 
                            "Height must be between 0.5m and 2.5m.")
          return False
          
      # Validate weight
      weight = self.ui.weightField.text()
      if not weight or not 20.0 <= float(weight) <= 300.0:
          QMessageBox.warning(self, "Validation Error", 
                            "Weight must be between 20kg and 300kg.")
          return False
          
      return True

class DirectoryManager:
  def __init__(self, main_window):
    self.main_window = main_window
    self.base_path = os.path.join(os.path.expanduser("~"), "Documents", "GaitScape")
    
    self._session_path = None
    self._participant_path = None
    self._trial_path = None

    self._trial_name = None
    
    # OpenPose configuration paths and settings
    self._openpose_path = None
    self._model_path = None
    self._algorithm = "openpose"  # Default algorithm

  @property
  def trial_name(self):
     return self._trial_name
  @trial_name.setter
  def trial_name(self, trial_name):
     self._trial_name = trial_name

  # --- Path Properties --- #
  @property
  def session_path(self):
     return self._session_path
  @property
  def participant_path(self):
     return self._participant_path
  @property
  def trial_path(self):
     return self._trial_path

  # --- Setters --- #
  @session_path.setter
  def session_path(self, value):
    if value is not None and not os.path.exists(value):
      raise ValueError("Session path must exist")
    self._session_path = value
    self.participant_path = None
    self.trial_path = None
    
    # Update OpenPose configuration when session changes
    self._update_openpose_config()
  @participant_path.setter
  def participant_path(self, value):
      if value is not None and not os.path.exists(value):
        raise ValueError("Participant path must exist")
      self._participant_path = value
      self.trial_path = None
      
      # Update OpenPose configuration when participant changes
      self._update_openpose_config()
  @trial_path.setter
  def trial_path(self, value):
    if value is not None and not os.path.exists(value):
      raise ValueError("Trial path must exist")
    self._trial_path = value
    
    # Update OpenPose configuration when trial changes
    self._update_openpose_config()
     
  # --- Directory Properties --- #
  @property
  def session_dir(self):
      return os.path.basename(self._session_path) if self._session_path else None
  @property
  def participant_dir(self):
     return os.path.basename(self._participant_path) if self._participant_path else None
  @property
  def trial_dir(self):
     return os.path.basename(self._trial_path) if self._trial_path else None
     
  # --- OpenPose Properties --- #
  @property
  def openpose_path(self):
      """Get the configured OpenPose installation path"""
      return self._openpose_path
  @property
  def model_path(self):
      """Get the configured OpenPose model path"""
      return self._model_path
  @property
  def algorithm(self):
      """Get the configured pose estimation algorithm (openpose or rtmpose)"""
      return self._algorithm
     
  # --- OpenPose Configuration Methods --- #
  def _update_openpose_config(self):
      """Update OpenPose configuration by reading available TOML files"""
      # Reset paths first
      self._openpose_path = None
      self._model_path = None
      self._algorithm = "openpose"  # Default
      
      # Try loading from global configuration first (lowest priority)
      self._load_global_openpose_config()
      
      # Then try session level configuration (overrides global)
      if self._session_path:
          self._load_openpose_config(os.path.join(self._session_path, "openpose.toml"))
      
      # Then try participant level configuration (overrides session)
      if self._participant_path:
          self._load_openpose_config(os.path.join(self._participant_path, "openpose.toml"))
      
      # Finally try trial level configuration (highest priority)
      if self._trial_path:
          self._load_openpose_config(os.path.join(self._trial_path, "openpose.toml"))
  def _load_global_openpose_config(self):
      """Load OpenPose configuration from user's home directory"""
      config_file = os.path.join(os.path.expanduser("~"), ".gaitscape", "pose_config.toml")
      
      if os.path.exists(config_file):
          try:
              config = toml.load(config_file)
              
              # Update algorithm if it exists
              if "algorithm" in config:
                  self._algorithm = config["algorithm"]
              
              # Update paths if they exist
              if "openpose_path" in config and config["openpose_path"] not in (None, "none", ""):
                  self._openpose_path = config["openpose_path"]
              
              if "model_path" in config and config["model_path"] not in (None, "none", ""):
                  self._model_path = config["model_path"]
          except Exception as e:
              print(f"Error loading global OpenPose configuration: {str(e)}")
  def _load_openpose_config(self, config_path):
      """Load OpenPose configuration from specified path"""
      if os.path.exists(config_path):
          try:
              config = toml.load(config_path)
              
              # Update OpenPose path if it exists and is not "none"
              if "OpenPose_path" in config and config["OpenPose_path"] not in (None, "none", ""):
                  self._openpose_path = config["OpenPose_path"]
              
              # Update model path if it exists and is not "none"
              if "model_path" in config and config["model_path"] not in (None, "none", ""):
                  self._model_path = config["model_path"]
              
              # Some config files might use pose_estimation.algorithm instead
              if "pose_estimation" in config and "algorithm" in config["pose_estimation"]:
                  self._algorithm = config["pose_estimation"]["algorithm"]
                  
          except Exception as e:
              print(f"Error loading OpenPose configuration from {config_path}: {str(e)}")

  # --- Setter Methods --- #
  def set_session(self):
    gaitscape_path = self.base_path
    
    if not os.path.exists(gaitscape_path):
        os.makedirs(gaitscape_path)
    
    dialog = QFileDialog(self.main_window)
    dialog.setFileMode(QFileDialog.Directory)
    dialog.setOption(QFileDialog.ShowDirsOnly, True)
    dialog.setDirectory(gaitscape_path)
    
    if dialog.exec_():
        selected_path = dialog.selectedFiles()[0]
        # Normalize both paths for comparison
        normalized_selected_parent = os.path.normpath(os.path.dirname(selected_path)).lower()
        normalized_gaitscape = os.path.normpath(gaitscape_path).lower()
        
        if normalized_selected_parent == normalized_gaitscape:
            self.session_path = selected_path  # Uses the property setter
        else:
            QMessageBox.warning(self.main_window, "Invalid Selection", 
                            "Please select a session folder directly under GaitScape folder.")  
  def set_participant(self):
    dialog = QFileDialog(self.main_window)
    dialog.setFileMode(QFileDialog.Directory)
    dialog.setOption(QFileDialog.ShowDirsOnly, True)
    dialog.setDirectory(self._session_path)
    
    if dialog.exec_():
        selected_path =  dialog.selectedFiles()[0]
        if os.path.dirname(selected_path) == self._session_path:
          self.participant_path = selected_path
        else:
            QMessageBox.warning(self.main_window, "Invalid Selection", 
                              f"Please select a participant folder directly under {os.path.basename(self._session_path)} folder.")
  def set_trial(self):
    dialog = QFileDialog(self.main_window)
    dialog.setFileMode(QFileDialog.Directory)
    dialog.setOption(QFileDialog.ShowDirsOnly, True)
    dialog.setDirectory(self._participant_path)

    if dialog.exec_():
      selected_path = dialog.selectedFiles()[0]
      if os.path.dirname(selected_path) == self._participant_path:
        self.trial_path = selected_path
        
        self.trial_name = self.trial_dir.split("_",1)[1]

      else:
         QMessageBox.warning(self.main_window, "Invalid Selection", 
                              f"Please select a trial folder directly under {os.path.basename(self._participant_path)} folder.")

  # --- OpenPose Utility Methods --- #
  def get_openpose_config_dict(self):
      """
      Get the OpenPose configuration as a dictionary
      
      Returns:
          dict: Dictionary containing current OpenPose configuration
      """
      return {
          "algorithm": self._algorithm,
          "openpose_path": self._openpose_path,
          "model_path": self._model_path
      }
  def save_openpose_config(self, config_dict):
      """
      Save the provided OpenPose configuration to the appropriate level
      
      Args:
          config_dict (dict): Dictionary containing OpenPose configuration
      
      Returns:
          bool: True if successful, False otherwise
      """
      try:
          # Determine which level to save to (trial > participant > session)
          if self._trial_path:
              target_path = self._trial_path
          elif self._participant_path:
              target_path = self._participant_path
          elif self._session_path:
              target_path = self._session_path
          else:
              # No valid path, save to global configuration
              config_dir = os.path.join(os.path.expanduser("~"), ".gaitscape")
              os.makedirs(config_dir, exist_ok=True)
              
              config_file = os.path.join(config_dir, "pose_config.toml")
              
              with open(config_file, "w") as f:
                  toml.dump(config_dict, f)
              
              # Update local settings
              self._algorithm = config_dict.get("algorithm", self._algorithm)
              self._openpose_path = config_dict.get("openpose_path", self._openpose_path)
              self._model_path = config_dict.get("model_path", self._model_path)
              
              return True
          
          # If we have a valid path, save to openpose.toml in that directory
          openpose_config_path = os.path.join(target_path, "openpose.toml")
          
          # Check if openpose.toml already exists
          if os.path.exists(openpose_config_path):
              # Read the existing file to preserve comments and formatting
              with open(openpose_config_path, 'r') as f:
                  content = f.read()
              
              # Update the values using regex to preserve formatting
              openpose_path = config_dict.get("openpose_path", self._openpose_path)
              model_path = config_dict.get("model_path", self._model_path)
              
              # Update OpenPose_path
              openpose_pattern = r'(OpenPose_path\s*=\s*)(?:"[^"]*"|\'[^\']*\'|[^\s\n]+)'
              if re.search(openpose_pattern, content):
                  # Update existing value
                  content = re.sub(
                      openpose_pattern,
                      f'\\1\'{openpose_path or "none"}\'',
                      content
                  )
              else:
                  # Add the setting if it doesn't exist
                  content = f'OpenPose_path = \'{openpose_path or "none"}\'\n' + content
              
              # Update model_path
              model_pattern = r'(model_path\s*=\s*)(?:"[^"]*"|\'[^\']*\'|[^\s\n]+)'
              if re.search(model_pattern, content):
                  # Update existing value
                  content = re.sub(
                      model_pattern,
                      f'\\1\'{model_path or "none"}\'',
                      content
                  )
              else:
                  # Add the setting if it doesn't exist
                  content = content + f'\nmodel_path = \'{model_path or "none"}\''
          else:
              # Create a new openpose.toml with default settings
            content = f'''
                        OpenPose_path = '{config_dict.get("openpose_path", "none")}'
                        model_path = '{config_dict.get("model_path", "none")}'
                        '''
          
          # Write the updated content back to the file
          with open(openpose_config_path, 'w') as f:
              f.write(content)
          
          # Update local settings
          self._algorithm = config_dict.get("algorithm", self._algorithm)
          self._openpose_path = config_dict.get("openpose_path", self._openpose_path)
          self._model_path = config_dict.get("model_path", self._model_path)
          
          # Optionally, propagate changes to lower levels
          if target_path == self._session_path:
              self._propagate_openpose_config(openpose_config_path)
          
          return True
          
      except Exception as e:
          print(f"Error saving OpenPose configuration: {str(e)}")
          return False
  def _propagate_openpose_config(self, source_config_path):
      """
      Propagate the OpenPose configuration from session to participants and trials
      
      Args:
          source_config_path (str): Path to the source openpose.toml
      """
      try:
          if not os.path.exists(source_config_path):
              return
              
          # If source is in session dir, copy to all participants and their trials
          if os.path.dirname(source_config_path) == self._session_path:
              for participant_dir in [d for d in os.listdir(self._session_path) 
                                   if os.path.isdir(os.path.join(self._session_path, d))]:
                  
                  # Check if this is a participant directory
                  if not (participant_dir.startswith('P') and participant_dir.split('_')[0][1:].isdigit()):
                      continue
                  
                  participant_path = os.path.join(self._session_path, participant_dir)
                  participant_config_path = os.path.join(participant_path, "openpose.toml")
                  
                  # Copy to participant directory
                  import shutil
                  shutil.copy2(source_config_path, participant_config_path)
                  
                  # Copy to all trials in this participant
                  for trial_dir in [d for d in os.listdir(participant_path) 
                                  if os.path.isdir(os.path.join(participant_path, d))]:
                      
                      # Check if this is a trial directory
                      if not (trial_dir.startswith('T') and trial_dir.split('_')[0][1:].isdigit()):
                          continue
                      
                      trial_path = os.path.join(participant_path, trial_dir)
                      trial_config_path = os.path.join(trial_path, "openpose.toml")
                      
                      shutil.copy2(source_config_path, trial_config_path)
                      
          # If source is in participant dir, copy to all trials in that participant
          elif self._participant_path and os.path.dirname(source_config_path) == self._participant_path:
              for trial_dir in [d for d in os.listdir(self._participant_path) 
                              if os.path.isdir(os.path.join(self._participant_path, d))]:
                  
                  # Check if this is a trial directory
                  if not (trial_dir.startswith('T') and trial_dir.split('_')[0][1:].isdigit()):
                      continue
                  
                  trial_path = os.path.join(self._participant_path, trial_dir)
                  trial_config_path = os.path.join(trial_path, "openpose.toml")
                  
                  import shutil
                  shutil.copy2(source_config_path, trial_config_path)
                  
      except Exception as e:
          print(f"Error propagating OpenPose configuration: {str(e)}")

  # --- Adder Methods --- #
  def add_participant(self):
    if not self._session_path:
      QMessageBox.warning(self.main_window, "Error", 
                        "Please select a session first.")
      return
        
    dialog = PatientForm(self.main_window)
    dialog.setup_validators()  # Ensure validators are set up
    
    if dialog.exec_() == QDialog.Accepted:
        # Get the validated data
        first_name = dialog.ui.firstNameField.text().strip()
        last_name = dialog.ui.lastNameField.text().strip()
        height = float(dialog.ui.heightField.text())
        weight = float(dialog.ui.weightField.text())
      
        # Check if participant with same name exists
        existing_dirs = [d for d in os.listdir(self._session_path) 
                       if os.path.isdir(os.path.join(self._session_path, d))]
      
        # Check for name match regardless of P-number
        for dir_name in existing_dirs:
            parts = dir_name.split('_')
            if len(parts) >= 3:  # Ensure directory follows P##_LastName_FirstName format
                existing_last = parts[1]
                existing_first = parts[2]
                if existing_last.lower() == last_name.lower() and existing_first.lower() == first_name.lower():
                    QMessageBox.warning(self.main_window, "Error", 
                                      f"A participant with the name {first_name} {last_name} already exists.")
                    return
        
        # Find the next available participant number
        p_numbers = []
        for dir_name in existing_dirs:
            if dir_name.startswith('P'):
                try:
                    p_num = int(dir_name.split('_')[0][1:])
                    p_numbers.append(p_num)
                except (IndexError, ValueError):
                    continue
      
        # Get next P number
        next_p_num = 0 if not p_numbers else max(p_numbers) + 1
      
        # Create participant directory name with P number
        participant_dir = f"P{next_p_num:02d}_{last_name}_{first_name}"
        participant_path = os.path.join(self._session_path, participant_dir)
      
        try:
            # Create participant directory
            os.makedirs(participant_path)
              
            # Create and write to information file
            info_file_path = os.path.join(participant_path, "information.txt")
            with open(info_file_path, 'w') as f:
                f.write(f"Participant ID: P{next_p_num:02d}\n")
                f.write(f"First Name: {first_name}\n")
                f.write(f"Last Name: {last_name}\n")
                f.write(f"Height (m): {height:.2f}\n")
                f.write(f"Weight (kg): {weight:.1f}\n")
                f.write(f"BMI: {weight/(height*height):.1f}\n")
                f.write(f"Date Added: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            # Copy and modify Config.toml file from session folder to participant folder
            session_config_path = os.path.join(self._session_path, "Config.toml")
            if os.path.exists(session_config_path):
                # Copy the Config.toml file first to a temporary location
                participant_config_path = os.path.join(participant_path, "Config.toml")
                
                # Read the original file content while preserving all comments and formatting
                with open(session_config_path, 'r') as source_file:
                    config_content = source_file.read()
                
                # Replace the height values in the content using string replacement
                # This preserves all comments and formatting
                config_content = config_content.replace(
                    "participant_height = 'auto'", 
                    f"participant_height = {height:.2f}"
                )
                config_content = config_content.replace(
                    "default_height = 1.7", 
                    f"default_height = {height:.2f}"
                )
                
                # Write the modified content to the new file
                with open(participant_config_path, 'w') as dest_file:
                    dest_file.write(config_content)
                
                print(f"Copied and updated Config.toml with height {height:.2f}m for {participant_dir}")
            
            # Copy openpose.toml from session folder to participant folder if it exists
            session_openpose_path = os.path.join(self._session_path, "openpose.toml")
            if os.path.exists(session_openpose_path):
                import shutil
                participant_openpose_path = os.path.join(participant_path, "openpose.toml")
                shutil.copy2(session_openpose_path, participant_openpose_path)
                print(f"Copied openpose.toml to {participant_dir}")
            
            # Copy calibration folder contents from session folder to participant folder
            session_calibration_path = os.path.join(self._session_path, "calibration")
            if os.path.exists(session_calibration_path) and os.path.isdir(session_calibration_path):
                import shutil
                participant_calibration_path = os.path.join(participant_path, "calibration")
                
                # Create the calibration directory in the participant folder
                os.makedirs(participant_calibration_path, exist_ok=True)
                
                # Copy all files from calibration folder
                for item in os.listdir(session_calibration_path):
                    source_item = os.path.join(session_calibration_path, item)
                    target_item = os.path.join(participant_calibration_path, item)
                    
                    if os.path.isdir(source_item):
                        shutil.copytree(source_item, target_item)
                        print(f"Copied calibration subfolder {item} to {participant_dir}")
                    else:
                        shutil.copy2(source_item, target_item)
                        print(f"Copied calibration file {item} to {participant_dir}")
                
                print(f"Copied calibration folder to {participant_dir}")
                          
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", 
                              f"Failed to create participant: {str(e)}")
            if os.path.exists(participant_path):
                try:
                    import shutil
                    shutil.rmtree(participant_path)
                except Exception as cleanup_error:
                    print(f"Failed to clean up after error: {str(cleanup_error)}")
  def add_trial(self):
    if not self._participant_path:
        QMessageBox.warning(self.main_window, "Error", 
                          "Please select a participant first.")
        return
          
    dialog = TrialForm(self.main_window)

    if dialog.exec_() == QDialog.Accepted:
        trial_name = dialog.ui.trialNameField.text().strip()
        
        # Check if name is empty
        if not trial_name:
            QMessageBox.warning(self.main_window, "Error", 
                              "Trial name cannot be empty.")
            return
        
        # Check for existing trials with the same name
        existing_dirs = [d for d in os.listdir(self._participant_path) 
                        if os.path.isdir(os.path.join(self._participant_path, d))]
        
        # Find the next available trial number
        t_numbers = []
        for dir_name in existing_dirs:
            if dir_name.startswith('T'):
                try:
                    t_num = int(dir_name.split('_')[0][1:])
                    t_numbers.append(t_num)
                except (IndexError, ValueError):
                    continue
        
        # Get next T number
        next_t_num = 0 if not t_numbers else max(t_numbers) + 1
        
        # Create trial directory name with T number
        trial_dir = f"T{next_t_num:02d}_{trial_name}"
        trial_path = os.path.join(self._participant_path, trial_dir)
        
        try:
            # Create trial directory
            os.makedirs(trial_path)
            
            # Copy Config.toml file from participant folder to trial folder
            participant_config_path = os.path.join(self._participant_path, "Config.toml")
            
            if os.path.exists(participant_config_path):
                import shutil
                
                # Copy the Config.toml file to the trial folder
                trial_config_path = os.path.join(trial_path, "Config.toml")
                shutil.copy2(participant_config_path, trial_config_path)
                print(f"Copied Config.toml to trial folder {trial_dir}")
            else:
                print(f"Warning: Config.toml not found in participant folder {os.path.basename(self._participant_path)}")
            
            # Copy openpose.toml file from participant folder to trial folder if it exists
            participant_openpose_path = os.path.join(self._participant_path, "openpose.toml")
            if os.path.exists(participant_openpose_path):
                import shutil
                trial_openpose_path = os.path.join(trial_path, "openpose.toml")
                shutil.copy2(participant_openpose_path, trial_openpose_path)
                print(f"Copied openpose.toml to trial folder {trial_dir}")
                
            # Set the trial path and name
            self.trial_path = trial_path
            self.trial_name = trial_name
            
            # Update UI if needed
            if hasattr(self.main_window, 'ui'):
                self.main_window.ui.trialSelectedLabel.setText(trial_dir)
                
            QMessageBox.information(self.main_window, "Success", 
                                 f"Trial '{trial_name}' created successfully.")
                
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", 
                              f"Failed to create trial: {str(e)}")
            if os.path.exists(trial_path):
                try:
                    import shutil
                    shutil.rmtree(trial_path)
                except Exception as cleanup_error:
                    print(f"Failed to clean up after error: {str(cleanup_error)}")

  # --- File Retrievers --- #
  def find_motion_csv_file(self):
    """
    Finds the path to the processed gait classification CSV file for the current trial.

    Returns:
        str or None: Path to the motion data file if found, None otherwise
    """
    if not self._trial_path:
        print("Warning: No trial path set, cannot find motion data file")
        return None
        
    try:
        # Construct expected path to the classification file (original angles)
        gait_class_dir = os.path.join(self._trial_path, "gait-classification")
        
        # Ensure the directory exists
        if not os.path.exists(gait_class_dir):
            # print(f"Warning: Gait classification directory not found at {gait_class_dir}")
            return None
        
        # Look for the CSV file with trial name in it
        csv_files = [f for f in os.listdir(gait_class_dir) if f.endswith('_original.csv')]
        
        if csv_files:
            # Use the first CSV file found
            file_path = os.path.join(gait_class_dir, csv_files[0])
            return file_path
        else:
            print(f"Warning: No CSV files found in {gait_class_dir}")
            return None
            
    except Exception as e:
        print(f"Error finding motion data file: {str(e)}")
        return None
  def find_reference_csv_file(self):
    """
    Finds a reference/normal gait pattern file for comparison.

    Returns:
        str or None: Path to the reference data file if found, None otherwise
    """
    if not self._session_path:
        print("Warning: No session path set, cannot find reference data file")
        return None
        
    try:
        # Look for a reference directory in the session folder
        reference_dir = os.path.join(self._session_path, "reference")
        
        if os.path.exists(reference_dir):
            csv_files = [f for f in os.listdir(reference_dir) if f.endswith('.csv')]
            
            if csv_files:
                # Use the first reference file found
                file_path = os.path.join(reference_dir, csv_files[0])
                print(f"Found reference data file: {file_path}")
                return file_path
        
        return None
    except Exception as e:
        print(f"Error finding reference data file: {str(e)}")
        return None 
            
  def find_motion_mot_file(self):
    """
    Finds the path to the MOT file in the kinematics directory for the current trial.
    
    Returns:
        str or None: Path to the motion MOT file if found, None otherwise
    """
    if not self._trial_path:
        print("Warning: No trial path set, cannot find motion MOT file")
        return None
        
    try:
        # Construct expected path to the kinematics directory
        kinematics_dir = os.path.join(self._trial_path, "kinematics")
        
        # Ensure the directory exists
        if not os.path.exists(kinematics_dir):
            print(f"Warning: Kinematics directory not found at {kinematics_dir}")
            return None
        
        # Look for MOT files in the kinematics directory
        mot_files = [f for f in os.listdir(kinematics_dir) if f.endswith('.mot')]
        
        if mot_files:
            # Use the first MOT file found
            file_path = os.path.join(kinematics_dir, mot_files[0])
            return file_path
        else:
            print(f"Warning: No MOT files found in {kinematics_dir}")
            return None
            
    except Exception as e:
        print(f"Error finding motion MOT file: {str(e)}")
        return None
  def find_reference_mot_file(self, selected_path=None):
    """
    Finds a reference/normal gait pattern MOT file for comparison.
    
    Args:
        selected_path (str, optional): Path selected from the newVerseButton dialog.
            If None, tries to find a default reference file.
    
    Returns:
        str or None: Path to the reference MOT file if found, None otherwise
    """
    try:
        # If a specific path was provided (from dialog), use it
        if selected_path and os.path.exists(selected_path):
            # Look for MOT files in the selected directory
            mot_files = [f for f in os.listdir(selected_path) if f.endswith('.mot')]
            
            if mot_files:
                # Use the first MOT file found
                file_path = os.path.join(selected_path, mot_files[0])
                print(f"Found reference MOT file: {file_path}")
                return file_path
                
            # If no MOT files in the main directory, check for kinematics subdirectory
            kinematics_dir = os.path.join(selected_path, "kinematics")
            if os.path.exists(kinematics_dir):
                mot_files = [f for f in os.listdir(kinematics_dir) if f.endswith('.mot')]
                if mot_files:
                    file_path = os.path.join(kinematics_dir, mot_files[0])
                    print(f"Found reference MOT file in kinematics directory: {file_path}")
                    return file_path
        
        # Fall back to original behavior if no path provided or nothing found
        elif self._session_path:
            # Look for a reference directory in the session folder
            reference_dir = os.path.join(self._session_path, "reference")
            
            if os.path.exists(reference_dir):
                # Look for MOT files in the reference directory
                mot_files = [f for f in os.listdir(reference_dir) if f.endswith('.mot')]
                
                if mot_files:
                    # Use the first reference MOT file found
                    file_path = os.path.join(reference_dir, mot_files[0])
                    print(f"Found reference MOT file: {file_path}")
                    return file_path
                    
                # If no MOT files in the main reference directory, check for kinematics subdirectory
                kinematics_dir = os.path.join(reference_dir, "kinematics")
                if os.path.exists(kinematics_dir):
                    mot_files = [f for f in os.listdir(kinematics_dir) if f.endswith('.mot')]
                    if mot_files:
                        file_path = os.path.join(kinematics_dir, mot_files[0])
                        print(f"Found reference MOT file in kinematics directory: {file_path}")
                        return file_path
        else:
            print("Warning: No path provided and no session path set")
        
        return None
    except Exception as e:
        print(f"Error finding reference MOT file: {str(e)}")
        return None