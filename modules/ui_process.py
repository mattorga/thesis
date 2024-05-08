import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QComboBox, QHBoxLayout,
                             QRadioButton, QLabel, QLineEdit, QGroupBox, QScrollArea, QFrame, QCheckBox, QDoubleSpinBox,
                              QLabel, QButtonGroup, QStackedWidget,QTableWidget,QSpinBox) 
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSlot
class ConverterCalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Main layout, note that order of arguments matters here
        self.layout = QVBoxLayout()

        # Dropdown for selecting mode with a default "Select" option
        self.mode_select = QComboBox()
        self.mode_select.addItems(["Select", "Convert", "Calculate"])
        self.mode_select.currentIndexChanged.connect(self.updateUI)
        self.layout.addWidget(self.mode_select, 0)

        # Set initial window size
        self.setGeometry(300, 300, 800, 600)  # You can adjust the size as needed

        # Initialize the conversion layout
        self.convert_layout = QVBoxLayout()
        self.createConvertOptions()  # Correctly include this method
        self.convert_layout_widget = QWidget()  # Wrap convert_layout in a QWidget for easy show/hide
        self.convert_layout_widget.setLayout(self.convert_layout)
        self.layout.addWidget(self.convert_layout_widget, 1)

        # Initialize the scroll area for calculation which will contain a window
        self.calculation_scroll_area = QScrollArea()
        self.calculation_window = QWidget()
        self.calculation_window_layout = QVBoxLayout()
        self.calculation_window.setLayout(self.calculation_window_layout)
        self.calculation_scroll_area.setWidget(self.calculation_window)
        self.calculation_scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.calculation_scroll_area, 2)
        self.createCalculationOptions()
        
        


        self.extrinsics_method_group = QButtonGroup(self)
        self.extrinsics_method_group.setExclusive(False)
        self.extrinsics_method_group.buttonClicked[int].connect(self.handleRadioButtonClicked)
    

        # Initially hide the conversion layout and scroll area
        self.convert_layout_widget.hide()
        self.calculation_scroll_area.hide()
        
        # Set main layout
        self.setLayout(self.layout)
        self.setWindowTitle('Convert or Calculate')
        self.show()

        self.method_dropdown = QComboBox()
        self.model_dropdown = QComboBox()
        
        self.initializeMethodDropdown()
        self.createSynchronizationUI()
        self.createTriangulationUI()
        self.createFilteringUI()
        self.createButterworthLayout()
        self.createKalmanLayout()
        self.createGaussianLayout()
        self.createLoessLayout()
        self.createMedianLayout()

        
#-------------------------CONVERT--------------------------
    def createConvertOptions(self):
        # Group box for conversion settings
        self.convert_group = QGroupBox("Convert From:")
        self.radio_button_layout = QHBoxLayout()

        # Radio buttons for each system
        systems = ['Qualisys', 'Optitrack', 'Vicon', 'Opencap', 'Easymocap', 'Biocv']
        self.radio_buttons = {system: QRadioButton(system) for system in systems}
        for radio_button in self.radio_buttons.values():
            self.radio_button_layout.addWidget(radio_button)

        # Set the radio buttons layout
        self.convert_group.setLayout(self.radio_button_layout)
        self.convert_layout.addWidget(self.convert_group)

        # Binning factor input smaller and to the right
        self.binning_factor_layout = QHBoxLayout()
        self.binning_factor_label = QLabel("Binning Factor:")
        self.binning_factor_input = QLineEdit()
        self.binning_factor_input.setMaximumWidth(100)  # Adjust the width as needed

        # Add widgets to the binning factor layout
        self.binning_factor_layout.addWidget(self.binning_factor_label)
        self.binning_factor_layout.addStretch()
        self.binning_factor_layout.addWidget(self.binning_factor_input)

        # Add the binning factor layout to the conversion layout
        self.convert_layout.addLayout(self.binning_factor_layout)
