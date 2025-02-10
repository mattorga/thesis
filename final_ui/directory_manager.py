import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDialog
from patient_form import Ui_patient_form

class DirectoryManager:
  def __init__(self, main_window):
    self.main_window = main_window
    self.session_directory = None
    self.participant_directory = None
    self.trial_directory = None
    self.base_directory = os.path.join(os.path.expanduser("~"), "Documents", "GaitScape")

  def set_session(self):
    # Start in Documents/GaitScape folder
    gaitscape_path = os.path.join(os.path.expanduser("~"), "Documents", "GaitScape")
      
    # Create GaitScape folder if it doesn't exist
    if not os.path.exists(gaitscape_path):
        os.makedirs(gaitscape_path)
    
    # Configure file dialog
    dialog = QFileDialog(self.main_window)
    dialog.setFileMode(QFileDialog.Directory)
    dialog.setOption(QFileDialog.ShowDirsOnly, True)
    dialog.setDirectory(gaitscape_path)
    
    if dialog.exec_():
        selected_path = dialog.selectedFiles()[0]
        # Verify selected folder is directly under GaitScape
        if os.path.dirname(selected_path) == gaitscape_path:
            self.session_directory = selected_path
            session_name = os.path.basename(selected_path)
            
            # Reset participant and trial selections
            self.participant_directory = None
            self.trial_directory = None

        else:
            QMessageBox.warning(self.main_window, "Invalid Selection", 
                              "Please select a session folder directly under GaitScape folder.")

  def get_session(self):
     return self.session_directory
  
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
            QMessageBox.warning(self.main_window, "Invalid Selection", 
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