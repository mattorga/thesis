import os
import re

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

  @participant_path.setter
  def participant_path(self, value):
      if value is not None and not os.path.exists(value):
        raise ValueError("Participant path must exist")
      self._participant_path = value

      self.trial_path = None
  
  @trial_path.setter
  def trial_path(self, value):
    if value is not None and not os.path.exists(value):
      raise ValueError("Trial path must exist")
    self._trial_path = value
     
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
        if os.path.dirname(selected_path) == gaitscape_path:
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
      else:
         QMessageBox.warning(self.main_window, "Invalid Selection", 
                              f"Please select a trial folder directly under {os.path.basename(self._participant_path)} folder.")

  # --- Adder Methods --- #
  def add_participant(self):
      if not self._session_path:
        QMessageBox.warning(self.main_window, "Error", 
                          "Please select a session first.")
        return
          
      dialog = PatientForm(self.main_window)
      
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
                            
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", 
                              f"Failed to create participant: {str(e)}")
            if os.path.exists(participant_path):
                try:
                    os.rmdir(participant_path)
                except:
                    pass                  
  def add_trial(self):
      dialog = TrialForm(self.main_window)
      

      if dialog.exec_() == QDialog.Accepted:
        trial_name = dialog.ui.trialNameField.text()

        trial_dir = f"T00_{trial_name}"
        trial_path = os.path.join(self._participant_path, trial_dir)
        
        os.makedirs(trial_path)