#------------------------------CALCULATE-------------------------------------
    def createCalculationOptions(self):
        # ----------------------------------------------------------------HEADER-------------------
        self.calculation_header = QLabel("Calculate Intrinsics")
        header_font = QFont("Arial", 12)  # You can modify the font family and size as needed
        self.calculation_header.setFont(header_font)
        self.calculation_window_layout.addWidget(self.calculation_header)

        # Toggle for overwrite_intrinsics
        self.overwrite_intrinsics_toggle = QCheckBox("Overwrite Intrinsics")
        self.calculation_window_layout.addWidget(self.overwrite_intrinsics_toggle)

        # Toggle for show_detection_intrinsics
        self.show_detection_intrinsics_toggle = QCheckBox("Show Detection Intrinsics")
        self.calculation_window_layout.addWidget(self.show_detection_intrinsics_toggle)

        # Dropdown for intrinsics_extension
        self.intrinsics_extension_layout = QHBoxLayout()
        self.intrinsics_extension_dropdown = QComboBox()
        file_extensions = ['.mp4', '.avi', '.mov', '.jpg', '.png', '.bmp']
        self.intrinsics_extension_dropdown.addItems(file_extensions)
        self.intrinsics_extension_layout.addWidget(QLabel("Intrinsics Extension:"))
        self.intrinsics_extension_layout.addWidget(self.intrinsics_extension_dropdown)
        self.intrinsics_extension_layout.addStretch()
        self.calculation_window_layout.addLayout(self.intrinsics_extension_layout)

        # Input for extract_every_N_sec
        self.extract_every_N_sec_layout = QHBoxLayout()
        self.extract_every_N_sec_input = QDoubleSpinBox()
        self.extract_every_N_sec_input.setMaximumWidth(100)
        self.extract_every_N_sec_layout.addWidget(QLabel("Extract Every N Seconds:"))
        self.extract_every_N_sec_layout.addWidget(self.extract_every_N_sec_input)
        self.extract_every_N_sec_layout.addStretch()
        self.calculation_window_layout.addLayout(self.extract_every_N_sec_layout)

        # Input for intrinsics_corners_nb with two input fields
        self.corners_nb_layout = QHBoxLayout()
        self.intrinsics_corners_nb_input1 = QDoubleSpinBox()
        self.intrinsics_corners_nb_input2 = QDoubleSpinBox()
        self.intrinsics_corners_nb_input1.setMaximumWidth(100)
        self.intrinsics_corners_nb_input2.setMaximumWidth(100)
        self.corners_nb_layout.addWidget(QLabel("Intrinsics Corners Nb:"))
        self.corners_nb_layout.addWidget(self.intrinsics_corners_nb_input1)
        self.corners_nb_layout.addWidget(self.intrinsics_corners_nb_input2)
        self.corners_nb_layout.addStretch()
        self.calculation_window_layout.addLayout(self.corners_nb_layout)

        # Input for intrinsics_square_size
        self.intrinsics_square_size_layout = QHBoxLayout()
        self.intrinsics_square_size_input1 = QDoubleSpinBox()
        self.intrinsics_square_size_input2 = QDoubleSpinBox()
        self.intrinsics_square_size_input1.setMaximumWidth(100)
        self.intrinsics_square_size_input2.setMaximumWidth(100)
        self.intrinsics_square_size_layout.addWidget(QLabel("Intrinsics Square Size (h,w):"))
        self.intrinsics_square_size_layout.addWidget(self.intrinsics_square_size_input1)
        self.intrinsics_square_size_layout.addWidget(self.intrinsics_square_size_input2)
        self.intrinsics_corners_nb_input2 = QDoubleSpinBox()

        self.intrinsics_square_size_layout.addStretch()
        self.calculation_window_layout.addLayout(self.intrinsics_square_size_layout)

        
#-------------------------------------------CALIBRATE EXTRINSICS------------------------------------------------
        self.calibrate_extrinsics_header = QLabel("Calibrate Extrinsics")
        self.calibrate_extrinsics_header.setFont(header_font)  # Use the same font as for 'Calculate Intrinsics'
        self.calculation_window_layout.addWidget(self.calibrate_extrinsics_header)

        # Toggle for 'Moving Cameras'
        self.moving_cameras_toggle = QCheckBox("Moving Cameras")
        self.calculation_window_layout.addWidget(self.moving_cameras_toggle)

        # Toggle for 'Calculate Extrinsics'
        self.calculate_extrinsics_toggle = QCheckBox("Calculate Extrinsics")
        self.calculation_window_layout.addWidget(self.calculate_extrinsics_toggle)

       

        # Dropdown for 'Extrinsics Method'
        self.extrinsics_method_dropdown = QComboBox()
        extrinsics_methods = ["Select", "Board", "Scene", "Keypoints"]
        self.extrinsics_method_dropdown.addItems(extrinsics_methods)
        self.calculation_window_layout.addWidget(QLabel("Extrinsics Method:"))
        self.calculation_window_layout.addWidget(self.extrinsics_method_dropdown)

        # Connect the dropdown selection change signal to a handler
        self.extrinsics_method_dropdown.currentIndexChanged.connect(self.extrinsicsMethodChanged)

        
       

        #self.calculation_window_layout.addLayout(self.extrinsics_method_layout)

#----------------------------STACKED WIDGET --------------------------------

