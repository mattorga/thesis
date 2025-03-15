import os
import pandas as pd
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtCore import Qt, QRect,  QTimer

from analyticsParams import Ui_Dialog as AnalyticsParamsUI

class AnalyticsParamsDialog(QDialog):
    """Dialog for displaying detailed gait analysis parameters"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = AnalyticsParamsUI()
        self.ui.setupUi(self)
        
        # Set up the dialog appearance
        self.setWindowTitle("Gait Parameters")
        self.setModal(False)  # Allow interaction with main window while dialog is open
        
        # Override the close event to just hide the dialog and update the button state
        self.parent = parent
    
    def closeEvent(self, event):
        """
        Override close event to update the button state instead of actually closing
        """
        # Find and uncheck the paramsButton when the dialog is closed via the X button
        if self.parent and hasattr(self.parent, 'ui') and hasattr(self.parent.ui, 'paramsButton'):
            self.parent.ui.paramsButton.setChecked(False)
        
        # Hide instead of close
        self.hide()
        event.ignore()
    
    def update_parameters(self, parameters):
        """
        Update the UI with the provided parameters
        
        Args:
            parameters (dict): Dictionary containing gait parameters
        """
        if not parameters:
            return
          
        # Update spatio-temporal parameters
        if 'stride_length_cm' in parameters:
            self.ui.strideLengthValue.setText(f"{parameters['stride_length_cm']:.2f}")
        
        if 'stride_time_s' in parameters:
            self.ui.strideTimeValue.setText(f"{parameters['stride_time_s']:.2f}")
            
        if 'gait_speed_m/s' in parameters:
            self.ui.gaitSpeedValue.setText(f"{parameters['gait_speed_m/s']:.2f}")
            
        if 'stride_width_cm' in parameters:
            self.ui.strideWidthValue.setText(f"{parameters['stride_width_cm']:.2f}")
    
    def update_metrics(self, metrics):
        """
        Update the UI with the gait classification metrics
        
        Args:
            metrics (dict): Dictionary containing gait metrics from metrics_summary.csv
        """
        if not metrics:
            return
        
        # Mapping from phase names in CSV to UI element prefixes
        phase_to_ui_map = {
            'Initial-LSw': 'initLSw',
            'Mid-LSw': 'midLSw',
            'Term-LSw': 'termLSw',
            'DSt1': 'DSt1',
            'Initial-RSw': 'initRSw',
            'Mid-RSw': 'midRSw',
            'Term-RSw': 'termRSw',
            'DSt2': 'DSt2'
        }
        
        # Update each phase's metrics in the UI
        for phase, prefix in phase_to_ui_map.items():
            if phase in metrics:
                phase_data = metrics[phase]
                
                # Get the UI elements for this phase
                gs_label = getattr(self.ui, f'GS_{prefix}', None)
                actual_label = getattr(self.ui, f'actual_{prefix}', None)
                abs_err_label = getattr(self.ui, f'absErr_{prefix}', None)
                rel_err_label = getattr(self.ui, f'relErr_{prefix}', None)
                
                # Update UI elements if they exist
                if gs_label and 'Gold Standard' in phase_data:
                    gs_label.setText(f"{phase_data['Gold Standard']:.2f}%")
                
                if actual_label and 'Avg Actual Percentage' in phase_data:
                    actual_label.setText(f"{phase_data['Avg Actual Percentage']:.2f}%")
                
                if abs_err_label and 'Avg Absolute Error' in phase_data:
                    abs_err_label.setText(f"{phase_data['Avg Absolute Error']:.2f}%")
                
                if rel_err_label and 'Avg Relative Error' in phase_data:
                    rel_err_label.setText(f"{phase_data['Avg Relative Error']:.2f}%")


class ParamsManager:
    """Manages the gait parameters and dialog"""
    
    def __init__(self, main_window):
        """
        Initialize the parameters manager
        
        Args:
            main_window: The main application window
        """
        self.main_window = main_window
        self.dialog = None
        self.current_parameters = {}
        self.current_metrics = {}
    
    def setup_connections(self):
        """Setup signal connections"""
        if hasattr(self.main_window.ui, 'paramsButton'):
            # Connect to the toggled signal
            self.main_window.ui.paramsButton.toggled.connect(self.on_params_button_toggled)
            
            # Since the paramsButton is checked by default, show the dialog initially
            # if the button is already checked
            if self.main_window.ui.paramsButton.isChecked():
                QApplication.processEvents()  # Ensure UI is fully initialized
                self.on_params_button_toggled(False)
    
    def create_dialog(self):
        """Create the parameters dialog if it doesn't exist"""
        if self.dialog is None:
            self.dialog = AnalyticsParamsDialog(self.main_window)
            
            # Position the dialog relative to the main window
            # Place it next to the main window on the right side
            main_geometry = self.main_window.geometry()
            dialog_width = 467  # Width from the UI file
            dialog_height = 448  # Height from the UI file
            
            # Position next to main window on right side
            dialog_x = main_geometry.x() + main_geometry.width() + 10
            dialog_y = main_geometry.y() + (main_geometry.height() - dialog_height) // 2
            
            self.dialog.setGeometry(QRect(dialog_x, dialog_y, dialog_width, dialog_height))

    def check_trial_selected(self):
        """
        Check if a trial is currently selected
        
        Returns:
            bool: True if a trial is selected, False otherwise
        """
        return (hasattr(self.main_window, 'directory_manager') and 
                self.main_window.directory_manager.trial_path is not None and 
                os.path.exists(self.main_window.directory_manager.trial_path))

    def on_params_button_toggled(self, checked):
        """Handle params button toggle"""
        if checked:
            # Check if a trial is selected before showing the dialog
            if not self.check_trial_selected():
                # No trial selected, uncheck the button and return
                QTimer.singleShot(0, lambda: self.main_window.ui.paramsButton.setChecked(False))
                return
                
            self.create_dialog()
            # Update the dialog with current trial data
            self.update_dialog_with_data(self.main_window.directory_manager.trial_path)
            self.dialog.show()
        elif self.dialog:
            self.dialog.hide()
    
    def update_dialog_with_data(self, trial_path):
        """
        Update the dialog with data from the specified trial path
        
        Args:
            trial_path (str): Path to the trial directory
        """
        # If trial_path is None or doesn't exist, close the dialog and uncheck the button
        if not trial_path or not os.path.exists(trial_path):
            self.close_dialog_and_uncheck_button()
            return
            
        self.load_parameters()
        self.load_metrics()
        
        if self.dialog:
            self.dialog.update_parameters(self.current_parameters)
            self.dialog.update_metrics(self.current_metrics)

    def close_dialog_and_uncheck_button(self):
        """
        Close the parameter dialog and uncheck the paramsButton
        """
        # Close dialog if it exists
        if self.dialog and self.dialog.isVisible():
            self.dialog.hide()
        
        # Uncheck the paramsButton on the analytics page
        if self.main_window and hasattr(self.main_window.ui, 'paramsButton'):
            self.main_window.ui.paramsButton.setChecked(False)
    
    def load_parameters(self):
        """
        Load gait parameters from the statistics directory created by Calc_ST_params.analyze_gait()
        """
        try:
            # Reset parameters
            self.current_parameters = {}
            
            # Check if a trial is selected
            if not self.check_trial_selected():
                return
            
            # Check if statistics directory and gait_parameters.csv exist
            stats_dir = os.path.join(self.main_window.directory_manager.trial_path, "statistics")
            csv_path = os.path.join(stats_dir, "gait_parameters.csv")
            
            if os.path.exists(csv_path):
                # Read the CSV file into a DataFrame
                df = pd.read_csv(csv_path)
                
                # Convert DataFrame to dictionary
                for _, row in df.iterrows():
                    param_name = row['Parameter'].lower().replace(' ', '_').replace('(', '').replace(')', '')
                    self.current_parameters[param_name] = row['Value']
            else:
                print(f"No parameters file found at {csv_path}")
        except Exception as e:
            print(f"Error loading gait parameters: {str(e)}")
    
    def load_metrics(self):
        """
        Load gait classification metrics from metrics_summary.csv
        """
        try:
            # Reset metrics
            self.current_metrics = {}
            
            # Check if a trial is selected
            if not self.check_trial_selected():
                return
            
            # Check if gait-classification directory and metrics_summary.csv exist
            gait_class_dir = os.path.join(self.main_window.directory_manager.trial_path, "gait-classification")
            csv_path = os.path.join(gait_class_dir, "metrics_summary.csv")
            
            if os.path.exists(csv_path):
                # Read the CSV file into a DataFrame
                df = pd.read_csv(csv_path)
                
                # Convert DataFrame to dictionary with Phase as the key
                for _, row in df.iterrows():
                    phase_name = row['Phase']
                    self.current_metrics[phase_name] = row.to_dict()
                
                print(f"Loaded metrics from {csv_path}")
            else:
                print(f"No metrics file found at {csv_path}")
                # Set current_metrics to an empty dictionary, which will cause update_metrics to reset UI
                self.current_metrics = {}
                
                # If the dialog exists, reset all metrics-related fields to "-"
                if self.dialog:
                    self.reset_metrics_ui()
        except Exception as e:
            print(f"Error loading gait metrics: {str(e)}")
            # Same behavior as file not found - reset metrics
            self.current_metrics = {}
            if self.dialog:
                self.reset_metrics_ui()
    
    def reset_metrics_ui(self):
        """
        Reset all metrics-related UI elements to "-"
        """
        if not self.dialog:
            return
            
        # Mapping from phase names to UI element prefixes
        phase_to_ui_map = {
            'Initial-LSw': 'initLSw',
            'Mid-LSw': 'midLSw',
            'Term-LSw': 'termLSw',
            'DSt1': 'DSt1',
            'Initial-RSw': 'initRSw',
            'Mid-RSw': 'midRSw',
            'Term-RSw': 'termRSw',
            'DSt2': 'DSt2'
        }
        
        # Reset each phase's metrics in the UI
        for _, prefix in phase_to_ui_map.items():
            # Get the UI elements for this phase
            gs_label = getattr(self.dialog.ui, f'GS_{prefix}', None)
            actual_label = getattr(self.dialog.ui, f'actual_{prefix}', None)
            abs_err_label = getattr(self.dialog.ui, f'absErr_{prefix}', None)
            rel_err_label = getattr(self.dialog.ui, f'relErr_{prefix}', None)
            
            # Reset UI elements if they exist
            if gs_label:
                gs_label.setText("-")
            
            if actual_label:
                actual_label.setText("-")
            
            if abs_err_label:
                abs_err_label.setText("-")
            
            if rel_err_label:
                rel_err_label.setText("-")
    
    def refresh_dialog(self):
        """Refresh the dialog with current data"""
        # Check if a trial is selected
        if not self.check_trial_selected():
            # No trial selected, close dialog and uncheck button
            self.close_dialog_and_uncheck_button()
            return
            
        # Always try to refresh even if dialog isn't visible yet,
        # so data is ready when dialog is shown
        # Load fresh data from the new trial
        self.current_metrics = {}
        self.current_parameters = {}
        
        self.load_parameters()
        self.load_metrics()
        
        # Update the UI if dialog exists
        if self.dialog:
            self.dialog.update_parameters(self.current_parameters)
            self.dialog.update_metrics(self.current_metrics)
            
            # If the dialog is visible, make sure it displays the updated data
            if self.dialog.isVisible():
                self.dialog.repaint()
    
    def cleanup(self):
        """Clean up resources"""
        if self.dialog is not None:
            # Disconnect signals to avoid crashes
            if hasattr(self.main_window.ui, 'paramsButton'):
                try:
                    self.main_window.ui.paramsButton.toggled.disconnect(self.on_params_button_toggled)
                except:
                    pass  # Signal might not be connected
            
            # Directly close the dialog without triggering the closeEvent logic
            self.dialog.setAttribute(Qt.WA_DeleteOnClose, True)
            self.dialog.close()
            self.dialog = None