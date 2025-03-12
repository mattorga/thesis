from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog
from comparativeParams import Ui_Dialog as ComparativeParamsUI
from utils.statistics.Angles_Analysis import analyze_gait_patterns
from utils.statistics.paired_t_test_gait import analyze_gait_parameters
import os
import types
from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog

class ComparativeStatsDialog(QDialog):
    """Dialog for displaying comparative statistics"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = ComparativeParamsUI()
        self.ui.setupUi(self)
        
        # Set up the dialog appearance
        self.setWindowTitle("Comparative Statistics")
        self.setModal(False)  # Allow interaction with main window while dialog is open
        
        # Store selected files for paired t-test
        self.base2_file = None
        self.verse2_file = None
        # Add properties for the main comparison paths
        self.base_csv_path = None
        self.verse_csv_path = None
        
        # Cache for analysis results to avoid redundant calculations
        self.cached_t_test_stats = None
        self.cached_input_files = {
            'base_files': None,
            'verse_files': None
        }
        
        # Connect button signals
        self.ui.base2Button.clicked.connect(self.on_base2_button_clicked)
        self.ui.verse2Button.clicked.connect(self.on_verse2_button_clicked)

    def on_base2_button_clicked(self):
        """Handle clicks on the Base 2 button"""
        try:
            # Get the main window reference
            main_window = self.parent()
            if not main_window:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Could not access main window reference."
                )
                return
                
            # Get participant path
            participant_path = main_window.directory_manager.participant_path
            if not participant_path:
                QMessageBox.warning(
                    self,
                    "Missing Data",
                    "Please select a participant first."
                )
                return
                
            # Create file dialog to select trial directory
            dialog = QFileDialog(self)
            dialog.setFileMode(QFileDialog.Directory)
            dialog.setOption(QFileDialog.ShowDirsOnly, True)
            dialog.setDirectory(participant_path)
            
            if dialog.exec_():
                selected_path = dialog.selectedFiles()[0]
                
                # Ensure it's a trial directory within the participant directory
                if os.path.dirname(selected_path) != participant_path:
                    QMessageBox.warning(
                        self,
                        "Invalid Selection",
                        "Please select a trial directory directly under the participant folder."
                    )
                    return
                    
                # Check if it's a valid trial directory (starts with T followed by numbers)
                trial_dir = os.path.basename(selected_path)
                if not (trial_dir.startswith('T') and trial_dir.split('_')[0][1:].isdigit()):
                    QMessageBox.warning(
                        self,
                        "Invalid Selection",
                        "Please select a valid trial folder (starts with 'T')."
                    )
                    return
                
                # Validate that it's not the same as the current base trial
                if main_window.directory_manager.trial_path == selected_path:
                    QMessageBox.warning(
                        self,
                        "Invalid Selection",
                        "Cannot select the current base trial for Base 2."
                    )
                    return
                    
                # Validate that it's not the same as the verse2 trial
                if self.verse2_file:
                    verse2_trial_path = os.path.dirname(os.path.dirname(self.verse2_file))
                    if verse2_trial_path == selected_path:
                        QMessageBox.warning(
                            self,
                            "Invalid Selection",
                            "Base 2 and Verse 2 cannot be the same trial."
                        )
                        return
                
                # Find CSV file in the statistics directory
                statistics_dir = os.path.join(selected_path, "statistics")
                if not os.path.exists(statistics_dir):
                    QMessageBox.warning(
                        self,
                        "Missing Data",
                        f"No statistics directory found in {trial_dir}."
                    )
                    return
                
                # Look for the gait_parameters.csv file
                csv_file_path = os.path.join(statistics_dir, "gait_parameters.csv")
                if not os.path.exists(csv_file_path):
                    QMessageBox.warning(
                        self,
                        "Missing Data",
                        f"No gait_parameters.csv file found in {statistics_dir}."
                    )
                    return
                
                # Store the selected file path
                self.base2_file = csv_file_path
                
                # Set the button as checked and update button text
                self.ui.base2Button.setChecked(True)
                self.ui.base2Button.setText(trial_dir)
                                
                # Store the selection in the manager for persistence
                main_window = self.parent()
                if main_window and hasattr(main_window, 'stats_manager'):
                    main_window.stats_manager.base2_file = csv_file_path
                    main_window.stats_manager.base2_trial_name = trial_dir
                
                # Run paired t-test if both files are selected
                self.run_paired_t_test()
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error selecting Base 2 trial: {str(e)}"
            )
        
    def on_verse2_button_clicked(self):
        """Handle clicks on the Verse 2 button"""
        try:
            # Get the main window reference
            main_window = self.parent()
            if not main_window:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Could not access main window reference."
                )
                return
                
            # Get participant path
            participant_path = main_window.directory_manager.participant_path
            if not participant_path:
                QMessageBox.warning(
                    self,
                    "Missing Data",
                    "Please select a participant first."
                )
                return
                
            # Create file dialog to select trial directory
            dialog = QFileDialog(self)
            dialog.setFileMode(QFileDialog.Directory)
            dialog.setOption(QFileDialog.ShowDirsOnly, True)
            dialog.setDirectory(participant_path)
            
            if dialog.exec_():
                selected_path = dialog.selectedFiles()[0]
                
                # Ensure it's a trial directory within the participant directory
                if os.path.dirname(selected_path) != participant_path:
                    QMessageBox.warning(
                        self,
                        "Invalid Selection",
                        "Please select a trial directory directly under the participant folder."
                    )
                    return
                    
                # Check if it's a valid trial directory (starts with T followed by numbers)
                trial_dir = os.path.basename(selected_path)
                if not (trial_dir.startswith('T') and trial_dir.split('_')[0][1:].isdigit()):
                    QMessageBox.warning(
                        self,
                        "Invalid Selection",
                        "Please select a valid trial folder (starts with 'T')."
                    )
                    return
                
                # Validate that it's not the same as current versus trial
                if hasattr(main_window, 'versus_data_file') and main_window.versus_data_file:
                    versus_dir = os.path.dirname(main_window.versus_data_file)
                    # If the versus_data_file is in a subdirectory, go up one level
                    if "gait-classification" in versus_dir:
                        versus_trial_path = os.path.dirname(versus_dir)
                    else:
                        versus_trial_path = os.path.dirname(os.path.dirname(versus_dir))
                    
                    if versus_trial_path == selected_path:
                        QMessageBox.warning(
                            self,
                            "Invalid Selection",
                            "Cannot select the current versus trial for Verse 2."
                        )
                        return
                
                # Validate that it's not the same as the base trial
                if main_window.directory_manager.trial_path == selected_path:
                    QMessageBox.warning(
                        self,
                        "Invalid Selection",
                        "Cannot select the current base trial for Verse 2."
                    )
                    return
                
                # Validate that it's not the same as base2 trial
                if self.base2_file:
                    base2_trial_path = os.path.dirname(os.path.dirname(self.base2_file))
                    if base2_trial_path == selected_path:
                        QMessageBox.warning(
                            self,
                            "Invalid Selection",
                            "Base 2 and Verse 2 cannot be the same trial."
                        )
                        return
                
                # Find CSV file in the statistics directory
                statistics_dir = os.path.join(selected_path, "statistics")
                if not os.path.exists(statistics_dir):
                    QMessageBox.warning(
                        self,
                        "Missing Data",
                        f"No statistics directory found in {trial_dir}."
                    )
                    return
                
                # Look for the gait_parameters.csv file
                csv_file_path = os.path.join(statistics_dir, "gait_parameters.csv")
                if not os.path.exists(csv_file_path):
                    QMessageBox.warning(
                        self,
                        "Missing Data",
                        f"No gait_parameters.csv file found in {statistics_dir}."
                    )
                    return
                
                # Store the selected file path
                self.verse2_file = csv_file_path
                
                # Set the button as checked and update button text
                self.ui.verse2Button.setChecked(True)
                self.ui.verse2Button.setText(trial_dir)
                                
                # Store the selection in the manager for persistence
                main_window = self.parent()
                if main_window and hasattr(main_window, 'stats_manager'):
                    main_window.stats_manager.verse2_file = csv_file_path
                    main_window.stats_manager.verse2_trial_name = trial_dir
                
                # Run paired t-test if both files are selected
                self.run_paired_t_test()
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error selecting Verse 2 trial: {str(e)}"
            )
    
    def run_paired_t_test(self):
        """Run the paired t-test if both Base 2 and Verse 2 files are selected"""
        if self.base2_file and self.verse2_file:
            try:
                # First check if both files exist
                if not os.path.exists(self.base2_file):
                    QMessageBox.warning(
                        self,
                        "Missing File",
                        f"Base 2 file not found: {self.base2_file}"
                    )
                    return
                    
                if not os.path.exists(self.verse2_file):
                    QMessageBox.warning(
                        self,
                        "Missing File",
                        f"Verse 2 file not found: {self.verse2_file}"
                    )
                    return
                
                # Make sure base_csv_path and verse_csv_path are set
                main_window = self.parent()
                if main_window:
                    # Get the base and verse paths from the main window if they're not set
                    if not self.base_csv_path and hasattr(main_window, 'directory_manager'):
                        base_trial_path = main_window.directory_manager.trial_path
                        if base_trial_path:
                            self.base_csv_path = os.path.join(base_trial_path, "statistics", "gait_parameters.csv")
                    
                    if not self.verse_csv_path and hasattr(main_window, 'versus_data_file'):
                        versus_dir = os.path.dirname(main_window.versus_data_file)
                        # If the versus_data_file is in a subdirectory, go up one level
                        if "gait-classification" in versus_dir:
                            versus_trial_path = os.path.dirname(versus_dir)
                        else:
                            versus_trial_path = os.path.dirname(os.path.dirname(versus_dir))
                        
                        if versus_trial_path:
                            self.verse_csv_path = os.path.join(versus_trial_path, "statistics", "gait_parameters.csv")
                
                # Check if we have all required paths
                if not self.base_csv_path or not self.verse_csv_path:
                    QMessageBox.warning(
                        self,
                        "Missing Files",
                        "Cannot find required CSV files for analysis. Please ensure both trials have been processed."
                    )
                    return
                    
                # Check if files exist
                if not os.path.exists(self.base_csv_path) or not os.path.exists(self.verse_csv_path):
                    QMessageBox.warning(
                        self,
                        "Missing Files",
                        "One or more CSV files not found. Please ensure both trials have been processed."
                    )
                    return
                
                # Create input file arrays for checking against cache
                base_files = [self.base_csv_path, self.base2_file]
                verse_files = [self.verse_csv_path, self.verse2_file]
                
                # Check if we can use cached results
                if (self.cached_t_test_stats and 
                    self.cached_input_files['base_files'] == base_files and 
                    self.cached_input_files['verse_files'] == verse_files):
                    print("Using cached t-test results in dialog")
                    t_test_stats = self.cached_t_test_stats
                else:
                    print("Calculating new t-test results in dialog")
                    # Run the paired t-test analysis with the new files
                    t_test_stats = analyze_gait_parameters(base_files, verse_files)
                    
                    # Cache the results and inputs for future use
                    self.cached_t_test_stats = t_test_stats
                    self.cached_input_files = {
                        'base_files': base_files.copy(),  # Make copies to avoid reference issues
                        'verse_files': verse_files.copy()
                    }
                
                # Update UI with t-test results
                if t_test_stats:
                    if 'ave_p_value' in t_test_stats:
                        self.ui.avePValValue.setText(f"{t_test_stats['ave_p_value']:.4f}")
                        
                    if 'sig_params' in t_test_stats and 'total_params' in t_test_stats:
                        self.ui.totalDiffParamsValue.setText(f"{t_test_stats['sig_params']}/{t_test_stats['total_params']}")
                        
                    if 'sig_percent' in t_test_stats:
                        self.ui.percDiffValue.setText(f"{t_test_stats['sig_percent']:.1f}%")
                        
                else:
                    QMessageBox.warning(
                        self,
                        "Analysis Warning",
                        "The paired t-test completed, but no statistics were returned."
                    )
                
                # Also update the cache in the manager for persistence
                main_window = self.parent()
                if main_window and hasattr(main_window, 'stats_manager'):
                    main_window.stats_manager.cached_analysis_results = t_test_stats
                    main_window.stats_manager.cached_analysis_inputs = {
                        'base_files': base_files.copy(),
                        'verse_files': verse_files.copy()
                    }
                
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Analysis Error",
                    f"Error running paired t-test: {str(e)}"
                )
                import traceback
                traceback.print_exc()  # Print detailed error information to console
                
    def update_statistics(self, statistics):
        """
        Update the UI with the provided statistics
        
        Args:
            statistics (dict): Dictionary containing comparative statistics
        """
        if not statistics:
            return
        
        # Update statistics values in UI
        if 'ave_dtw' in statistics:
            self.ui.aveDTWValue.setText(f"{statistics['ave_dtw']:.2f}")
            
        if 'ave_corr' in statistics:
            self.ui.aveCorrValue.setText(f"{statistics['ave_corr']:.2f}")
            
        if 'ave_pearson_corr' in statistics:
            self.ui.avePearCorrValue.setText(f"{statistics['ave_pearson_corr']:.2f}")
            
        if 'ave_p_values' in statistics:
            self.ui.avePValuesValue.setText(f"{statistics['ave_p_values']:.4f}")
            
        # Add support for t-test statistics
        if 'ave_p_value' in statistics:
            self.ui.avePValValue.setText(f"{statistics['ave_p_value']:.4f}")
            
        if 'sig_params' in statistics and 'total_params' in statistics:
            self.ui.totalDiffParamsValue.setText(f"{statistics['sig_params']}/{statistics['total_params']}")
            
        if 'sig_percent' in statistics:
            self.ui.percDiffValue.setText(f"{statistics['sig_percent']:.1f}%")

class ComparativeStatsManager:
    """Manages the comparative statistics calculations and dialog"""
    
    def __init__(self, main_window):
        """
        Initialize the comparative statistics manager
        
        Args:
            main_window: The main application window
        """
        self.main_window = main_window
        self.stats_dialog = None
        
        # Store the selected trials for persistence between dialog instances
        self.base2_file = None
        self.verse2_file = None
        self.base2_trial_name = None
        self.verse2_trial_name = None
        
        # Cache for analysis results to avoid redundant calculations
        self.cached_analysis_results = None
        self.cached_analysis_inputs = None
        
    def setup_connections(self):
        """Setup signal connections"""
        if hasattr(self.main_window.ui, 'comparativeStatsButton'):
            # Connect to the clicked signal
            self.main_window.ui.comparativeStatsButton.clicked.connect(self.on_stats_button_clicked)
    
    def on_stats_button_clicked(self):
        """Handler for when the comparative stats button is clicked.
        Uses MOT files stored from verse trial selection for analysis."""
        try:
            # Get the button's checked state
            is_checked = self.main_window.ui.comparativeStatsButton.isChecked()
            
            if is_checked:
                # Button is checked, show dialog
                
                # Check if we have both base and verse trial data
                if not hasattr(self.main_window, 'base_motion_data') or not hasattr(self.main_window, 'versus_motion_data'):
                    QMessageBox.warning(
                        self.main_window,
                        "Missing Data",
                        "Cannot calculate statistics. Either base or versus trial data is missing."
                    )
                    # Reset button state
                    self.main_window.ui.comparativeStatsButton.setChecked(False)
                    return
                    
                # Further check if data is not None
                if self.main_window.base_motion_data is None or self.main_window.versus_motion_data is None:
                    QMessageBox.warning(
                        self.main_window,
                        "Missing Data",
                        "Cannot calculate statistics. Either base or versus trial data is None."
                    )
                    # Reset button state
                    self.main_window.ui.comparativeStatsButton.setChecked(False)
                    return
            
                # Get the paths to the MOT files - use the stored paths from when trials were selected
                base_mot_file = None
                versus_mot_file = None
                
                # Get base MOT file
                if hasattr(self.main_window, 'directory_manager'):
                    base_mot_file = self.main_window.directory_manager.find_motion_mot_file()
                
                # Get verse MOT file - use the one stored during verse trial selection
                if hasattr(self.main_window, 'versus_mot_file'):
                    versus_mot_file = self.main_window.versus_mot_file
                
                if base_mot_file is None or versus_mot_file is None:
                    QMessageBox.warning(
                        self.main_window,
                        "Missing Files",
                        "Cannot find required MOT files for analysis. Please ensure both trials have been processed."
                    )
                    # Reset button state
                    self.main_window.ui.comparativeStatsButton.setChecked(False)
                    return
                
                # Get the paths to the CSV files for paired t-test analysis
                base_csv_path = None
                versus_csv_path = None
                
                # Get the base trial path
                base_trial_path = self.main_window.directory_manager.trial_path
                
                # Get the versus trial path from the versus_data_file path
                versus_trial_path = None
                if hasattr(self.main_window, 'versus_data_file') and self.main_window.versus_data_file:
                    versus_dir = os.path.dirname(self.main_window.versus_data_file)
                    # If the versus_data_file is in a subdirectory, go up one level
                    if "gait-classification" in versus_dir:
                        versus_trial_path = os.path.dirname(versus_dir)
                    else:
                        versus_trial_path = os.path.dirname(os.path.dirname(versus_dir))
                
                # Construct paths to the CSV files in statistics directory
                if base_trial_path:
                    base_csv_path = os.path.join(base_trial_path, "statistics", "gait_parameters.csv")
                
                if versus_trial_path:
                    versus_csv_path = os.path.join(versus_trial_path, "statistics", "gait_parameters.csv")
                    
                # Call Angles_Analysis.analyze_gait_patterns with the MOT files
                angle_stats = analyze_gait_patterns(base_mot_file, versus_mot_file)
                
                # Also get t-test statistics if CSV files are available
                t_test_stats = None
                if self.base2_file and self.verse2_file and os.path.exists(self.base2_file) and os.path.exists(self.verse2_file):
                    if base_csv_path and versus_csv_path and os.path.exists(base_csv_path) and os.path.exists(versus_csv_path):
                        t_test_stats = analyze_gait_parameters([base_csv_path, self.base2_file], 
                                                                    [versus_csv_path, self.verse2_file])
                
                # Combine the statistics
                combined_stats = {}
                if angle_stats:
                    combined_stats.update(angle_stats)
                if t_test_stats:
                    combined_stats.update(t_test_stats)
                
                # If no stats were generated, show an error
                if not combined_stats:
                    QMessageBox.warning(
                        self.main_window,
                        "Analysis Failed",
                        "Failed to generate comparative statistics. Check console for details."
                    )
                    # Reset button state
                    self.main_window.ui.comparativeStatsButton.setChecked(False)
                    return
                
                # Create and show the dialog
                if not self.stats_dialog:
                    self.stats_dialog = ComparativeStatsDialog(self.main_window)
                    
                    # Define a custom closeEvent function
                    def custom_close_event(dialog_self, event):
                        """Override close event to update the button state when user closes with X button"""
                        main_window = dialog_self.parent()
                        if main_window and hasattr(main_window.ui, 'comparativeStatsButton'):
                            # Uncheck the button when dialog is closed
                            main_window.ui.comparativeStatsButton.setChecked(False)
                        
                        # Don't actually close, just hide the dialog
                        dialog_self.hide()
                        event.ignore()
                    
                    # Bind the custom closeEvent to the dialog
                    import types
                    self.stats_dialog.closeEvent = types.MethodType(custom_close_event, self.stats_dialog)
                    
                    # Set the base and verse CSV paths
                    self.stats_dialog.base_csv_path = base_csv_path
                    self.stats_dialog.verse_csv_path = versus_csv_path
                    
                    # Restore previously selected trials if they exist
                    if self.base2_file and os.path.exists(self.base2_file):
                        self.stats_dialog.base2_file = self.base2_file
                        if self.base2_trial_name:
                            self.stats_dialog.ui.base2Button.setText(f"Base 2: {self.base2_trial_name}")
                            self.stats_dialog.ui.base2Button.setChecked(True)
                    
                    if self.verse2_file and os.path.exists(self.verse2_file):
                        self.stats_dialog.verse2_file = self.verse2_file
                        if self.verse2_trial_name:
                            self.stats_dialog.ui.verse2Button.setText(f"Verse 2: {self.verse2_trial_name}")
                            self.stats_dialog.ui.verse2Button.setChecked(True)
                            
                    # If both files are set, run the paired t-test
                    if self.stats_dialog.base2_file and self.stats_dialog.verse2_file:
                        self.stats_dialog.run_paired_t_test()
                        print(f"Base 2: {self.stats_dialog.base2_file}")
                        print(f"Verse 2: {self.stats_dialog.verse2_file}")
                else:
                    # Update the base and verse CSV paths in case they've changed
                    self.stats_dialog.base_csv_path = base_csv_path
                    self.stats_dialog.verse_csv_path = versus_csv_path
                
                # Update dialog with calculated statistics
                self.stats_dialog.update_statistics(combined_stats)
                
                # Show the dialog
                self.stats_dialog.show()
                self.stats_dialog.raise_()  # Bring to front
            else:
                # Button is unchecked, hide dialog if it exists
                if self.stats_dialog and self.stats_dialog.isVisible():
                    self.stats_dialog.hide()
                
        except Exception as e:
            QMessageBox.critical(
                self.main_window,
                "Error",
                f"Error calculating comparative statistics: {str(e)}"
            )
            # Reset button state on error
            self.main_window.ui.comparativeStatsButton.setChecked(False)
            import traceback
            traceback.print_exc()
            
    
    def check_selected_trials_validity(self):
        """
        Check if previously selected Base2 and Verse2 trials are still valid
        after a session/participant/trial change
        """
        current_participant_path = None
        if hasattr(self.main_window, 'directory_manager'):
            current_participant_path = self.main_window.directory_manager.participant_path
        
        if not current_participant_path:
            # No participant selected, reset everything
            self.reset_selected_trials()
            return
            
        # Check Base2 file
        if self.base2_file and os.path.exists(self.base2_file):
            base2_trial_path = os.path.dirname(os.path.dirname(self.base2_file))
            base2_participant_path = os.path.dirname(base2_trial_path)
            
            # If the Base2 trial is no longer in the current participant folder, reset it
            if base2_participant_path != current_participant_path:
                self.base2_file = None
                self.base2_trial_name = None
        else:
            # File doesn't exist anymore
            self.base2_file = None
            self.base2_trial_name = None
            
        # Check Verse2 file
        if self.verse2_file and os.path.exists(self.verse2_file):
            verse2_trial_path = os.path.dirname(os.path.dirname(self.verse2_file))
            verse2_participant_path = os.path.dirname(verse2_trial_path)
            
            # If the Verse2 trial is no longer in the current participant folder, reset it
            if verse2_participant_path != current_participant_path:
                self.verse2_file = None
                self.verse2_trial_name = None
        else:
            # File doesn't exist anymore
            self.verse2_file = None
            self.verse2_trial_name = None
            
        # Update dialog if it exists
        if self.stats_dialog is not None:
            if self.base2_file:
                self.stats_dialog.base2_file = self.base2_file
                if self.base2_trial_name:
                    self.stats_dialog.ui.base2Button.setText(f"Base 2: {self.base2_trial_name}")
                    self.stats_dialog.ui.base2Button.setChecked(True)
            else:
                self.stats_dialog.base2_file = None
                self.stats_dialog.ui.base2Button.setText("Base 2")
                self.stats_dialog.ui.base2Button.setChecked(False)
                
            if self.verse2_file:
                self.stats_dialog.verse2_file = self.verse2_file
                if self.verse2_trial_name:
                    self.stats_dialog.ui.verse2Button.setText(f"Verse 2: {self.verse2_trial_name}")
                    self.stats_dialog.ui.verse2Button.setChecked(True)
            else:
                self.stats_dialog.verse2_file = None
                self.stats_dialog.ui.verse2Button.setText("Verse 2")
                self.stats_dialog.ui.verse2Button.setChecked(False)
            
            # Check if we need to run the paired t-test
            if self.base2_file and self.verse2_file:
                self.stats_dialog.run_paired_t_test()
            else:
                # Reset t-test results if we don't have both files
                self.stats_dialog.ui.avePValValue.setText("-")
                self.stats_dialog.ui.totalDiffParamsValue.setText("-")
                self.stats_dialog.ui.percDiffValue.setText("-")
    
    def reset_selected_trials(self):
        """Reset the selected Base2 and Verse2 trials"""
        self.base2_file = None
        self.verse2_file = None
        self.base2_trial_name = None
        self.verse2_trial_name = None
        
        # If the dialog exists, reset its values too
        if self.stats_dialog is not None:
            self.stats_dialog.base2_file = None
            self.stats_dialog.verse2_file = None
            self.stats_dialog.ui.base2Button.setText("Base 2")
            self.stats_dialog.ui.verse2Button.setText("Verse 2")
            self.stats_dialog.ui.base2Button.setChecked(False)
            self.stats_dialog.ui.verse2Button.setChecked(False)
            
            # Also reset the t-test results
            self.stats_dialog.ui.avePValValue.setText("-")
            self.stats_dialog.ui.totalDiffParamsValue.setText("-")
            self.stats_dialog.ui.percDiffValue.setText("-")
            
    def update_dialog_if_open(self):
        """Update the dialog if it's already open with new data"""
        if self.stats_dialog is not None and self.stats_dialog.isVisible():
            # Recalculate statistics
            self.on_stats_button_clicked()
    
    def cleanup(self):
        """Clean up resources"""
        if self.stats_dialog is not None:
            self.stats_dialog.close()
            self.stats_dialog = None