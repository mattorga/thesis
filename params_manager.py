import os
import pandas as pd
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtCore import Qt, QRect

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
        
        # The remaining parameters are placeholders - the ST_params file might not have these
        # but we include them for completeness
        params_mapping = {
            'single_stance': self.ui.label_19,
            'single_stance_error': self.ui.label_25,
            'double_stance': self.ui.label_20,
            'double_stance_error': self.ui.label_26,
            'left_stance': self.ui.label_21,
            'left_stance_error': self.ui.label_27,
            'right_stance': self.ui.label_22,
            'right_stance_error': self.ui.label_28,
            'left_swing': self.ui.label_23,
            'left_swing_error': self.ui.label_29,
            'right_swing': self.ui.label_24,
            'right_swing_error': self.ui.label_30
        }
        
        # Update any available parameters
        for param_name, label in params_mapping.items():
            if param_name in parameters:
                # Format as percentage if it's a stance or swing parameter
                if 'stance' in param_name or 'swing' in param_name:
                    label.setText(f"{parameters[param_name]:.1f}%")
                else:
                    label.setText(f"{parameters[param_name]:.2f}")


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
    
    def on_params_button_toggled(self, checked):
        """
        Handle the toggle state of the params button
        
        Args:
            checked (bool): Whether the button is checked
        """
        if checked:
            # Create the dialog if it doesn't exist
            if self.dialog is None:
                self.dialog = AnalyticsParamsDialog(self.main_window)
                
                # Position the dialog relative to the main window
                main_geometry = self.main_window.geometry()
                dialog_width = self.dialog.width()
                dialog_height = self.dialog.height()
                
                # Position at right side of main window
                self.dialog.setGeometry(
                    main_geometry.right() - dialog_width,
                    main_geometry.top() + 100,
                    dialog_width,
                    dialog_height
                )
            
            # Load and update with current parameters
            self.load_parameters()
            self.dialog.update_parameters(self.current_parameters)
            
            # Show the dialog
            self.dialog.show()
            self.dialog.raise_()  # Bring to front
            
        else:
            # Hide the dialog if it exists
            if self.dialog is not None:
                self.dialog.hide()
    
    def load_parameters(self):
        """
        Load gait parameters from the statistics directory created by Calc_ST_params.analyze_gait()
        """
        try:
            # Reset parameters
            self.current_parameters = {}
            
            # Check if a trial is selected
            if not hasattr(self.main_window, 'directory_manager') or not self.main_window.directory_manager.trial_path:
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
                # No parameters file found, use mock data for testing
                self._add_mock_data()
                
        except Exception as e:
            print(f"Error loading gait parameters: {str(e)}")
    
    def _add_mock_data(self):
        """Add mock data for testing purposes"""
        self.current_parameters = {
            'stride_length_cm': 120.5,
            'stride_time_s': 1.25,
            'gait_speed_ms': 1.1,
            'stride_width_cm': 15.3,
            'single_stance': 60.0,
            'single_stance_error': 5.2,
            'double_stance': 40.0,
            'double_stance_error': 4.8,
            'left_stance': 62.3,
            'left_stance_error': 4.1,
            'right_stance': 61.7,
            'right_stance_error': 4.3,
            'left_swing': 37.7,
            'left_swing_error': 4.1,
            'right_swing': 38.3,
            'right_swing_error': 4.3
        }
    
    def refresh_dialog(self):
        """Refresh dialog with updated parameters if it's visible"""
        if self.dialog is not None and self.dialog.isVisible():
            self.load_parameters()
            self.dialog.update_parameters(self.current_parameters)
    
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