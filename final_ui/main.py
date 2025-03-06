import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Pose2Sim import Pose2Sim
import toml

import os
import pathlib

from final import Ui_MainWindow

from camera_manager import Camera, CameraManager
from directory_manager import DirectoryManager
from table_manager import TableManager
from data_manager import DataManager
from process_manager import ProcessManager
from chart_manager import ChartManager
from viewer_manager import ViewerManager

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.stackedWidget.setCurrentIndex(1)
        self.current_highlighted_row = 0
        self.current_comparative_row = 0
        
        self.directory_manager = DirectoryManager(self)
        self.table_manager = TableManager(self)
        self.data_manager = DataManager()
        self.camera_manager = CameraManager(self)
        self.process_manager = ProcessManager(self)
        self.chart_manager = ChartManager(self)

        self.motion_data_file = "/Users/mattheworga/Documents/Git/DLSU/thesis/scripts/data_2/P03/results/original/P03_normal_classification_1.csv"
        self.versus_data_file = "/Users/mattheworga/Documents/Git/DLSU/thesis/scripts/data_2/P03/results/original/P03_trendelenburg_classification_1.csv"
        
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
        self.ui.stackedWidget.setCurrentIndex(2)
    def on_jointAnalyticsButton_clicked(self):
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

        # Setup comparative page connections
        self.setup_comparative_page()
        self.ui.stackedWidget.currentChanged.connect(self.on_tab_changed)

        self.ui.skipButton.clicked.connect(self.on_skip_button_clicked)
        self.ui.backButton.clicked.connect(self.on_back_button_clicked)
        self.ui.fastForwardButton.clicked.connect(self.on_speed_up_button_clicked)
        self.ui.rewindButton.clicked.connect(self.on_speed_down_button_clicked)
        self.ui.centerAnimationButton.clicked.connect(self.on_center_animation_toggled)
        self.ui.axisButton.clicked.connect(self.on_axis_toggled)

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
    def on_select_participant(self):
        self.directory_manager.set_participant()
        participant_name = self.directory_manager.participant_dir
        
        if participant_name: 
            self.ui.participantSelectedLabel.setText(participant_name)
            self.ui.trialSelectButton.setEnabled(True)
            self.ui.trialAddButton.setEnabled(True)
            self.ui.processButton.setEnabled(True)
    def on_select_trial(self):
      self.directory_manager.set_trial()
      trial_name = self.directory_manager.trial_dir

      self.ui.directoryValue.setText(self.directory_manager.trial_dir)

      self.camera_manager.save_directory = self.directory_manager.trial_path
      self.camera_manager.file_name = self.directory_manager.trial_name

      if trial_name:
        self.ui.trialSelectedLabel.setText(trial_name)
        self.ui.processButton.setEnabled(True)
        
    def add_participant(self):
        self.directory_manager.add_participant()
    def add_trial(self):
        self.directory_manager.add_trial()

    # --- Cameras Page Functions --- #
    def on_detect_cameras(self):
        self.camera_manager.detect_available_cameras()
    
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
                    
                    if motion_data:
                        self.table_manager.display_data_in_table(self.ui.jointsTable, motion_data, True, "all")
                        self.chart_manager.display_data_in_chart(self.ui.trialChart, motion_data, False, "all")

                        num_rows = len(motion_data['time'])
                        self.ui.slider.setMinimum(0)
                        self.ui.slider.setMaximum(num_rows - 1)
                        self.ui.slider.setValue(0)
                            
                        # Initialize highlighting for the first row
                        self.table_manager.highlight_row(self.ui.jointsTable, 0)
                        
                        # Initialize the gait stage value
                        self.update_gait_stage_value(0)
                    else:
                        # QMessageBox.warning(
                        #     self,
                        #     "Data Loading Error",
                        #     "Failed to load motion data file."
                        # )
                        pass
            else:
                QMessageBox.information(
                    self,
                    "No Data File",
                    "No motion data file found in trial directory."
                )
            
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
            if self.motion_data_file:
                self.base_motion_data = self.data_manager.read_csv_file(self.motion_data_file)
                
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
                    if hasattr(self.ui, 'baseTrialValue'):
                        trial_name = self.directory_manager.trial_name
                        if trial_name:
                            self.ui.baseTrialValue.setText(trial_name)
            
            # Load versus trial data
            if self.versus_data_file:
                # Check file extension to determine how to read it
                if self.versus_data_file.endswith('.mot'):
                    self.versus_motion_data = self.data_manager.read_mot_file(self.versus_data_file)
                else:
                    self.versus_motion_data = self.data_manager.read_csv_file(self.versus_data_file)
                
                if self.versus_motion_data:
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
            
            # Set up the slider for the comparative page
            max_rows = 0
            if hasattr(self, 'base_motion_data') and 'time' in self.base_motion_data:
                max_rows = max(max_rows, len(self.base_motion_data['time']))
                
            if hasattr(self, 'versus_motion_data') and 'time' in self.versus_motion_data:
                max_rows = max(max_rows, len(self.versus_motion_data['time']))
                
            if max_rows > 0:
                self.ui.comparativeSlider.setMinimum(0)
                self.ui.comparativeSlider.setMaximum(max_rows - 1)
                self.ui.comparativeSlider.setValue(0)
                
                # Initialize highlighting for the first row in both tables
                self.table_manager.highlight_row(self.ui.baseTrialTable, 0)
                self.table_manager.highlight_row(self.ui.versusTrialTable, 0)
                
                # Initialize the gait stage values
                self.update_comparative_gait_stage_values(0)
        
        except Exception as e:
            print(f"Error loading comparative data: {str(e)}")
            QMessageBox.warning(
                self,
                "Data Loading Error",
                f"Failed to load comparative data: {str(e)}"
            )
    def on_comparative_joint_filter_changed(self, joint_filter):
        """
        Handle joint filter button clicks on the comparative page
        
        Args:
            joint_filter (str): Type of filter ("all", "hip", "knee", "ankle")
        """
        try:
            # Update base trial display
            if hasattr(self, 'base_trial_data') and self.base_trial_data:
                self.table_manager.display_data_in_table(
                    self.ui.baseTrialTable, 
                    self.base_trial_data, 
                    True,  # scrollable
                    joint_filter
                )
                self.chart_manager.display_data_in_chart(
                    self.ui.baseTrialChart, 
                    self.base_trial_data, 
                    False,  # not scrollable
                    joint_filter
                )
                
            # Update versus trial display
            if hasattr(self, 'versus_trial_data') and self.versus_trial_data:
                self.table_manager.display_data_in_table(
                    self.ui.versusTrialTable, 
                    self.versus_trial_data, 
                    True,  # scrollable
                    joint_filter
                )
                self.chart_manager.display_data_in_chart(
                    self.ui.versusTrialChart, 
                    self.versus_trial_data, 
                    False,  # not scrollable
                    joint_filter
                )
                
        except Exception as e:
            print(f"Error updating comparative filter: {str(e)}")
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
  

    # --- Table & Charts Functions --- # 
    def on_tab_changed(self, index):
        """
        Handle tab changes and reapply highlighting when needed
        
        Args:
            index (int): The index of the newly selected tab
        """
        # Check if we're switching to the analytics/simulation page (tab index 2)
        if index == 2:  # Analytics tab
            # Make sure the slider value matches the current highlighted row
            self.ui.slider.setValue(self.current_highlighted_row)
            
            # Use a short timer to ensure UI is fully updated before highlighting
            self.reapply_table_highlighting()
            self.reapply_chart_vertical_line()
            
            # Update the gait stage value
            self.update_gait_stage_value(self.current_highlighted_row)
        
        # Check if we're switching to the comparative page (tab index 3)
        elif index == 3:  # Comparative tab
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
        session_config_path = os.path.join(self.directory_manager.session_path, "Config.toml")
        session_config_dict = toml.load(session_config_path)
        session_config_dict.get("project").update({"project_dir":os.path.join(self.directory_manager.session_path)})

        trial_config_path = os.path.join(self.directory_manager.trial_path, "Config.toml")
        trial_config_dict = toml.load(trial_config_path)
        trial_config_dict.get("project").update({"project_dir":self.directory_manager.trial_path})

        # self.process_manager.start_processing(session_config_dict, trial_config_dict)

        # Pose2Sim.calibration(session_config_dict) # Working
        # print("WORKING: Calibration")

        Pose2Sim.poseEstimation(trial_config_dict)
        Pose2Sim.synchronization(trial_config_dict)
        Pose2Sim.triangulation(trial_config_dict)
        Pose2Sim.filtering(trial_config_dict)
        Pose2Sim.kinematics(trial_config_dict)

    # --- Visualization Function --- #
    def init_viewer(self):
        """Initialize the 3D viewer"""
        try:
            print("Initializing 3D viewer...")
            # Pass self to ViewerManager to enable callbacks
            self.viewer_manager = ViewerManager(self.ui.visualizationWidget)
            
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
        
        # Initialize playback state
        self.is_playing = False
        self.playback_timer = QTimer()
        self.playback_timer.timeout.connect(self.update_playback_frame)
        self.playback_speed = 30  # Default to 30 fps
    def on_play_button_clicked(self):
        """Handle play button click"""
        if not self.is_playing:
            self.is_playing = True
            
            # Start the timer for animation
            self.playback_timer.start(1000 // self.playback_speed)  # milliseconds per frame
            
            # Update the 3D viewer's play state if available
            if hasattr(self, 'viewer_manager') and self.viewer_manager:
                self.viewer_manager.set_playing(True)
    def on_pause_button_clicked(self):
        """Handle pause button click"""
        if self.is_playing:
            self.is_playing = False
            
            # Stop the timer
            self.playback_timer.stop()
            
            # Update the 3D viewer's play state if available
            if hasattr(self, 'viewer_manager') and self.viewer_manager:
                self.viewer_manager.set_playing(False)
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
        if hasattr(self, 'motion_data') and self.motion_data:
            current_value = self.ui.slider.value()
            # Move to previous frame (minimum 0)
            prev_value = max(0, current_value - 1)
            
            # Only update if we actually changed frames
            if prev_value != current_value:
                # Update the slider value, which will trigger all necessary updates
                self.ui.slider.setValue(prev_value)
    def on_skip_button_clicked(self):
        """Move to the next frame when the skip button is clicked"""
        if hasattr(self, 'motion_data') and self.motion_data:
            current_value = self.ui.slider.value()
            max_value = self.ui.slider.maximum()
            # Move to next frame (maximum is slider max)
            next_value = min(max_value, current_value + 1)
            
            # Only update if we actually changed frames
            if next_value != current_value:
                # Update the slider value, which will trigger all necessary updates
                self.ui.slider.setValue(next_value)
    def on_speed_up_button_clicked(self):
        """Increase the playback speed when the speed up button is clicked"""
        # Define speed increments - common multipliers for playback
        speed_options = [0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0]
        
        # Find the next higher speed option
        current_index = -1
        for i, speed in enumerate(speed_options):
            if abs(self.playback_speed / 30 - speed) < 0.1:  # Using a small epsilon for float comparison
                current_index = i
                break
        
        # If current speed wasn't found or is already at max, use the highest speed
        if current_index == -1 or current_index >= len(speed_options) - 1:
            new_speed = speed_options[-1]
        else:
            new_speed = speed_options[current_index + 1]
        
        # Update playback speed (convert from multiplier to frames per second)
        self.playback_speed = int(new_speed * 30)
        
        # Update timer interval if currently playing
        if self.is_playing:
            self.playback_timer.setInterval(1000 // self.playback_speed)
        
        # Update the speed label
        self.update_speed_label(new_speed)
        
        # Display current speed as feedback (optional)
        print(f"Playback speed: {new_speed}x")
        
        # Update the 3D viewer's speed if available
        if hasattr(self, 'viewer_manager') and self.viewer_manager:
            self.viewer_manager.set_speed(new_speed)
    def on_speed_down_button_clicked(self):
        """Decrease the playback speed when the speed down button is clicked"""
        # Define speed increments - common multipliers for playback
        speed_options = [0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0]
        
        # Find the next lower speed option
        current_index = -1
        for i, speed in enumerate(speed_options):
            if abs(self.playback_speed / 30 - speed) < 0.1:  # Using a small epsilon for float comparison
                current_index = i
                break
        
        # If current speed wasn't found or is already at min, use the lowest speed
        if current_index == -1 or current_index <= 0:
            new_speed = speed_options[0]
        else:
            new_speed = speed_options[current_index - 1]
        
        # Update playback speed (convert from multiplier to frames per second)
        self.playback_speed = int(new_speed * 30)
        
        # Update timer interval if currently playing
        if self.is_playing:
            self.playback_timer.setInterval(1000 // self.playback_speed)
        
        # Update the speed label
        self.update_speed_label(new_speed)
        
        # Display current speed as feedback (optional)
        print(f"Playback speed: {new_speed}x")
        
        # Update the 3D viewer's speed if available
        if hasattr(self, 'viewer_manager') and self.viewer_manager:
            self.viewer_manager.set_speed(new_speed)
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
        
        super().closeEvent(event)
    
if __name__ == "__main__":
  app = QApplication(sys.argv)

  window = MainWindow()
  window.show()

  sys.exit(app.exec()) 