# Create a stacked widget to hold the extra settings for different methods
        self.extra_settings_stack = QStackedWidget()

        # Create a widget for the 'Board' method settings
        self.board_settings_widget = QWidget()
        self.board_settings_layout = QVBoxLayout()

        # Toggle for 'Show Reprojection Error'
        self.show_reprojection_error_toggle = QCheckBox("Show Reprojection Error")
        self.board_settings_layout.addWidget(self.show_reprojection_error_toggle)

        # Dropdown for 'Extrinsics Extension'
        self.extrinsics_extension_dropdown = QComboBox()
        file_extensions = ['.mp4', '.avi', '.mov', '.jpg', '.png', '.bmp']
        self.extrinsics_extension_dropdown.addItems(file_extensions)
        self.board_settings_layout.addWidget(QLabel("Extrinsics Extension:"))
        self.board_settings_layout.addWidget(self.extrinsics_extension_dropdown)

        # Inputs for 'Extrinsics Corners Nb' and 'Extrinsics Square Size'
        self.extrinsics_corners_nb_layout = QHBoxLayout()
        self.extrinsics_corners_nb_input1 = QDoubleSpinBox()
        self.extrinsics_corners_nb_input2 = QDoubleSpinBox()
        self.setupDoubleSpinBox(self.extrinsics_corners_nb_input1)
        self.setupDoubleSpinBox(self.extrinsics_corners_nb_input2)
        self.extrinsics_corners_nb_layout.addWidget(QLabel("Extrinsics Corners Nb:"))
        self.extrinsics_corners_nb_layout.addWidget(self.extrinsics_corners_nb_input1)
        self.extrinsics_corners_nb_layout.addWidget(self.extrinsics_corners_nb_input2)
        self.board_settings_layout.addLayout(self.extrinsics_corners_nb_layout)

        self.extrinsics_square_size_layout = QHBoxLayout()
        self.extrinsics_square_size_input1 = QDoubleSpinBox()
        self.extrinsics_square_size_input2 = QDoubleSpinBox()
        self.setupDoubleSpinBox(self.extrinsics_square_size_input1)
        self.setupDoubleSpinBox(self.extrinsics_square_size_input2)
        self.extrinsics_square_size_layout.addWidget(QLabel("Extrinsics Square Size:"))
        self.extrinsics_square_size_layout.addWidget(self.extrinsics_square_size_input1)
        self.extrinsics_square_size_layout.addWidget(self.extrinsics_square_size_input2)
        self.board_settings_layout.addLayout(self.extrinsics_square_size_layout)
        

    
        # Set the layout for the 'Board' settings widget and add it to the stack
        self.board_settings_widget.setLayout(self.board_settings_layout)
        self.extra_settings_stack.addWidget(self.board_settings_widget)

        # Placeholder widget for other methods (Scene, Keypoints), can be expanded later
        self.extra_settings_stack.addWidget(QWidget())  # For 'Scene'
        self.extra_settings_stack.addWidget(QWidget())  # For 'Keypoints'

        self.calculation_window_layout.addWidget(self.extra_settings_stack)

    #-----------------------------------POSE FRAMEWORK----------------------------------------------------------

    # Function to initialize the method dropdown and connect its signal
    def initializeMethodDropdown(self):
         # Create labels for the dropdowns
        self.pose_framework_label = QLabel("Pose Framework:")
        self.pose_model_label = QLabel("Pose Model:")

        # Initialize the method dropdown and add items
        self.method_dropdown = QComboBox()
        self.method_dropdown.addItem("Select")
        self.method_dropdown.addItems(["OpenPose", "MediaPipe", "AlphaPose", "DeepLabCut"])
        self.method_dropdown.currentIndexChanged.connect(self.methodDropdownChanged)

        # Initialize the model dropdown and add the placeholder item
        self.model_dropdown = QComboBox()
        self.model_dropdown.addItem("Select")

        # Create the overwrite pose toggle
        self.overwrite_pose = QCheckBox("Overwrite Pose")

        # Add the labels and dropdowns to the layout
        self.calculation_window_layout.addWidget(self.pose_framework_label)
        self.calculation_window_layout.addWidget(self.method_dropdown)
        self.calculation_window_layout.addWidget(self.pose_model_label)
        self.calculation_window_layout.addWidget(self.model_dropdown)
        # Add the overwrite pose toggle to the layout
        self.calculation_window_layout.addWidget(self.overwrite_pose)
        self.method_dropdown.currentIndexChanged.connect(self.poseOptionsChanged)
        self.model_dropdown.currentIndexChanged.connect(self.poseOptionsChanged)

    # Handler for method dropdown changes to update the model dropdown
    def methodDropdownChanged(self, index):
        # Clear and populate the model dropdown based on the selected method
        self.model_dropdown.clear()
        self.model_dropdown.addItem("Select")  # Placeholder option
        method = self.method_dropdown.currentText()

        if method == "OpenPose":
            self.model_dropdown.addItems(["BODY_25B", "BODY_25", "BODY_135", "COCO", "MPII"])
        elif method == "MediaPipe":
            self.model_dropdown.addItems(["BlazePose"])
        elif method == "AlphaPose":
            self.model_dropdown.addItems(["HALPE_26", "HALPE_68", "HALPE_136", "COCO_133"])
        elif method == "DeepLabCut":
            self.model_dropdown.addItems(["CUSTOM"])


    #-----------------------------------SYNCHRONIZATION, FIX INPUT FIELD SIZES----------------------------------------------------------------


    def createSynchronizationUI(self):
    # Header for synchronization
        self.synchronization_header = QLabel("Synchronization")
        self.synchronization_header.setFont(QFont("Arial", 12))
        self.frames_input1 = QDoubleSpinBox()
        self.frames_input2 = QDoubleSpinBox()
        self.cut_off_frequency_input = QDoubleSpinBox()
        self.setupSpinBox(self.frames_input1)
        self.setupSpinBox(self.frames_input2)
        self.setupSpinBox(self.cut_off_frequency_input)

        # Create the synchronization UI elements
        self.reset_sync = QCheckBox("Reset Sync")
        
        self.frames_label = QLabel("Frames:")
        #####

        self.frames_input1 = QDoubleSpinBox()
        self.frames_input2 = QDoubleSpinBox()

        self.cut_off_frequency_label = QLabel("Cut Off Frequency:")
        self.cut_off_frequency_input = QDoubleSpinBox()

        self.speed_kind_label = QLabel("Speed Kind:")
        self.speed_kind_dropdown = QComboBox()
        self.speed_kind_dropdown.addItems(["Select", "x", "y", "z", "2D"])

        self.vmax_label = QLabel("Vmax:")
        self.vmax_input = QDoubleSpinBox()

        self.cam1_nb_label = QLabel("Cam1 Nb:")
        self.cam1_nb_input = QDoubleSpinBox()

        self.cam2_nb_label = QLabel("Cam2 Nb:")
        self.cam2_nb_input = QDoubleSpinBox()

        self.id_kpt_label = QLabel("ID Kpt:")
        self.id_kpt_input1 = QDoubleSpinBox()
        self.id_kpt_input2 = QDoubleSpinBox()

        self.weights_kpt_label = QLabel("Weights Kpt:")
        self.weights_kpt_input1 = QDoubleSpinBox()
        self.weights_kpt_input2 = QDoubleSpinBox()

        # Add the synchronization UI elements to the layout
        self.calculation_window_layout.addWidget(self.synchronization_header)
        self.calculation_window_layout.addWidget(self.reset_sync)
        self.calculation_window_layout.addWidget(self.frames_label)
        self.calculation_window_layout.addWidget(self.frames_input1)
        self.calculation_window_layout.addWidget(self.frames_input2)
        self.calculation_window_layout.addWidget(self.cut_off_frequency_label)
        self.calculation_window_layout.addWidget(self.cut_off_frequency_input)
        self.calculation_window_layout.addWidget(self.speed_kind_label)
        self.calculation_window_layout.addWidget(self.speed_kind_dropdown)
        self.calculation_window_layout.addWidget(self.vmax_label)
        self.calculation_window_layout.addWidget(self.vmax_input)
        self.calculation_window_layout.addWidget(self.cam1_nb_label)
        self.calculation_window_layout.addWidget(self.cam1_nb_input)
        self.calculation_window_layout.addWidget(self.cam2_nb_label)
        self.calculation_window_layout.addWidget(self.cam2_nb_input)
        self.calculation_window_layout.addWidget(self.id_kpt_label)
        self.calculation_window_layout.addWidget(self.id_kpt_input1)
        self.calculation_window_layout.addWidget(self.id_kpt_input2)
        self.calculation_window_layout.addWidget(self.weights_kpt_label)
        self.calculation_window_layout.addWidget(self.weights_kpt_input1)
        self.calculation_window_layout.addWidget(self.weights_kpt_input2)
    
    #-----------------------------------PERSON ASSOCIATION --------------------------------

        self.person_association_header = QLabel("Person Association")
        self.person_association_header.setFont(QFont("Arial", 12))

        # Toggle for 'Single Person', toggled by default
        self.single_person_toggle = QCheckBox("Single Person")
        self.single_person_toggle.setChecked(True)

        # Dropdown list for 'Tracked Keypoint'
        self.tracked_keypoint_label = QLabel("Tracked Keypoint:")
        self.tracked_keypoint_dropdown = QComboBox()
        self.tracked_keypoint_dropdown.addItem("Neck")  # Assuming only one option is needed as specified

        # Input for 'Reprojection Error Threshold Association'
        self.reproj_error_threshold_association_label = QLabel("Reproj Error Threshold Association:")
        self.reproj_error_threshold_association_input = QDoubleSpinBox()
        self.setupSpinBox(self.reproj_error_threshold_association_input)

        # Input for 'Likelihood Threshold Association'
        self.likelihood_threshold_association_label = QLabel("Likelihood Threshold Association:")
        self.likelihood_threshold_association_input = QDoubleSpinBox()
        self.likelihood_threshold_association_input.setSingleStep(0.1)
        self.setupSpinBox(self.likelihood_threshold_association_input)

        # Add the 'Person Association' UI elements to the layout
        self.calculation_window_layout.addWidget(self.person_association_header)
        self.calculation_window_layout.addWidget(self.single_person_toggle)
        self.calculation_window_layout.addWidget(self.tracked_keypoint_label)
        self.calculation_window_layout.addWidget(self.tracked_keypoint_dropdown)
        self.calculation_window_layout.addWidget(self.reproj_error_threshold_association_label)
        self.calculation_window_layout.addWidget(self.reproj_error_threshold_association_input)
        self.calculation_window_layout.addWidget(self.likelihood_threshold_association_label)
        self.calculation_window_layout.addWidget(self.likelihood_threshold_association_input)

    #-----------------------------------TRIANGULATION-----------------------------------

    def createTriangulationUI(self):
        # Header for triangulation
        self.triangulation_header = QLabel("Triangulation")
        self.triangulation_header.setFont(QFont("Arial", 12))

        # Labels and input fields for triangulation settings
        self.reproj_error_threshold_triangulation_label = QLabel("Reprojection Error Threshold Triangulation:")
        self.reproj_error_threshold_triangulation_input = QDoubleSpinBox()
        
        self.likelihood_threshold_triangulation_label = QLabel("Likelihood Threshold Triangulation:")
        self.likelihood_threshold_triangulation_input = QDoubleSpinBox()
        
        self.min_cameras_for_triangulation_label = QLabel("Minimum Cameras for triangulation:")
        self.min_cameras_for_triangulation_input = QSpinBox()
        
        self.interpolation_type_label = QLabel("Interpolation Type:")
        self.interpolation_dropdown = QComboBox()
        
        self.interp_if_gap_smaller_than_label = QLabel("Interpolate if Gap is Smaller Than:")
        self.interp_if_gap_smaller_than_input = QDoubleSpinBox()
        
        self.show_interp_indices_toggle = QCheckBox("Show Interp Indices")
        self.handle_LR_swap_toggle = QCheckBox("Handle L/R Swap")
        self.undistort_points_toggle = QCheckBox("Undistort Points")
        self.make_c3d_toggle = QCheckBox("Make C3D")

        # Set default values and configurations for the widgets
        self.setupSpinBox(self.reproj_error_threshold_triangulation_input)
        self.setupSpinBox(self.likelihood_threshold_triangulation_input)
        self.setupSpinBox(self.interp_if_gap_smaller_than_input)
        self.min_cameras_for_triangulation_input.setRange(0, 100)  # Update this as needed
        self.show_interp_indices_toggle.setChecked(True)  # Checked by default

        # Setup the interpolation dropdown
        self.interpolation_dropdown.addItems(["Select", "linear", "slinear", "quadratic", "cubic", "none"])

        # Add the triangulation UI elements to the layout with labels
        self.calculation_window_layout.addWidget(self.triangulation_header)
        self.calculation_window_layout.addWidget(self.reproj_error_threshold_triangulation_label)
        self.calculation_window_layout.addWidget(self.reproj_error_threshold_triangulation_input)
        self.calculation_window_layout.addWidget(self.likelihood_threshold_triangulation_label)
        self.calculation_window_layout.addWidget(self.likelihood_threshold_triangulation_input)
        self.calculation_window_layout.addWidget(self.min_cameras_for_triangulation_label)
        self.calculation_window_layout.addWidget(self.min_cameras_for_triangulation_input)
        self.calculation_window_layout.addWidget(self.interpolation_type_label)
        self.calculation_window_layout.addWidget(self.interpolation_dropdown)
        self.calculation_window_layout.addWidget(self.interp_if_gap_smaller_than_label)
        self.calculation_window_layout.addWidget(self.interp_if_gap_smaller_than_input)
        self.calculation_window_layout.addWidget(self.show_interp_indices_toggle)
        self.calculation_window_layout.addWidget(self.handle_LR_swap_toggle)
        self.calculation_window_layout.addWidget(self.undistort_points_toggle)
        self.calculation_window_layout.addWidget(self.make_c3d_toggle)


    #-----------------------------------FILTERING------------------------------------------------------

    def createFilteringUI(self):
        # Header for filtering
        self.filtering_header = QLabel("Filtering")
        self.filtering_header.setFont(QFont("Arial", 12))
        self.calculation_window_layout.addWidget(self.filtering_header)

        self.filtering_type_dropdown = QComboBox()
        self.filtering_type_dropdown.addItem("Select") 
        self.filtering_type_dropdown.addItems([
            "butterworth", "kalman", "gaussian", "LOESS", "median", "butterworth_on_speed"
        ])
        
        # Connect the dropdown selection change to the handler function
        self.filtering_type_dropdown.currentIndexChanged.connect(self.onFilteringTypeChanged)
        self.calculation_window_layout.addWidget(self.filtering_type_dropdown)
        
        # Create a stacked widget to hold the different settings for each filtering type
        self.filtering_settings_stack = QStackedWidget()
        self.filtering_settings_stack.addWidget(QWidget())
        

        # Layouts for each filtering type
        self.filtering_settings_stack.addWidget(self.createButterworthLayout())  # Index 0
        self.filtering_settings_stack.addWidget(self.createKalmanLayout())      # Index 1
        self.filtering_settings_stack.addWidget(self.createGaussianLayout())    # Index 2
        self.filtering_settings_stack.addWidget(self.createLoessLayout())       # Index 3
        self.filtering_settings_stack.addWidget(self.createMedianLayout())      # Index 4
        self.filtering_settings_stack.addWidget(self.createButterworthLayout()) # Index 5 for butterworth_on_speed
        
        # Add the 'Display Figures' toggle
        self.display_figures_label = QLabel("Display Figures:")
        self.display_figures_toggle = QCheckBox()
        self.display_figures_toggle.setChecked(True)  # Checked by default

        # Create a layout for the 'Display Figures' toggle
        self.display_figures_layout = QHBoxLayout()
        self.display_figures_layout.addWidget(self.display_figures_label)
        self.display_figures_layout.addWidget(self.display_figures_toggle)
        self.display_figures_layout.addStretch()  # Add stretch to push everything to the left

        # Add the 'Display Figures' layout to the main layout below the stacked widget
        self.calculation_window_layout.addLayout(self.display_figures_layout)

        self.calculation_window_layout.addWidget(self.filtering_settings_stack)


    #-----------------------------------FILTERING OPTIONS------------------------------------------------------

    @pyqtSlot(int)
    def onFilteringTypeChanged(self, index):
        # Switch to the corresponding UI elements based on the selected filtering type
        self.filtering_settings_stack.setCurrentIndex(index)

    def createButterworthLayout(self):
        layout = QWidget()
        layout_hbox = QHBoxLayout(layout)
        order_label = QLabel("Order:")
        order_input = QSpinBox()
        order_input.setRange(1, 10)  # Example range, adjust as needed
        cut_off_frequency_label = QLabel("Cut off Frequency:")
        cut_off_frequency_input = QDoubleSpinBox()
        cut_off_frequency_input.setRange(0.01, 1000.00)  # Example range, adjust as needed
        layout_hbox.addWidget(order_label)
        layout_hbox.addWidget(order_input)
        layout_hbox.addWidget(cut_off_frequency_label)
        layout_hbox.addWidget(cut_off_frequency_input)
        return layout

    def createKalmanLayout(self):
        layout = QWidget()
        layout_hbox = QHBoxLayout(layout)
        trust_ratio_label = QLabel("Trust Ratio:")
        trust_ratio_input = QDoubleSpinBox()
        trust_ratio_input.setRange(0.00, 1000.00)  # Example range, adjust as needed
        smooth_label = QLabel("Smooth:")
        smooth_toggle = QCheckBox()
        smooth_toggle.setChecked(True)  # Checked by default
        layout_hbox.addWidget(trust_ratio_label)
        layout_hbox.addWidget(trust_ratio_input)
        layout_hbox.addWidget(smooth_label)
        layout_hbox.addWidget(smooth_toggle)
        return layout

    def createGaussianLayout(self):
        layout = QWidget()
        layout_hbox = QHBoxLayout(layout)
        sigma_kernel_label = QLabel("Sigma Kernel:")
        sigma_kernel_input = QDoubleSpinBox()
        sigma_kernel_input.setRange(0.01, 100.00)  # Example range, adjust as needed
        layout_hbox.addWidget(sigma_kernel_label)
        layout_hbox.addWidget(sigma_kernel_input)
        return layout

    def createLoessLayout(self):
        layout = QWidget()
        layout_hbox = QHBoxLayout(layout)
        nb_values_used_label = QLabel("Nb Values Used:")
        nb_values_used_input = QSpinBox()
        nb_values_used_input.setRange(1, 1000)  # Example range, adjust as needed
        layout_hbox.addWidget(nb_values_used_label)
        layout_hbox.addWidget(nb_values_used_input)
        return layout

    def createMedianLayout(self):
        layout = QWidget()
        layout_hbox = QHBoxLayout(layout)
        kernel_size_label = QLabel("Kernel Size:")
        kernel_size_input = QSpinBox()
        kernel_size_input.setRange(1, 100)  # Example range, adjust as needed
        layout_hbox.addWidget(kernel_size_label)
        layout_hbox.addWidget(kernel_size_input)
        return layout
    









    #-----------------------------------MARKER AUGMENTATION-----------------------------


    def createMarkerAugmentationUI(self):
        # Create 'Marker Augmentation' header
        self.marker_augmentation_header = QLabel("Marker Augmentation")
        self.marker_augmentation_header.setFont(QFont("Arial", 12))

        # Participant height input
        self.participant_height_label = QLabel("Participant height (m):")
        self.participant_height_input = QDoubleSpinBox()
        self.participant_height_input.setRange(0.00, 3.00)  # Example range, adjust as needed

        # Participant mass input
        self.participant_mass_label = QLabel("Participant Mass (kg):")
        self.participant_mass_input = QDoubleSpinBox()
        self.participant_mass_input.setRange(0.00, 300.00)  # Example range, adjust as needed

        # Layout for Marker Augmentation section
        self.marker_augmentation_layout = QVBoxLayout()
        self.marker_augmentation_layout.addWidget(self.marker_augmentation_header)
        self.marker_augmentation_layout.addWidget(self.participant_height_label)
        self.marker_augmentation_layout.addWidget(self.participant_height_input)
        self.marker_augmentation_layout.addWidget(self.participant_mass_label)
        self.marker_augmentation_layout.addWidget(self.participant_mass_input)

        return self.marker_augmentation_layout

    def poseOptionsChanged(self):
        # Check conditions and display "Marker Augmentation" if met
        framework = self.method_dropdown.currentText()
        model = self.model_dropdown.currentText()
        if framework == "OpenPose" and model in ["BODY_25A", "BODY_25B"]:
            if not hasattr(self, 'marker_augmentation_layout'):
                self.marker_augmentation_layout = self.createMarkerAugmentationUI()
            self.calculation_window_layout.addLayout(self.marker_augmentation_layout)
        else:
            # Hide or remove the "Marker Augmentation" section
            if hasattr(self, 'marker_augmentation_layout'):
                self.clearLayout(self.marker_augmentation_layout)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

    #-----------------------------------HANDLER FUNCTIONS----------------------------------------------------------------

    def extrinsicsMethodChanged(self, index):
    # Hide all settings by default
        self.hideAllExtrinsicsSettings()
        
        # Convert index to method name using the dropdown item text
        method = self.extrinsics_method_dropdown.itemText(index)
        if method in ["Board", "Scene"]:
            # Show the settings for 'Board' and 'Scene'
            self.showBoardAndSceneSettings()
       # else:
            # Hide the settings for other methods
          #  self.hideExtrinsicsSettings()

    # Function to show extrinsics settings
        
    def showExtrinsicsSettings(self):
        # Ensure all widgets are initialized before trying to modify their visibility
        if hasattr(self, 'show_reprojection_error_toggle'):
            self.show_reprojection_error_toggle.setVisible(True)
        if hasattr(self, 'extrinsics_extension_dropdown'):
            self.extrinsics_extension_dropdown.setVisible(True)
        if hasattr(self, 'extrinsics_corners_nb_input1'):
            self.extrinsics_corners_nb_input1.setVisible(True)
        if hasattr(self, 'extrinsics_corners_nb_input2'):
            self.extrinsics_corners_nb_input2.setVisible(True)
        if hasattr(self, 'extrinsics_square_size_input1'):
            self.extrinsics_square_size_input1.setVisible(True)
        if hasattr(self, 'extrinsics_square_size_input2'):
            self.extrinsics_square_size_input2.setVisible(True)

    # Function to hide extrinsics settings
    def hideExtrinsicsSettings(self):
        # Ensure all widgets are initialized before trying to modify their visibility
        if hasattr(self, 'show_reprojection_error_toggle'):
            self.show_reprojection_error_toggle.setVisible(False)
        if hasattr(self, 'extrinsics_extension_dropdown'):
            self.extrinsics_extension_dropdown.setVisible(False)
        if hasattr(self, 'extrinsics_corners_nb_input1'):
            self.extrinsics_corners_nb_input1.setVisible(False)
        if hasattr(self, 'extrinsics_corners_nb_input2'):
            self.extrinsics_corners_nb_input2.setVisible(False)
        if hasattr(self, 'extrinsics_square_size_input1'):
            self.extrinsics_square_size_input1.setVisible(False)
        if hasattr(self, 'extrinsics_square_size_input2'):
            self.extrinsics_square_size_input2.setVisible(False)

    # Function to hide all extrinsic related settings
    def hideAllExtrinsicsSettings(self):
        # Hide the widgets if they have been defined
        if hasattr(self, 'show_reprojection_error_toggle'):
            self.show_reprojection_error_toggle.setVisible(False)
        if hasattr(self, 'extrinsics_extension_dropdown'):
            self.extrinsics_extension_dropdown.setVisible(False)
        if hasattr(self, 'extrinsics_corners_nb_input1'):
            self.extrinsics_corners_nb_input1.setVisible(False)
        if hasattr(self, 'extrinsics_corners_nb_input2'):
            self.extrinsics_corners_nb_input2.setVisible(False)
        if hasattr(self, 'extrinsics_square_size_input1'):
            self.extrinsics_square_size_input1.setVisible(False)
        if hasattr(self, 'extrinsics_square_size_input2'):
            self.extrinsics_square_size_input2.setVisible(False)

    # Function to show settings for 'Board' and 'Scene' methods
   
    def showBoardAndSceneSettings(self):
    # Show common settings for both 'Board' and 'Scene'
        self.show_reprojection_error_toggle.setVisible(True)
        self.extrinsics_extension_dropdown.setVisible(True)
        # Hide the corners number and square size inputs which are not used for 'Scene'
        self.extrinsics_corners_nb_input1.setVisible(False)
        self.extrinsics_corners_nb_input2.setVisible(False)
        self.extrinsics_square_size_input1.setVisible(False)
        self.extrinsics_square_size_input2.setVisible(False)

        method = self.extrinsics_method_dropdown.currentText()
        if method == "Scene":
            # Ensure the input for number of rows is created and visible
            if not hasattr(self, 'num_rows_input'):
                self.num_rows_input = QSpinBox()
                self.num_rows_input.setMinimum(1)
                self.num_rows_input.setMaximum(100)
                self.num_rows_input.valueChanged.connect(self.updateObjectCoordinatesTable)
                self.num_rows_label = QLabel("Enter number of rows here:")

            # Find correct index for inserting below 'Extrinsics Square Size'
            extrinsics_size_index = self.calculation_window_layout.indexOf(self.extrinsics_square_size_layout) + 1
            
            # Ensure correct placement relative to 'Extrinsics Square Size'
            self.calculation_window_layout.insertWidget(extrinsics_size_index + 13, self.num_rows_label)
            self.calculation_window_layout.insertWidget(extrinsics_size_index + 14, self.num_rows_input)

            # Create or update 3D Object Coordinates table
            if not hasattr(self, 'object_coordinates_table'):
                self.createObjectCoordinatesTable(self.num_rows_input.value())

            self.calculation_window_layout.insertWidget(extrinsics_size_index + 15, self.object_coordinates_table_label)
            self.calculation_window_layout.insertWidget(extrinsics_size_index + 16, self.object_coordinates_table)
            
            self.object_coordinates_table.setVisible(True)
            self.num_rows_input.setVisible(True)

        elif method == "Board":
            # Specific for 'Board': Show corners number and square size inputs
            self.extrinsics_corners_nb_input1.setVisible(True)
            self.extrinsics_corners_nb_input2.setVisible(True)
            self.extrinsics_square_size_input1.setVisible(True)
            self.extrinsics_square_size_input2.setVisible(True)
            # Hide the 3D Object Coordinates table and number of rows input if they exist
            if hasattr(self, 'num_rows_input'):
                self.num_rows_input.setVisible(False)
            if hasattr(self, 'object_coordinates_table'):
                self.object_coordinates_table.setVisible(False)


        elif method == "Board":
            # Specific for 'Board': Show corners number and square size inputs
            self.extrinsics_corners_nb_input1.setVisible(True)
            self.extrinsics_corners_nb_input2.setVisible(True)
            self.extrinsics_square_size_input1.setVisible(True)
            self.extrinsics_square_size_input2.setVisible(True)
            # Ensure the 3D Object Coordinates table and number of rows input are hidden if they exist
            if hasattr(self, 'num_rows_input'):
                self.num_rows_input.setVisible(False)
            if hasattr(self, 'object_coordinates_table'):
                self.object_coordinates_table.setVisible(False)


   
     






    # Function to create the 3D Object Coordinates table
    def createObjectCoordinatesTable(self, num_rows):
    # Create the table with the number of rows specified by the user
        self.object_coordinates_table = QTableWidget(num_rows, 3)  # num_rows rows, 3 columns
        self.object_coordinates_table.setHorizontalHeaderLabels(['X', 'Y', 'Z'])
        self.object_coordinates_table_label = QLabel("3D Object Coordinates (in m):")
        
        self.board_settings_layout.addWidget(self.object_coordinates_table_label)
        self.board_settings_layout.addWidget(self.object_coordinates_table)

        # Initialize all cells with a QDoubleSpinBox
        for i in range(num_rows):
            for j in range(3):
                spin_box = QDoubleSpinBox()
                spin_box.setRange(-10000, 10000)  # Set an appropriate range
                spin_box.setDecimals(2)
                self.object_coordinates_table.setCellWidget(i, j, spin_box)



    def updateObjectCoordinatesTable(self, num_rows=None):
        if num_rows is None and hasattr(self, 'num_rows_input'):
            num_rows = self.num_rows_input.value()
        if num_rows is not None:
            self.object_coordinates_table.setRowCount(num_rows)
            # Ensure each cell has a QDoubleSpinBox with proper configuration
            for i in range(num_rows):
                for j in range(3):
                    if self.object_coordinates_table.cellWidget(i, j) is None:
                        spin_box = QDoubleSpinBox()
                        spin_box.setRange(-10000, 10000)
                        spin_box.setDecimals(2)
                        self.object_coordinates_table.setCellWidget(i, j, spin_box)
                    else:
                        # Update existing spin boxes to ensure proper range and decimals
                        spin_box = self.object_coordinates_table.cellWidget(i, j)
                        spin_box.setRange(-10000, 10000)
                        spin_box.setDecimals(2)



    def setupSpinBox(self, spin_box):
        spin_box.setFixedWidth(100)  # Set the maximum width to match the existing UI
        spin_box.setDecimals(2)
        spin_box.setRange(0.00, 500.00) 
    def setupDoubleSpinBox(self, spin_box):
        spin_box.setMaximumWidth(100)
        spin_box.setDecimals(2)
        spin_box.setRange(0, 10000)  # Set an appropriate range

    def setupIntSpinBox(self, spin_box):
        spin_box.setFixedWidth(100)
        spin_box.setRange(0, 500) 

   

    @pyqtSlot(bool)
    def on_board_toggled(self, checked):
        if checked:
            self.extra_settings_stack.setCurrentIndex(0)
        else:
            # Assuming that 'Scene' is at index 1 and 'Keypoints' is at index 2, adjust as necessary.
            self.extra_settings_stack.setCurrentIndex(1)  # or 2 for 'Keypoints'







    def radio_button_clicked(self, button):
        # If the button is checked, remember it as the last checked button
        if button.isChecked():
            self.currently_checked_button = button
        else:
            # If the button was unchecked, clear the last checked button
            self.currently_checked_button = None

        # Deselect all other buttons
        for radio_button in self.extrinsics_methods.values():
            if radio_button is not button and radio_button.isChecked():
                radio_button.setChecked(False)

    def handleRadioButtonClicked(self, id):
        button = self.extrinsics_method_group.button(id)
        if self.currently_checked_button == button:
            # If the currently checked button is clicked again, deselect it
            button.setChecked(False)
            self.currently_checked_button = None
            self.hideExtrinsicsSettings()
        else:
            # If another button is clicked, select the new one and update the UI accordingly
            self.currently_checked_button = button
            self.updateExtrinsicsSettings(id)

    def handleRadioDeselection(self, radio_button):
        if radio_button.isChecked():
            self.currently_checked_button = radio_button
        else:
            self.currently_checked_button = None

        for button in self.extrinsics_methods.values():
            if button is not self.currently_checked_button:
                button.setChecked(False)


    def updateUI(self):
        mode = self.mode_select.currentText()
        if mode == "Convert":
            self.convert_layout_widget.show()
            self.calculation_scroll_area.hide()
        elif mode == "Calculate":
            self.calculation_scroll_area.show()
            self.convert_layout_widget.hide()
            self.hideAllExtrinsicsSettings()  # Add this line to hide the extrinsic settings initially
        else:  # for "Select" or any other option, hide both
            self.convert_layout_widget.hide()
            self.calculation_scroll_area.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ConverterCalculatorApp()
    sys.exit(app.exec_())
