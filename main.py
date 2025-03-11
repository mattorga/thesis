import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import glob
from Pose2Sim import Pose2Sim
from Pose2Sim.Utilities import bodykin_from_mot_osim
import toml
import configparser
import os
import pathlib
import subprocess
from final import Ui_MainWindow
from utils.gait_classification import gait_classification
from utils.statistics import Calc_ST_params
from params_manager import ParamsManager


from camera_manager import Camera, CameraManager
from directory_manager import DirectoryManager
from table_manager import TableManager
from data_manager import DataManager
from process_manager import ProcessManager
from chart_manager import ChartManager
from viewer_manager import ViewerManager
from comparative_params_manager import ComparativeStatsManager

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
    
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.stackedWidget.setCurrentIndex(1)
        self.current_highlighted_row = 0
        self.current_comparative_row = 0
        
        # Disable analytics and comparative buttons by default
        self.ui.analyticsButton.setEnabled(False)
        self.ui.jointAnalyticsButton.setEnabled(False)
        
        self.directory_manager = DirectoryManager(self)
        self.table_manager = TableManager(self)
        self.data_manager = DataManager()
        self.camera_manager = CameraManager(self)
        self.process_manager = ProcessManager(self)
        self.chart_manager = ChartManager(self)
        self.params_manager = ParamsManager(self)
        self.stats_manager = ComparativeStatsManager(self) 

        self.motion_data_file = None
        self.versus_data_file = None
        
        self.setup_player_controls()

        self.viewer_manager = None
        QTimer.singleShot(1000, self.init_viewer)

        camera_slots = {
        0: self.ui.cameraSlot1,
        1: self.ui.cameraSlot2,
        2: self.ui.cameraSlot3
        }
        self.camera_manager.camera_slots = camera_slots
        
        self.setup_analytics_buttons()
        self.setup_comparative_buttons()
        
        self.ui.slider.valueChanged.connect(self.on_slider_value_changed)
        self.ui.centerAnimationButton.setChecked(True)  # Default to centered
        self.ui.axisButton.setChecked(False)  # Default to axes hidden

        self.setup_connections()
        self.on_display_data()
 
  # --- Page Changing Functions --- #
  # Note: Simple enough to not need signal/slot implementation
    def on_dashboardButton_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    def on_camerasButton_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)
    def on_analyticsButton_clicked(self):
    # Only change page if the button is enabled (meaning data is available)
        if self.ui.analyticsButton.isEnabled():
            self.ui.stackedWidget.setCurrentIndex(2)
    def on_jointAnalyticsButton_clicked(self):
    # Only change page if the button is enabled (meaning data is available)
        if self.ui.jointAnalyticsButton.isEnabled():
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

        # Joint filter buttons for Analytics (Simulation) page
        self.ui.analyticsAllButton.clicked.connect(lambda: self.on_joint_filter_changed('all', 'analytics'))
        self.ui.analyticsHipButton.clicked.connect(lambda: self.on_joint_filter_changed('hip', 'analytics'))
        self.ui.analyticsKneeButton.clicked.connect(lambda: self.on_joint_filter_changed('knee', 'analytics'))
        self.ui.analyticsAnkleButton.clicked.connect(lambda: self.on_joint_filter_changed('ankle', 'analytics'))

        # Joint filter buttons for Comparative page
        self.ui.comparativeAllButton.clicked.connect(lambda: self.on_joint_filter_changed('all', 'comparative'))
        self.ui.comparativeHipButton.clicked.connect(lambda: self.on_joint_filter_changed('hip', 'comparative'))
        self.ui.comparativeKneeButton.clicked.connect(lambda: self.on_joint_filter_changed('knee', 'comparative'))
        self.ui.comparativeAnkleButton.clicked.connect(lambda: self.on_joint_filter_changed('ankle', 'comparative'))
        self.ui.newVerseButton.clicked.connect(self.on_new_verse_clicked)


        # Setup comparative page connections
        self.setup_comparative_page()

        self.ui.stackedWidget.currentChanged.connect(self.on_tab_changed)

        self.ui.skipButton.clicked.connect(self.on_skip_button_clicked)
        self.ui.backButton.clicked.connect(self.on_back_button_clicked)
        self.ui.fastForwardButton.clicked.connect(self.on_speed_up_button_clicked)
        self.ui.rewindButton.clicked.connect(self.on_speed_down_button_clicked)
        self.ui.centerAnimationButton.clicked.connect(self.on_center_animation_toggled)
        self.ui.axisButton.clicked.connect(self.on_axis_toggled)

        self.ui.processConfiguration.clicked.connect(self.on_process_configuration)
        self.params_manager.setup_connections()
        self.stats_manager.setup_connections()

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
            self.ui.processConfiguration.setEnabled(False)
            
            # Disable analytics and comparative buttons when changing session
            self.ui.analyticsButton.setEnabled(False)
            self.ui.jointAnalyticsButton.setEnabled(False)

            if hasattr(self, 'stats_manager'):
                self.stats_manager.reset_selected_trials()
            
            # If we are on Analytics or Comparative page, switch to Cameras page
            current_page = self.ui.stackedWidget.currentIndex()
            if current_page in [2, 3]:  # 2=Analytics, 3=Comparative
                self.ui.stackedWidget.setCurrentIndex(1)  # 1=Cameras page

    def on_select_participant(self):
        self.directory_manager.set_participant()
        participant_name = self.directory_manager.participant_dir
        
        if participant_name: 
            self.ui.participantSelectedLabel.setText(participant_name)
            self.ui.trialSelectButton.setEnabled(True)
            self.ui.trialAddButton.setEnabled(True)
            self.ui.processButton.setEnabled(False)
            self.ui.processConfiguration.setEnabled(False)
            
            # Disable analytics and comparative buttons when changing participant
            self.ui.analyticsButton.setEnabled(False)
            self.ui.jointAnalyticsButton.setEnabled(False)

            if hasattr(self, 'stats_manager'):
                self.stats_manager.check_selected_trials_validity()
            
            # If we are on Analytics or Comparative page, switch to Cameras page
            current_page = self.ui.stackedWidget.currentIndex()
            if current_page in [2, 3]:  # 2=Analytics, 3=Comparative
                self.ui.stackedWidget.setCurrentIndex(1)  # 1=Cameras page
    def on_select_trial(self):
        self.directory_manager.set_trial()
        trial_name = self.directory_manager.trial_dir

        self.ui.directoryValue.setText(self.directory_manager.trial_dir)

        self.camera_manager.save_directory = self.directory_manager.trial_path
        self.camera_manager.file_name = self.directory_manager.trial_name

        if trial_name:
            # Update trial name in main sidebar
            self.ui.trialSelectedLabel.setText(trial_name)
            
            # IMPORTANT: Update the base trial value in comparative page as well
            # This ensures it's updated even if we don't switch tabs
            if hasattr(self.ui, 'baseTrialValue'):
                self.ui.baseTrialValue.setText(trial_name)
                
            self.ui.processButton.setEnabled(True)
            
            # Check if processed data already exists for this trial
            self.motion_data_file = self.directory_manager.find_motion_csv_file()
            
            # Also store the MOT file path for use in comparative analysis
            self.base_mot_file = self.directory_manager.find_motion_mot_file()
            
            # Enable or disable analytics and comparative buttons based on motion file existence
            has_data = self.motion_data_file is not None
            self.ui.analyticsButton.setEnabled(has_data)
            self.ui.jointAnalyticsButton.setEnabled(has_data)
            self.ui.processConfiguration.setEnabled(True)
            
            # Reset verse trial data when a new trial is selected
            self.versus_data_file = None
            self.versus_mot_file = None
            if hasattr(self, 'versus_motion_data'):
                self.versus_motion_data = None
            
            # Reset versus UI elements
            if hasattr(self.ui, 'versusTrialValue'):
                self.ui.versusTrialValue.setText("-")  # Reset to default value
            
            if hasattr(self, 'stats_manager'):
                self.stats_manager.check_selected_trials_validity()
            
            self.update_comparative_stats_button_state()

            if hasattr(self, 'params_manager'):
                self.params_manager.refresh_dialog()
            
            # After resetting verse data, try to find a reference file
            self.versus_data_file = self.directory_manager.find_reference_csv_file()
            
            # If data file was found, update display
            if self.motion_data_file:
                self.on_display_data()
                
                # If we're currently on the comparative page, we need to
                # reload the comparative data with the new trial
                if self.ui.stackedWidget.currentIndex() == 3:  # 3 = Comparative page
                    self.load_comparative_data()
            else:
                # If we are on Analytics or Comparative page and there's no data,
                # automatically go back to Cameras page
                current_page = self.ui.stackedWidget.currentIndex()
                if current_page in [2, 3]:  # 2=Analytics, 3=Comparative
                    self.ui.stackedWidget.setCurrentIndex(1)  # 1=Cameras page 
    def add_participant(self):
        self.directory_manager.add_participant()
    def add_trial(self):
        self.directory_manager.add_trial()

    # --- Cameras Page Functions --- #
    def on_detect_cameras(self):
        self.camera_manager.detect_available_cameras(max_cameras=3)
    
        # Update UI elements
        self.ui.camerasValue.setText(str(self.camera_manager.camera_count))
        self.ui.framerateValue.setText(str(self.camera_manager.framerates))
        self.ui.resolutionValue.setText(str(self.camera_manager.resolution))
    def on_close_cameras(self):
        self.camera_manager.close_all_cameras()
        self.ui.camerasValue.setText(str(self.camera_manager.camera_count))
    def on_start_recording(self):
        self.camera_manager.start_recording_all_cameras() 
    def on_stop_recording(self):
        self.camera_manager.stop_recording_all_cameras()

    # --- Analytics Page Functions --- #
    def setup_analytics_buttons(self):
        self.analytics_filter_group = QButtonGroup(self)
        self.analytics_filter_group.addButton(self.ui.analyticsAllButton)
        self.analytics_filter_group.addButton(self.ui.analyticsHipButton)
        self.analytics_filter_group.addButton(self.ui.analyticsKneeButton)
        self.analytics_filter_group.addButton(self.ui.analyticsAnkleButton)
        self.analytics_filter_group.setExclusive(True)
        self.ui.analyticsAllButton.setChecked(True)
    def reapply_chart_vertical_line(self):
        # Check if we're on the analytics page
        if self.ui.stackedWidget.currentIndex() == 2:
            # Call the method from the chart manager
            self.chart_manager.reapply_chart_vertical_line(
                self.current_highlighted_row
            )
    def reapply_table_highlighting(self):
        # Check if we're on the analytics page (tab index 2)
        if self.ui.stackedWidget.currentIndex() == 2:
            # Call the method from the table manager
            self.table_manager.reapply_table_highlighting(
                self.ui.jointsTable, 
                self.current_highlighted_row
            )
    def on_display_data(self):
        try:
            if self.motion_data_file:
                    motion_data = self.data_manager.read_csv_file(self.motion_data_file)
                    # Store the motion data for later use
                    self.motion_data = motion_data
                    
                    # ADDED: Also update the base_motion_data for comparative page
                    self.base_motion_data = motion_data
                    
                    if motion_data:
                        self.table_manager.display_data_in_table(self.ui.jointsTable, motion_data, True, "all")
                        self.chart_manager.display_data_in_chart(self.ui.trialChart, motion_data, False, "all")

                        # ADDED: Update the comparative page base trial if it exists
                        if hasattr(self.ui, 'baseTrialTable') and hasattr(self.ui, 'baseTrialChart'):
                            self.table_manager.display_data_in_table(self.ui.baseTrialTable, motion_data, True, "all")
                            self.chart_manager.display_data_in_chart(self.ui.baseTrialChart, motion_data, False, "all")
                        
                        # ADDED: If we're currently on the comparative page, update trial value
                        if self.ui.stackedWidget.currentIndex() == 3 and hasattr(self.ui, 'baseTrialValue'):
                            self.ui.baseTrialValue.setText(self.directory_manager.trial_dir)

                        num_rows = len(motion_data['time'])
                        self.ui.slider.setMinimum(0)
                        self.ui.slider.setMaximum(num_rows - 1)
                        self.ui.slider.setValue(0)
                            
                        # Initialize highlighting for the first row
                        self.table_manager.highlight_row(self.ui.jointsTable, 0)
                        
                        # Initialize the gait stage value
                        self.update_gait_stage_value(0)
                    else:
                        pass
            else:
                pass
                
        finally:
            # Restore cursor
            QApplication.restoreOverrideCursor()
    def update_analytics_chart(self, joint_filter):
        """Update the chart in the analytics page based on the selected joint filter"""
        try:
            motion_data = self.data_manager.read_csv_file(self.motion_data_file)
            
            if motion_data:
                # Update the chart with the selected joint filter
                self.chart_manager.display_data_in_chart(
                    self.ui.trialChart,
                    motion_data,
                    False,  # Not scrollable
                    joint_filter
                )
                
        except Exception as e:
            print(f"Error updating analytics chart: {str(e)}")
    def on_slider_value_changed(self, value):
        """
        Handles when the slider value changes in the PyQt UI
        
        Args:
            value (int): The current slider value
        """
        # Store the current row index
        self.current_highlighted_row = value
        
        # Update the table highlight
        self.table_manager.highlight_row(self.ui.jointsTable, value)
        
        # Update the vertical line position on the chart
        self.chart_manager.update_vertical_line(value)
        
        # Update the gait stage value if data is available
        self.update_gait_stage_value(value)
        
        # Sync the 3D viewer with the slider
        if hasattr(self, 'viewer_manager') and self.viewer_manager:
            max_value = self.ui.slider.maximum()
            self.viewer_manager.sync_with_slider(value, max_value)
            
  # --- Comparative Page Functions --- #
    def setup_comparative_page(self):
        """Setup the comparative page with initial data and connections"""
        # Connect joint filter buttons
        self.ui.comparativeAllButton.clicked.connect(
            lambda: self.on_comparative_joint_filter_changed('all'))
        self.ui.comparativeHipButton.clicked.connect(
            lambda: self.on_comparative_joint_filter_changed('hip'))
        self.ui.comparativeKneeButton.clicked.connect(
            lambda: self.on_comparative_joint_filter_changed('knee'))
        self.ui.comparativeAnkleButton.clicked.connect(
            lambda: self.on_comparative_joint_filter_changed('ankle'))
        
        # Connect file selection buttons (if they exist in the UI)
        if hasattr(self.ui, 'selectBaseTrialButton'):
            self.ui.selectBaseTrialButton.clicked.connect(self.select_base_trial_file)
        if hasattr(self.ui, 'selectVersusTrialButton'):
            self.ui.selectVersusTrialButton.clicked.connect(self.select_versus_trial_file)
        
        # Initialize with data if available
        self.ui.comparativeSlider.valueChanged.connect(self.on_comparative_slider_value_changed)

        self.load_comparative_data()
    def load_comparative_data(self):
        """Load data for the comparative analysis page"""
        try:            
            # Load base trial data
            if hasattr(self, 'motion_data') and self.motion_data:
                print("Base motion data available")
                # Use the motion data from the Analytics page as the base trial
                self.base_motion_data = self.motion_data
                
                if self.base_motion_data:
                    self.table_manager.display_data_in_table(
                        self.ui.baseTrialTable, 
                        self.base_motion_data, 
                        True,  # scrollable 
                        "all"  # all joints
                    )
                    
                    self.chart_manager.display_data_in_chart(
                        self.ui.baseTrialChart, 
                        self.base_motion_data, 
                        False,  # not scrollable
                        "all"   # all joints
                    )
                    
                    # Update UI
                    self.ui.baseTrialValue.setText(self.directory_manager.trial_dir)
            
            
            # Load versus trial data if available
            if self.versus_data_file:
                print(f"Loading versus data from {self.versus_data_file}")
                # Check file extension to determine how to read it
                if self.versus_data_file.endswith('.mot'):
                    self.versus_motion_data = self.data_manager.read_mot_file(self.versus_data_file)
                else:
                    self.versus_motion_data = self.data_manager.read_csv_file(self.versus_data_file)
                
                if self.versus_motion_data:
                    print("Versus motion data loaded successfully")
                    self.table_manager.display_data_in_table(
                        self.ui.versusTrialTable, 
                        self.versus_motion_data, 
                        True,  # scrollable 
                        "all"  # all joints
                    )
                    
                    self.chart_manager.display_data_in_chart(
                        self.ui.versusTrialChart, 
                        self.versus_motion_data, 
                        False,  # not scrollable
                        "all"   # all joints
                    )
                    
                    # Get 'versus' trial name from file path
                    versus_trial_name = os.path.basename(self.versus_data_file)
                    versus_trial_name = os.path.splitext(versus_trial_name)[0]
                    
                    # Update UI
                    if hasattr(self.ui, 'versusTrialValue'):
                        self.ui.versusTrialValue.setText(versus_trial_name)
                else:
                    print("Failed to load versus motion data")
                    # Clear versus charts and tables if data couldn't be loaded
                    self.clear_versus_display()
            else:
                # Clear versus charts and tables if no file is selected
                self.clear_versus_display()
            
            # Set up the slider for the comparative page
            max_rows = 0
            if hasattr(self, 'base_motion_data') and 'time' in self.base_motion_data:
                max_rows = max(max_rows, len(self.base_motion_data['time']))
                
            if hasattr(self, 'versus_motion_data') and self.versus_motion_data and 'time' in self.versus_motion_data:
                max_rows = max(max_rows, len(self.versus_motion_data['time']))
                
            if max_rows > 0:
                print(f"Setting comparative slider range: 0-{max_rows-1}")
                self.ui.comparativeSlider.setMinimum(0)
                self.ui.comparativeSlider.setMaximum(max_rows - 1)
                self.ui.comparativeSlider.setValue(0)
                
                # Initialize highlighting for the first row in both tables
                self.table_manager.highlight_row(self.ui.baseTrialTable, 0)
                if hasattr(self, 'versus_motion_data') and self.versus_motion_data:
                    self.table_manager.highlight_row(self.ui.versusTrialTable, 0)
                
                # Initialize the gait stage values
                self.update_comparative_gait_stage_values(0)

            self.update_comparative_stats_button_state()
        except Exception as e:
            print(f"Error loading comparative data: {str(e)}")
            import traceback
            traceback.print_exc()  # More detailed error information
    def on_comparative_joint_filter_changed(self, joint_filter):
        """
        Handle joint filter button clicks on the comparative page
        
        Args:
            joint_filter (str): Type of filter ("all", "hip", "knee", "ankle")
        """
        try:
            print(f"Changing comparative filter to: {joint_filter}")
            
            # Update base trial display
            if hasattr(self, 'base_motion_data') and self.base_motion_data:
                self.table_manager.display_data_in_table(
                    self.ui.baseTrialTable, 
                    self.base_motion_data, 
                    True,  # scrollable
                    joint_filter
                )
                self.chart_manager.display_data_in_chart(
                    self.ui.baseTrialChart, 
                    self.base_motion_data, 
                    False,  # not scrollable
                    joint_filter
                )
                
            # Update versus trial display
            if hasattr(self, 'versus_motion_data') and self.versus_motion_data:
                self.table_manager.display_data_in_table(
                    self.ui.versusTrialTable, 
                    self.versus_motion_data, 
                    True,  # scrollable
                    joint_filter
                )
                self.chart_manager.display_data_in_chart(
                    self.ui.versusTrialChart, 
                    self.versus_motion_data, 
                    False,  # not scrollable
                    joint_filter
                )
            
            # Reapply highlighting and vertical lines after updates
            QTimer.singleShot(5, self.reapply_comparative_table_highlighting)
            QTimer.singleShot(5, self.reapply_comparative_chart_vertical_lines)
                
        except Exception as e:
            print(f"Error updating comparative filter: {str(e)}")
            import traceback
            traceback.print_exc()
    def setup_comparative_buttons(self):
        self.comparative_filter_group = QButtonGroup(self)
        self.comparative_filter_group.addButton(self.ui.comparativeAllButton)
        self.comparative_filter_group.addButton(self.ui.comparativeHipButton)
        self.comparative_filter_group.addButton(self.ui.comparativeKneeButton)
        self.comparative_filter_group.addButton(self.ui.comparativeAnkleButton)
        self.comparative_filter_group.setExclusive(True)
        self.ui.comparativeAllButton.setChecked(True)
    def on_comparative_slider_value_changed(self, value):
        """
        Handles when the comparative slider value changes by highlighting the corresponding rows in both tables,
        updating the vertical lines on both charts, and updating both gait stage values.
        
        Args:
            value (int): The current slider value, corresponding directly to the row index
        """
        # Store the current row index
        self.current_comparative_row = value
        
        # Update the base trial table highlight
        if hasattr(self, 'base_motion_data') and self.ui.baseTrialTable.rowCount() > 0:
            self.table_manager.highlight_row(self.ui.baseTrialTable, value)
        
        # Update the versus trial table highlight
        if hasattr(self, 'versus_motion_data') and self.ui.versusTrialTable.rowCount() > 0:
            self.table_manager.highlight_row(self.ui.versusTrialTable, value)
        
        # Update the vertical line positions on both charts
        self.chart_manager.update_comparative_vertical_lines(value)
        
        # Update the gait stage values for both trials
        self.update_comparative_gait_stage_values(value)
    def update_comparative_gait_stage_values(self, row_index):
        """
        Updates both gait stage values in the comparative UI based on the current row index
        
        Args:
            row_index (int): The current row index corresponding to the slider value
        """
        try:
            # Update base trial gait stage
            if hasattr(self, 'base_motion_data') and self.base_motion_data and 'gait_phase' in self.base_motion_data:
                gait_phases = self.base_motion_data['gait_phase']
                
                # Ensure the row index is valid
                if 0 <= row_index < len(gait_phases):
                    # Get the gait phase at the current index
                    current_phase = gait_phases[row_index]
                    
                    # Update the UI element
                    if hasattr(self.ui, 'label'):  # The base gait stage value label
                        self.ui.label.setText(current_phase)
                else:
                    # Reset the UI element if index is out of range
                    if hasattr(self.ui, 'label'):
                        self.ui.label.setText("N/A")
                        
            # Update versus trial gait stage
            if hasattr(self, 'versus_motion_data') and self.versus_motion_data and 'gait_phase' in self.versus_motion_data:
                gait_phases = self.versus_motion_data['gait_phase']
                
                # Ensure the row index is valid
                if 0 <= row_index < len(gait_phases):
                    # Get the gait phase at the current index
                    current_phase = gait_phases[row_index]
                    
                    # Update the UI element
                    if hasattr(self.ui, 'label_5'):  # The versus gait stage value label
                        self.ui.label_5.setText(current_phase)
                else:
                    # Reset the UI element if index is out of range
                    if hasattr(self.ui, 'label_5'):
                        self.ui.label_5.setText("N/A")
                        
        except Exception as e:
            print(f"Error updating comparative gait stage values: {str(e)}")
            
            # Set fallback values
            if hasattr(self.ui, 'label'):
                self.ui.label.setText("Error")
            if hasattr(self.ui, 'label_5'):
                self.ui.label_5.setText("Error")
    def reapply_comparative_table_highlighting(self):
        # Check if we're on the comparative page (tab index 3)
        if self.ui.stackedWidget.currentIndex() == 3:
            # Call the method from the table manager for both tables
            if hasattr(self, 'base_motion_data') and self.ui.baseTrialTable.rowCount() > 0:
                self.table_manager.reapply_table_highlighting(
                    self.ui.baseTrialTable, 
                    self.current_comparative_row
                )
                
            if hasattr(self, 'versus_motion_data') and self.ui.versusTrialTable.rowCount() > 0:
                self.table_manager.reapply_table_highlighting(
                    self.ui.versusTrialTable, 
                    self.current_comparative_row
                )
    def reapply_comparative_chart_vertical_lines(self):
        # Check if we're on the comparative page
        if self.ui.stackedWidget.currentIndex() == 3:
            # Call the method from the chart manager
            self.chart_manager.reapply_comparative_chart_vertical_lines(
                self.current_comparative_row
            )
    def on_new_verse_clicked(self):
        """
        Handles when the 'Choose Verse' button is clicked to select a different trial for comparison.
        Opens a file dialog to select a trial folder and ensures it's not the same as the base trial.
        Uses CSV files for visualization (tables/charts) and MOT files for comparative analysis.
        Specifically looks for files matching the "*_original.csv" pattern.
        """
        try:
            # Get current base trial directory path (if any)
            current_base_trial_path = self.directory_manager.trial_path
            
            # Create a file dialog
            dialog = QFileDialog(self)
            dialog.setFileMode(QFileDialog.Directory)
            dialog.setOption(QFileDialog.ShowDirsOnly, True)
            
            # Set the initial directory to the participant folder
            if self.directory_manager.participant_path:
                dialog.setDirectory(self.directory_manager.participant_path)
            elif self.directory_manager.session_path:
                dialog.setDirectory(self.directory_manager.session_path)
            
            # Show the dialog and get selected directory
            if dialog.exec_():
                selected_path = dialog.selectedFiles()[0]
                
                # Prevent selecting the same trial as the base trial
                if selected_path == current_base_trial_path:
                    QMessageBox.warning(
                        self,
                        "Invalid Selection",
                        "The verse trial cannot be the same as the base trial."
                    )
                    return
                
                # Check if the selected directory is a valid trial folder
                # (trial folders should start with 'T' followed by numbers)
                trial_dir = os.path.basename(selected_path)
                if not (trial_dir.startswith('T') and trial_dir.split('_')[0][1:].isdigit()):
                    QMessageBox.warning(
                        self,
                        "Invalid Selection",
                        "Please select a valid trial folder (starts with 'T')."
                    )
                    return
                
                # 1. Find CSV file for visualization in tables and charts
                # Look in multiple possible directories for files matching the "*_original.csv" pattern
                csv_file_path = None
                
                # First, check the gait-classification directory
                gait_class_dir = os.path.join(selected_path, "gait-classification")
                if os.path.exists(gait_class_dir):
                    # Find all CSV files matching the "*_original.csv" pattern
                    original_csv_files = glob.glob(os.path.join(gait_class_dir, "*_original.csv"))
                    if original_csv_files:
                        # Use the first matching CSV file found
                        csv_file_path = original_csv_files[0]
                        print(f"Found original CSV file: {csv_file_path}")
                
                # If not found in gait-classification, check the trial root directory
                if not csv_file_path:
                    original_csv_files = glob.glob(os.path.join(selected_path, "*_original.csv"))
                    if original_csv_files:
                        csv_file_path = original_csv_files[0]
                        print(f"Found original CSV file in trial root: {csv_file_path}")
                
                # If not found with _original pattern, fall back to any CSV in gait-classification
                if not csv_file_path and os.path.exists(gait_class_dir):
                    csv_files = [f for f in os.listdir(gait_class_dir) if f.endswith('.csv')]
                    if csv_files:
                        csv_file_path = os.path.join(gait_class_dir, csv_files[0])
                        print(f"No '*_original.csv' file found, falling back to: {csv_file_path}")
                
                if not csv_file_path:
                    QMessageBox.warning(
                        self,
                        "Missing Data",
                        f"No CSV data found in {trial_dir}. Please process this trial first."
                    )
                    return
                
                # 2. Find MOT file for comparative analysis
                kinematics_dir = os.path.join(selected_path, "kinematics")
                mot_file_path = None
                
                if os.path.exists(kinematics_dir):
                    # Find MOT files in the kinematics directory
                    mot_files = [f for f in os.listdir(kinematics_dir) if f.endswith('.mot')]
                    if mot_files:
                        # Use the first MOT file found
                        mot_file_path = os.path.join(kinematics_dir, mot_files[0])
                
                if not mot_file_path:
                    QMessageBox.warning(
                        self,
                        "Missing Data",
                        f"No MOT data found in {trial_dir}. Please process this trial first."
                    )
                    return
                
                # 3. Load the CSV data for visualization
                verse_motion_data = self.data_manager.read_csv_file(csv_file_path)
                if not verse_motion_data:
                    QMessageBox.warning(
                        self,
                        "Data Loading Error",
                        f"Failed to load CSV data from {csv_file_path}."
                    )
                    return
                
                # Store both file paths and data for later use
                self.versus_data_file = csv_file_path  # For visualization
                self.versus_mot_file = mot_file_path   # For comparative analysis
                self.versus_motion_data = verse_motion_data
                
                # Update the comparative stats button state
                self.update_comparative_stats_button_state()

                # Update the UI elements
                self.ui.versusTrialValue.setText(trial_dir)
                
                # Refresh the table and chart with the new data
                current_filter = "all"
                if self.ui.comparativeHipButton.isChecked():
                    current_filter = "hip"
                elif self.ui.comparativeKneeButton.isChecked():
                    current_filter = "knee"
                elif self.ui.comparativeAnkleButton.isChecked():
                    current_filter = "ankle"
                
                # Update the table and chart with the new data
                self.table_manager.display_data_in_table(
                    self.ui.versusTrialTable, 
                    self.versus_motion_data, 
                    True,  # scrollable 
                    current_filter
                )
                
                self.chart_manager.display_data_in_chart(
                    self.ui.versusTrialChart, 
                    self.versus_motion_data, 
                    False,  # not scrollable
                    current_filter
                )
                
                # Reset the comparative slider
                max_rows = 0
                if hasattr(self, 'base_motion_data') and 'time' in self.base_motion_data:
                    max_rows = max(max_rows, len(self.base_motion_data['time']))
                    
                if 'time' in self.versus_motion_data:
                    max_rows = max(max_rows, len(self.versus_motion_data['time']))
                    
                if max_rows > 0:
                    self.ui.comparativeSlider.setMinimum(0)
                    self.ui.comparativeSlider.setMaximum(max_rows - 1)
                    self.ui.comparativeSlider.setValue(0)
                    
                    # Initialize highlighting for the first row in the versus table
                    self.table_manager.highlight_row(self.ui.versusTrialTable, 0)
                    
                    # Update comparative chart vertical lines
                    self.chart_manager.reapply_comparative_chart_vertical_lines(0)
                
                QMessageBox.information(
                    self,
                    "Success",
                    f"Selected '{trial_dir}' as the verse trial for comparison."
                )
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"An error occurred when selecting verse trial: {str(e)}"
            )
            import traceback
            traceback.print_exc()
    def clear_versus_display(self):
        """Clear versus trial display elements when no versus data is available"""
        # Clear the table
        self.ui.versusTrialTable.clear()
        self.ui.versusTrialTable.setRowCount(0)
        self.ui.versusTrialTable.setColumnCount(0)

        # Disable stats button
        self.ui.comparativeStatsButton.setEnabled(False)

        # Clear the chart
        # We need to create an empty chart to replace the existing one
        if hasattr(self.chart_manager, 'versus_chart') and self.chart_manager.versus_chart:
            # Use an empty layout to effectively clear the chart
            if self.ui.versusTrialChart.layout() is not None:
                layout = self.ui.versusTrialChart.layout()
                while layout.count():
                    item = layout.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()
        
        # Reset the versus trial value label
        if hasattr(self.ui, 'versusTrialValue'):
            self.ui.versusTrialValue.setText("-")
    def update_comparative_stats_button_state(self):
        """
        Update the state of the comparative stats button based on whether versus data is available
        """
        if hasattr(self, 'versus_motion_data') and self.versus_motion_data is not None:
            self.ui.comparativeStatsButton.setEnabled(True)
        else:
            self.ui.comparativeStatsButton.setEnabled(False)
    
    # --- Table & Charts Functions --- # 
    def on_tab_changed(self, index):
        """
        Handle tab changes and reapply highlighting when needed
        
        Args:
            index (int): The index of the newly selected tab
        """
        # Check if we're switching to the analytics/simulation page (tab index 2)
        if index == 2:  # Analytics tab        
            # If params button is checked, ensure dialog is shown
            if hasattr(self.ui, 'paramsButton') and self.ui.paramsButton.isChecked():
                if hasattr(self, 'params_manager'):
                    self.params_manager.on_params_button_toggled(True)
        
        # If switching away from analytics tab, hide the params dialog
        elif hasattr(self, 'params_manager') and hasattr(self.params_manager, 'dialog') and self.params_manager.dialog:
            # Only hide if we're leaving the analytics tab
            if self.ui.stackedWidget.currentIndex() == 2:  # Coming from analytics tab
                self.params_manager.dialog.hide()
                # Uncheck the button to maintain consistency
                if hasattr(self.ui, 'paramsButton'):
                    self.ui.paramsButton.setChecked(False)

        
        # Check if we're switching to the comparative page (tab index 3)
        elif index == 3:  # Comparative tab
            # If we have motion data loaded, use it as the base trial
            if hasattr(self, 'motion_data') and self.motion_data:
                # Set the base_motion_data to the current motion_data
                self.base_motion_data = self.motion_data
                
                # Update the base trial UI elements
                if hasattr(self.ui, 'baseTrialValue') and self.directory_manager.trial_dir:
                    self.ui.baseTrialValue.setText(self.directory_manager.trial_dir)
                
                # Update the base trial table and chart
                self.table_manager.display_data_in_table(
                    self.ui.baseTrialTable, 
                    self.base_motion_data, 
                    True,  # scrollable 
                    "all"  # all joints
                )
                
                self.chart_manager.display_data_in_chart(
                    self.ui.baseTrialChart, 
                    self.base_motion_data, 
                    False,  # not scrollable
                    "all"   # all joints
                )
            
            # Make sure the slider value matches the current comparative row
            self.ui.comparativeSlider.setValue(self.current_comparative_row)
            
            # Use a short timer to ensure UI is fully updated before highlighting
            self.reapply_comparative_table_highlighting()
            self.reapply_comparative_chart_vertical_lines()
            
            # Update both gait stage values
            self.update_comparative_gait_stage_values(self.current_comparative_row)

    # Update the on_joint_filter_changed method to reapply highlighting
    def on_joint_filter_changed(self, joint_filter, page_type):
        """
        Handle joint filter button clicks
        
        Args:
            joint_filter (str): Type of filter ("all", "hip", "knee", "ankle")
            page_type (str): Which page to update ("analytics" or "comparative")
        """
        try:
            if page_type == "analytics":
                # Simulation page - update only the analytics table
                motion_data = self.data_manager.read_csv_file(self.motion_data_file)
                if motion_data:
                    self.table_manager.display_data_in_table(
                        self.ui.jointsTable, 
                        motion_data, 
                        True,  # scrollable 
                        joint_filter
                    )
                    # Also update the chart if needed
                    self.update_analytics_chart(joint_filter)
                    
                    # Reapply highlighting after table update
                    QTimer.singleShot(5, self.reapply_table_highlighting)
                    
                    # Also reapply the chart's vertical line after the chart is updated
                    QTimer.singleShot(5, self.reapply_chart_vertical_line)
            
            elif page_type == "comparative":
                # Comparative page - update both base and versus tables/charts
                if hasattr(self, 'base_motion_data') and self.base_motion_data:
                    self.table_manager.display_data_in_table(
                        self.ui.baseTrialTable, 
                        self.base_motion_data, 
                        True,  # scrollable 
                        joint_filter
                    )
                    
                    self.chart_manager.display_data_in_chart(
                        self.ui.baseTrialChart, 
                        self.base_motion_data, 
                        False,  # not scrollable
                        joint_filter
                    )
                
                if hasattr(self, 'versus_motion_data') and self.versus_motion_data:
                    self.table_manager.display_data_in_table(
                        self.ui.versusTrialTable, 
                        self.versus_motion_data, 
                        True,  # scrollable 
                        joint_filter
                    )
                    
                    self.chart_manager.display_data_in_chart(
                        self.ui.versusTrialChart, 
                        self.versus_motion_data, 
                        False,  # not scrollable
                        joint_filter
                    )
                
                # Reapply highlighting and vertical lines after updates
                QTimer.singleShot(5, self.reapply_comparative_table_highlighting)
                QTimer.singleShot(5, self.reapply_comparative_chart_vertical_lines)
                    
        except Exception as e:
            print(f"Error updating table filter: {str(e)}")
    def update_gait_stage_value(self, row_index):
        """
        Updates the gaitStageValue text in the UI based on the current row index
        
        Args:
            row_index (int): The current row index corresponding to the slider value
        """
        try:
            # Check if motion data is available and contains gait phase information
            if hasattr(self, 'motion_data') and self.motion_data and 'gait_phase' in self.motion_data:
                gait_phases = self.motion_data['gait_phase']
                
                # Ensure the row index is valid
                if 0 <= row_index < len(gait_phases):
                    # Get the gait phase at the current index
                    current_phase = gait_phases[row_index]
                    
                    # Update the UI element
                    if hasattr(self.ui, 'gaitStageValue'):
                        self.ui.gaitStageValue.setText(current_phase)
                    
                else:
                    # Reset the UI element if index is out of range
                    if hasattr(self.ui, 'gaitStageValue'):
                        self.ui.gaitStageValue.setText("N/A")

        except Exception as e:
            print(f"Error updating gait stage value: {str(e)}")
            
            # Set a fallback value
            if hasattr(self.ui, 'gaitStageValue'):
                self.ui.gaitStageValue.setText("Error")

    # --- Processing Function --- #
    def on_process(self):
        """Handle the processing of the selected trial"""
        try:
            # Load configuration files
            participant_config_path = os.path.join(self.directory_manager.participant_path, "Config.toml")
            participant_config_dict = toml.load(participant_config_path)
            participant_config_dict.get("project").update({"project_dir": os.path.join(self.directory_manager.participant_path)})

            trial_config_path = os.path.join(self.directory_manager.trial_path, "Config.toml")
            trial_config_dict = toml.load(trial_config_path)
            trial_config_dict.get("project").update({"project_dir": self.directory_manager.trial_path})

            # Create progress dialog
            progress_dialog = QProgressDialog("Processing trial...", "Cancel", 0, 10, self)
            progress_dialog.setWindowTitle("Processing")
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.setValue(0)
            progress_dialog.show()
            QApplication.processEvents()

            # Get process states from configuration dialog
            process_config = self.process_manager.get_process_configuration()
            
            # --- Step 1: Pose Estimation --- #
            if process_config.get('pose_estimation', True):
                progress_dialog.setLabelText("Step 1/7: Pose Estimation...")
                QApplication.processEvents()

                # Update the pose_model in the Config.toml based on the selected algorithm
                if 'pose' not in trial_config_dict:
                    trial_config_dict['pose'] = {}
                    
                # Set the appropriate pose_model based on the algorithm
                if self.directory_manager.algorithm == "rtmpose":
                    print("Using RTMPose for pose estimation - setting pose_model to 'Body_with_feet'")
                    trial_config_dict['pose']['pose_model'] = 'Body_with_feet'
                    
                    # Save the updated Config.toml file
                    with open(trial_config_path, 'w') as f:
                        toml.dump(trial_config_dict, f)
                        
                    # Proceed with RTMPose estimation
                    Pose2Sim.poseEstimation(trial_config_dict)
                else:  # Default is "openpose"
                    print("Using OpenPose for pose estimation - setting pose_model to 'BODY_25'")
                    trial_config_dict['pose']['pose_model'] = 'BODY_25'
                    
                    # Save the updated Config.toml file
                    with open(trial_config_path, 'w') as f:
                        toml.dump(trial_config_dict, f)
                    # Create the pose directory structure if it doesn't exist
                    pose_dir = os.path.join(self.directory_manager.trial_path, "pose")
                    if not os.path.exists(pose_dir):
                        os.makedirs(pose_dir)
                        
                    # Find video files in the trial directory
                    videos_dir = os.path.join(self.directory_manager.trial_path, "videos")
                    if not os.path.exists(videos_dir):
                        raise ValueError(f"No videos directory found at {videos_dir}. Please record videos first.")
                    
                    # Debug: Print directory information to help diagnose import issues
                    print(f"Current working directory: {os.getcwd()}")
                    main_dir = os.path.dirname(os.path.abspath(__file__))
                    print(f"Directory of main.py: {main_dir}")
                    
                    # Find the openposelocal.py file by searching for it
                    openpose_local_path = None
                    
                    # Common locations to search
                    possible_paths = [
                        os.path.join(os.getcwd(), 'utils', 'openpose', 'openposelocal.py'),
                        os.path.join(main_dir, 'utils', 'openpose', 'openposelocal.py'),
                        os.path.join(os.path.dirname(main_dir), 'utils', 'openpose', 'openposelocal.py'),
                        # Search for utils directory recursively up to 3 levels up
                        *[os.path.join(os.path.dirname(os.path.abspath(__file__)), *['..'] * i, 'utils', 'openpose', 'openposelocal.py') 
                        for i in range(4)]
                    ]
                    
                    # Try to find the file
                    for path in possible_paths:
                        norm_path = os.path.normpath(os.path.abspath(path))
                        print(f"Checking for openposelocal.py at: {norm_path}")
                        if os.path.isfile(norm_path):
                            openpose_local_path = norm_path
                            print(f"Found openposelocal.py at: {norm_path}")
                            break
                    
                    if not openpose_local_path:
                        raise ImportError("Could not find openposelocal.py in any expected location")
                    
                    # Import using the file path directly
                    import importlib.util
                    spec = importlib.util.spec_from_file_location("openposelocal", openpose_local_path)
                    openpose_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(openpose_module)
                    OpenPoseRunner = openpose_module.OpenPoseRunner
                    
                    # Initialize OpenPoseRunner
                    runner = OpenPoseRunner()
                    
                    # Set OpenPose path from directory manager
                    openpose_path = self.directory_manager.openpose_path
                    if not openpose_path or not os.path.exists(openpose_path):
                        raise ValueError("OpenPose path not properly configured. Please set it in the configuration dialog.")
                    
                    # Find OpenPoseDemo.exe in the openpose_path directory
                    openpose_exe = None
                    for root, dirs, files in os.walk(openpose_path):
                        for file in files:
                            if file == "OpenPoseDemo.exe" or file == "openpose.exe" or file == "OpenPoseDemo":
                                openpose_exe = os.path.join(root, file)
                                break
                        if openpose_exe:
                            break
                    
                    if not openpose_exe:
                        # If not found, try with default locations based on the provided path
                        if os.path.exists(os.path.join(openpose_path, "bin", "OpenPoseDemo.exe")):
                            openpose_exe = os.path.join(openpose_path, "bin", "OpenPoseDemo.exe")
                        elif os.path.exists(os.path.join(openpose_path, "OpenPoseDemo.exe")):
                            openpose_exe = os.path.join(openpose_path, "OpenPoseDemo.exe")
                        else:
                            raise ValueError(f"OpenPoseDemo.exe not found in {openpose_path} or its subdirectories.")
                    
                    runner.set_openpose_path(openpose_exe)
                    
                    # Set model folder from directory manager or default location
                    model_path = self.directory_manager.model_path
                    if not model_path or not os.path.exists(model_path):
                        # Try to find models folder in openpose_path
                        if os.path.exists(os.path.join(openpose_path, "models")):
                            model_path = os.path.join(openpose_path, "models")
                        else:
                            raise ValueError("Model path not properly configured. Please set it in the configuration dialog.")
                    
                    runner.set_model_folder(model_path)
                    
                    # Set input and output directories
                    runner.set_input_directory(videos_dir)
                    runner.set_output_directory(pose_dir)
                    
                    # Load default config or create one with your desired settings
                    openpose_config = {
                        'face': False,
                        'hand': False,
                        'net_resolution': '-1x368',  # Use -1 to maintain aspect ratio with 368px height
                        'model_pose': 'BODY_25',
                        'number_people_max': 5
                    }
                    
                    # Get trial-specific openpose.toml if available
                    trial_openpose_config_path = os.path.join(self.directory_manager.trial_path, "openpose.toml")
                    if os.path.exists(trial_openpose_config_path):
                        try:
                            config = toml.load(trial_openpose_config_path)
                            
                            # Handle OpenPose section if it exists
                            if 'openpose' in config:
                                openpose_config.update(config['openpose'])
                            
                            # Also look for direct keys
                            for key, value in config.items():
                                if key not in ['openpose'] and not isinstance(value, dict):
                                    openpose_config[key] = value
                                    
                            print(f"Loaded OpenPose configuration from {trial_openpose_config_path}")
                        except Exception as e:
                            print(f"Error loading openpose.toml: {str(e)}")
                    
                    # Also apply pose settings from the trial Config.toml
                    if 'pose' in trial_config_dict:
                        pose_config = trial_config_dict['pose']
                        
                        # Apply specific settings from pose section
                        if 'pose_model' in pose_config and pose_config['pose_model'] == 'BODY_25':
                            openpose_config['model_pose'] = 'BODY_25'
                    
                    # Apply settings from the directory manager's openpose configuration
                    if self.directory_manager.openpose_path:
                        if 'net_resolution' in openpose_config:
                            print(f"Using net_resolution: {openpose_config['net_resolution']}")
                    
                    # Debug: Print the final OpenPose config
                    print("Final OpenPose configuration:")
                    for key, value in openpose_config.items():
                        print(f"  {key}: {value}")
                    
                    runner.config = openpose_config
                    
                    # Process the videos - this function will wait for OpenPose to finish
                    print("Starting OpenPose processing...")
                    runner.process_videos()
                    print("OpenPose processing complete.")
                    
                    # Verify output
                    json_files_found = False
                    for root, dirs, files in os.walk(pose_dir):
                        for file in files:
                            if file.endswith('.json'):
                                json_files_found = True
                                break
                        if json_files_found:
                            break
                    
                    if not json_files_found:
                        raise ValueError(f"No JSON files were created by OpenPose in {pose_dir}. Check OpenPose settings and try again.")
            
            progress_dialog.setValue(1)
            
            # --- Step 2: Synchronization --- #
            if process_config.get('synchronization', True):
                progress_dialog.setLabelText("Step 2/10: Synchronization...")
                QApplication.processEvents()
                Pose2Sim.synchronization(trial_config_dict)
            progress_dialog.setValue(2)
            
            # --- Step 3: Triangulation --- #
            if process_config.get('triangulation', True):
                progress_dialog.setLabelText("Step 3/10: Triangulation...")
                QApplication.processEvents()
                Pose2Sim.triangulation(trial_config_dict)
            progress_dialog.setValue(3)
            
            # --- Step 4: Filtering --- #
            if process_config.get('filtering', True):
                progress_dialog.setLabelText("Step 4/10: Filtering...")
                QApplication.processEvents()
                Pose2Sim.filtering(trial_config_dict)
            progress_dialog.setValue(4)
            
            # --- Step 5: Marker Augmentation --- #
            if process_config.get('marker_augmentation', True):
                progress_dialog.setLabelText("Step 5/10: Marker Augmentation...")
                QApplication.processEvents()
                Pose2Sim.markerAugmentation(trial_config_dict)
            progress_dialog.setValue(5)
            
            # --- Step 6: Kinematics --- #
            if process_config.get('kinematics', True):
                progress_dialog.setLabelText("Step 6/10: Kinematics...")
                QApplication.processEvents()
                Pose2Sim.kinematics(trial_config_dict)
                progress_dialog.setValue(6)
            
            # --- Step 7: Gait Classification --- #
            progress_dialog.setLabelText("Step 7/10: Gait Classification...")
            QApplication.processEvents()
            gait_classification(self.directory_manager.trial_path)
            progress_dialog.setValue(7)
            
            # --- Step 8: Convert .mot to CSV --- #
            progress_dialog.setLabelText("Step 8/10: Converting .mot to CSV...")
            QApplication.processEvents()

            # Define the kinematics directory dynamically
            kinematics_dir = os.path.join(self.directory_manager.trial_path, "kinematics")

            # Dynamically find the .mot and .osim files in the kinematics directory
            mot_files = glob.glob(os.path.join(kinematics_dir, "*.mot"))
            osim_files = glob.glob(os.path.join(kinematics_dir, "*.osim"))

            if not mot_files or not osim_files:
                raise ValueError("Could not find a .mot or .osim file in the kinematics directory.")

            mot_path = mot_files[0]
            osim_path = osim_files[0]

            # Define the output CSV file in the kinematics folder
            csv_path = os.path.join(kinematics_dir, "motion.csv")

            # Call the conversion function (ensure bodykin_from_mot_osim is in your PYTHONPATH)
            bodykin_from_mot_osim.bodykin_from_mot_osim_func(mot_path, osim_path, csv_path)
            progress_dialog.setValue(8)

            # --- Step 9: Generate FBX file using Blender ---
            if os.name == 'nt':
                progress_dialog.setLabelText("Step 9/10: Generating FBX file using Blender...")
                QApplication.processEvents()

                pose_3d_dir  =  os.path.join(self.directory_manager.trial_path, "pose-3d")
                all_files = glob.glob(os.path.join(pose_3d_dir, "*"))
                print("All files in pose_3d directory:", all_files)
                print(f"pose_3d_dirpath detected: {pose_3d_dir}")
                trc_file_path  = glob.glob(os.path.join(pose_3d_dir, "*_LSTM.trc"))
                print(f"Trc file path detected: {trc_file_path}")
                trc_file = trc_file_path[0]
                # osim_file and csv_file were defined in Step 8
                csv_file  = os.path.join(kinematics_dir, "motion.csv")
                fbx_output = os.path.join(kinematics_dir, "exported_pose2sim.fbx")


                
                # Paths to the Blender executable and the Blender script
                blender_path_ini = os.path.join(self.directory_manager.session_path, "blender_path.ini")
                config = configparser.ConfigParser()
                config.read(blender_path_ini)
                blender_exe = config.get('Paths', 'blender')
                base_dir = os.path.dirname(os.path.abspath(__file__))

                blender_script =  os.path.join(base_dir, "blender_viz_orig", "blender_script_fbx.py")

                
                # Build the command.
                # Note the '--' marker: everything after it is passed as arguments to your Python script inside Blender.
                cmd = [
                    blender_exe,
                    "--background",
                    "--python", blender_script,
                    "--",  # everything after this marker is passed to blender_script_fbx.py
                    "--base", pose_3d_dir,
                    "--trc", trc_file,
                    "--osim", osim_path,
                    "--csv", csv_file,
                    "--fbx", fbx_output,
                    "--fps", '30'
                ]

                result = subprocess.run(cmd, capture_output=True, text=True)
                print("Blender output:", result.stdout)
                print("Blender errors:", result.stderr)

                progress_dialog.setValue(9)

                fbx_output = os.path.join(kinematics_dir, "exported_pose2sim.fbx")
                if os.path.exists(fbx_output):
                    print(f"Found processed FBX file: {fbx_output}")
                    # Set the FBX file path in the viewer
                    if hasattr(self, 'viewer_manager') and self.viewer_manager:
                        self.viewer_manager.set_fbx_path(fbx_output)
                        
                        # If we're on the analytics page, update the viewer
                        if self.ui.stackedWidget.currentIndex() == 2:  # 2=Analytics page
                            # Use a small delay to ensure the viewer has time to load the new FBX
                            QTimer.singleShot(500, lambda: self.viewer_manager.sync_with_slider(
                                self.ui.slider.value(), self.ui.slider.maximum()))
            else:
                pass

            # --- Step 10: Calculate ST Parameters --- #
            progress_dialog.setLabelText("Step 10/10: Calculating ST Parameters")
            QApplication.processEvents()
            pose_3d_dir  =  os.path.join(self.directory_manager.trial_path, "pose-3d")
            trc_file_path  = glob.glob(os.path.join(pose_3d_dir, "*_LSTM.trc"))
            trc_file = trc_file_path[0]
            Calc_ST_params.analyze_gait(self.directory_manager.trial_path, trc_file)
            if hasattr(self, 'params_manager'):
                self.params_manager.refresh_dialog()
            progress_dialog.setValue(10)

            # Update the process status in the configuration dialog if it's open
            if hasattr(self, 'process_manager'):
                self.process_manager.update_process_status()

            self.motion_data_file = self.directory_manager.find_motion_csv_file()

            # Update the display if we found a data file
            if self.motion_data_file:
                # Enable analytics and comparative buttons since a motion file now exists
                self.ui.analyticsButton.setEnabled(True)
                self.ui.jointAnalyticsButton.setEnabled(True)
                self.on_display_data()
                
                QMessageBox.information(
                    self,
                    "Processing Complete",
                    "The trial has been successfully processed."
                )
            else:
                QMessageBox.warning(
                    self,
                    "Processing Warning",
                    "Processing completed, but no motion data file was found. Check logs for issues."
                )
            

        except Exception as e:
            # Close the progress dialog if it's open
            if 'progress_dialog' in locals():
                progress_dialog.close()
                
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self,
                "Processing Error",
                f"An error occurred during processing:\n\n{str(e)}"
            )
        finally:
            # Ensure progress dialog is closed
            if 'progress_dialog' in locals():
                progress_dialog.close()
    def on_process_configuration(self):
        """Open the process configuration dialog"""
        if hasattr(self, 'process_manager'):
            # Get the current OpenPose configuration from directory manager
            openpose_config = self.directory_manager.get_openpose_config_dict()
            
            # Open the configuration dialog with the current configuration
            self.process_manager.open_configuration_dialog(openpose_config)
        else:
            print("Error: process_manager not initialized")

    # --- Visualization Function --- #
    def init_viewer(self):
        """Initialize the 3D viewer"""
        try:
            print("Initializing 3D viewer...")
            # Pass self to ViewerManager to enable callbacks
            self.viewer_manager = ViewerManager(self.ui.visualizationWidget)

            QTimer.singleShot(5000, self.viewer_manager.force_hide_loading_screen)
            # Set initial states for the toggle buttons once the viewer is loaded
            QTimer.singleShot(2000, self.initialize_viewer_settings)
        except Exception as e:
            print(f"Error initializing viewer: {str(e)}")
    def initialize_viewer_settings(self):
        """Initialize viewer settings after it's fully loaded"""
        if hasattr(self, 'viewer_manager') and self.viewer_manager:
            # Set initial center animation state
            self.viewer_manager.set_center_animation(self.ui.centerAnimationButton.isChecked())
            
            # Set initial axis visibility state
            self.viewer_manager.set_axis_visible(self.ui.axisButton.isChecked())

    @pyqtSlot(float)
    def update_slider_from_web(self, time):
        """
        Updates the PyQt slider when the web viewer timeline changes
        
        Args:
            time (float): The current time in the web animation
        """
        try:
            # Only process if we're on the analytics page
            if self.ui.stackedWidget.currentIndex() == 2:
                # Check if we have animation data
                if hasattr(self, 'motion_data') and self.motion_data and 'time' in self.motion_data:
                    time_data = self.motion_data['time']
                    
                    # Find the closest time index
                    closest_idx = 0
                    min_diff = float('inf')
                    
                    for i, t in enumerate(time_data):
                        diff = abs(t - time)
                        if diff < min_diff:
                            min_diff = diff
                            closest_idx = i
                      
                    # Only update if the index has changed
                    if closest_idx != self.current_highlighted_row:
                        # Temporarily block signals to avoid feedback loop
                        self.ui.slider.blockSignals(True)
                        self.ui.slider.setValue(closest_idx)
                        self.ui.slider.blockSignals(False)
                        
                        # Update the highlighted row and vertical line
                        self.current_highlighted_row = closest_idx
                        self.table_manager.highlight_row(self.ui.jointsTable, closest_idx)
                        self.chart_manager.update_vertical_line(closest_idx)
                        self.update_gait_stage_value(closest_idx)
        except Exception as e:
            print(f"Error updating slider from web: {str(e)}")

    # --- Playback Functions --- #
    def on_slider_value_changed(self, value):
        """
        Handles when the slider value changes by highlighting the corresponding row in the table,
        updating the vertical line on the chart, and updating the gait stage value.

        Args:
            value (int): The current slider value, corresponding directly to the row index
        """
        # Since slider maximum is now (num_frames - 1), we can use the value directly
        self.current_highlighted_row = value

        # Update the table highlight
        self.table_manager.highlight_row(self.ui.jointsTable, value)

        # Update the vertical line position on the chart
        self.chart_manager.update_vertical_line(value)

        # Update the gait stage value if data is available
        self.update_gait_stage_value(value)

        # Sync the 3D viewer with the slider
        if hasattr(self, 'viewer_manager') and self.viewer_manager:
            max_value = self.ui.slider.maximum()
            self.viewer_manager.sync_with_slider(value, max_value)
    def setup_player_controls(self):
        """Set up connections for play/pause buttons"""
        # Connect play and pause buttons
        self.ui.playButton.clicked.connect(self.on_play_button_clicked)
        self.ui.pauseButton.clicked.connect(self.on_pause_button_clicked)
        
        # Connect skip/back buttons
        self.ui.skipButton.clicked.connect(self.on_skip_button_clicked)
        self.ui.backButton.clicked.connect(self.on_back_button_clicked)
        
        # Connect speed buttons
        self.ui.fastForwardButton.clicked.connect(self.on_speed_up_button_clicked)
        self.ui.rewindButton.clicked.connect(self.on_speed_down_button_clicked)
        
        # Connect center animation and axis toggle buttons
        self.ui.centerAnimationButton.clicked.connect(self.on_center_animation_toggled)
        self.ui.axisButton.clicked.connect(self.on_axis_toggled)
        
        # Initialize playback state
        self.is_playing = False
        
        # Display initial speed value
        self.update_speed_label(1.0)  # Default 1x speed

    def on_play_button_clicked(self):
        """Handle play button click"""
        if hasattr(self, 'viewer_manager') and self.viewer_manager:
            # Toggle play/pause in the viewer.js
            self.viewer_manager.play_pause()
            
            # Query the current state to update UI accordingly
            self.viewer_manager.get_animation_state(self.update_ui_from_animation_state)

    def on_pause_button_clicked(self):
        """Handle pause button click"""
        if hasattr(self, 'viewer_manager') and self.viewer_manager:
            # This does the same as play - it toggles the state
            self.viewer_manager.play_pause()
            
            # Query the current state to update UI accordingly
            self.viewer_manager.get_animation_state(self.update_ui_from_animation_state)

    def update_ui_from_animation_state(self, state):
        """Update UI based on the animation state received from JavaScript"""
        if state:
            # Update playing state
            self.is_playing = state.get('isPlaying', False)
            
            # Update speed label if needed
            speed = state.get('speed', 1.0)
            self.update_speed_label(speed)

    def update_playback_frame(self):
        """Update the current frame during playback"""
        if not self.is_playing:
            return
            
        current_value = self.ui.slider.value()
        max_value = self.ui.slider.maximum()
        
        # Move to next frame, loop back to beginning if at the end
        next_value = current_value + 1
        if next_value > max_value:
            next_value = 0
        
        # Update the slider value, which will trigger all necessary updates
        self.ui.slider.setValue(next_value)
    def on_back_button_clicked(self):
        """Move to the previous frame when the back button is clicked"""
        if hasattr(self, 'viewer_manager') and self.viewer_manager:
            # Trigger the rewind button in viewer.js
            self.viewer_manager.rewind()

    def on_skip_button_clicked(self):
        """Move to the next frame when the skip button is clicked"""
        if hasattr(self, 'viewer_manager') and self.viewer_manager:
            # Trigger the forward button in viewer.js
            self.viewer_manager.forward()
        
    def on_speed_up_button_clicked(self):
        """Increase the playback speed when the speed up button is clicked"""
        # Define speed increments - common multipliers for playback
        speed_options = [0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0]
        
        # Get current speed from UI
        current_text = self.ui.speedLabel.text().rstrip('x')
        try:
            current_speed = float(current_text)
        except ValueError:
            current_speed = 1.0  # Default if parsing fails
        
        # Find the next higher speed option
        next_speed = 1.0  # Default if not found
        for speed in speed_options:
            if speed > current_speed:
                next_speed = speed
                break
        if current_speed >= speed_options[-1]:
            next_speed = speed_options[-1]  # Cap at maximum
        
        # Update the viewer speed
        if hasattr(self, 'viewer_manager') and self.viewer_manager:
            self.viewer_manager.set_speed(next_speed)
        
        # Update the speed label
        self.update_speed_label(next_speed)

    def on_speed_down_button_clicked(self):
        """Decrease the playback speed when the speed down button is clicked"""
        # Define speed increments - common multipliers for playback
        speed_options = [0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0]
        
        # Get current speed from UI
        current_text = self.ui.speedLabel.text().rstrip('x')
        try:
            current_speed = float(current_text)
        except ValueError:
            current_speed = 1.0  # Default if parsing fails
        
        # Find the next lower speed option
        next_speed = 0.25  # Default if not found
        for speed in reversed(speed_options):
            if speed < current_speed:
                next_speed = speed
                break
        if current_speed <= speed_options[0]:
            next_speed = speed_options[0]  # Cap at minimum
        
        # Update the viewer speed
        if hasattr(self, 'viewer_manager') and self.viewer_manager:
            self.viewer_manager.set_speed(next_speed)
        
        # Update the speed label
        self.update_speed_label(next_speed)
        
    def on_center_animation_toggled(self):
        """Handle the center animation button toggle"""
        # Get the checked state of the button
        is_center_enabled = self.ui.centerAnimationButton.isChecked()
        
        # Update the 3D viewer if available
        if hasattr(self, 'viewer_manager') and self.viewer_manager:
            self.viewer_manager.set_center_animation(is_center_enabled)

    def on_axis_toggled(self):
        """Handle the axis visibility button toggle"""
        # Get the checked state of the button
        is_axis_visible = self.ui.axisButton.isChecked()
        
        # Update the 3D viewer if available
        if hasattr(self, 'viewer_manager') and self.viewer_manager:
            self.viewer_manager.set_axis_visible(is_axis_visible)

    def update_speed_label(self, speed_multiplier):
        """Update the speed label with the current playback speed multiplier"""
        # Format the speed as a string with the 'x' suffix
        speed_text = f"{speed_multiplier:.2f}x"
        
        # Remove trailing zeros for cleaner display
        if speed_text.endswith('0x'):
            speed_text = speed_text[:-2] + 'x'
        if speed_text.endswith('.0x'):
            speed_text = speed_text[:-3] + 'x'
            
        # Update the speedLabel text
        self.ui.speedLabel.setText(speed_text)
    def setup_player_controls(self):
        """Set up connections for play/pause buttons"""
        # Connect play and pause buttons
        self.ui.playButton.clicked.connect(self.on_play_button_clicked)
        self.ui.pauseButton.clicked.connect(self.on_pause_button_clicked)
        
        # Initialize playback state
        self.is_playing = False
        self.playback_timer = QTimer()
        self.playback_timer.timeout.connect(self.update_playback_frame)
        self.playback_speed = 30  # Default to 30 fps
        
        # Initialize the speed label with the default speed (1x)
        self.update_speed_label(1.0)
    
    def closeEvent(self, event):
        """Handle application closing"""
        self.process_manager.cleanup()
        
        # Also cleanup camera resources if they're still running
        self.camera_manager.close_all_cameras()
        
        # Clean up viewer resources if needed
        if hasattr(self, 'viewer_manager') and self.viewer_manager:
            # Stop any server threads
            if hasattr(self.viewer_manager, 'server_thread') and self.viewer_manager.server_thread:
                # We can't really stop a thread directly, but we can let it die when the app closes
                print("Viewer server thread will terminate with application")
        
        # Clean up params manager resources
        if hasattr(self, 'params_manager'):
            self.params_manager.cleanup()
        
        # Clean up stats manager resources
        if hasattr(self, 'stats_manager'):
            self.stats_manager.cleanup()
        
        super().closeEvent(event)
    
if __name__ == "__main__":
  app = QApplication(sys.argv)

  window = MainWindow()
  window.show()

  sys.exit(app.exec()) 