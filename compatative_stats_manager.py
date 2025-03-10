from PyQt5.QtWidgets import QDialog, QMessageBox
from comparativeStats import Ui_Dialog as ComparativeStatsUI
from utils.statistics.Angles_Analysis import analyze_gait_patterns  # Import the analyze_gait_patterns function

class ComparativeStatsDialog(QDialog):
    """Dialog for displaying comparative statistics"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = ComparativeStatsUI()
        self.ui.setupUi(self)
        
        # Set up the dialog appearance
        self.setWindowTitle("Comparative Statistics")
        self.setModal(False)  # Allow interaction with main window while dialog is open
        self.resize(400, 175)  # Adjust size if needed

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
        
    def setup_connections(self):
        """Setup signal connections"""
        if hasattr(self.main_window.ui, 'comparativeStatsButton'):
            # Connect to the clicked signal
            self.main_window.ui.comparativeStatsButton.clicked.connect(self.on_stats_button_clicked)
    
    def on_stats_button_clicked(self):
      """Handler for when the comparative stats button is clicked.
      Uses MOT files stored from verse trial selection for analysis."""
      try:
          # Check if we have both base and verse trial data
          if not hasattr(self.main_window, 'base_motion_data') or not hasattr(self.main_window, 'versus_motion_data'):
              QMessageBox.warning(
                  self.main_window,
                  "Missing Data",
                  "Cannot calculate statistics. Either base or versus trial data is missing."
              )
              return
              
          # Further check if data is not None
          if self.main_window.base_motion_data is None or self.main_window.versus_motion_data is None:
              QMessageBox.warning(
                  self.main_window,
                  "Missing Data",
                  "Cannot calculate statistics. Either base or versus trial data is None."
              )
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
              return
                  
          # Call Angles_Analysis.analyze_gait_patterns with the MOT files
          stats = analyze_gait_patterns(base_mot_file, versus_mot_file)
          
          # Create and show the dialog
          if not self.stats_dialog:
              self.stats_dialog = ComparativeStatsDialog(self.main_window)
          
          # Update dialog with calculated statistics
          self.stats_dialog.update_statistics(stats)
          
          # Show the dialog
          self.stats_dialog.show()
          self.stats_dialog.raise_()  # Bring to front
          
      except Exception as e:
          QMessageBox.critical(
              self.main_window,
              "Error",
              f"Error calculating comparative statistics: {str(e)}"
          )
          import traceback
          traceback.print_exc()
    

    
    def cleanup(self):
        """Clean up resources"""
        if self.stats_dialog is not None:
            self.stats_dialog.close()
            self.stats_dialog = None