import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QComboBox, QHBoxLayout,
                             QRadioButton, QLabel, QLineEdit, QGroupBox, QScrollArea, QFrame, QCheckBox, QDoubleSpinBox,
                              QLabel, QButtonGroup, QStackedWidget,QTableWidget) 
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSlot
class ConverterCalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Main layout
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

        self.calibrate_extrinsics_header = QLabel("Calibrate Extrinsics")
        self.calibrate_extrinsics_header.setFont(header_font)  # Use the same font as for 'Calculate Intrinsics'
        self.calculation_window_layout.addWidget(self.calibrate_extrinsics_header)

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

        # Get the currently selected method from the dropdown
        method = self.extrinsics_method_dropdown.currentText()
        if method == "Scene":
            # Specific for 'Scene': Show the 3D Object Coordinates table
            if not hasattr(self, 'object_coordinates_table'):
                self.createObjectCoordinatesTable()
            self.object_coordinates_table.setVisible(True)
        elif method == "Board":
            # Specific for 'Board': Show corners number and square size inputs
            self.extrinsics_corners_nb_input1.setVisible(True)
            self.extrinsics_corners_nb_input2.setVisible(True)
            self.extrinsics_square_size_input1.setVisible(True)
            self.extrinsics_square_size_input2.setVisible(True)
            # Ensure the 3D Object Coordinates table is hidden if it exists
            if hasattr(self, 'object_coordinates_table'):
                self.object_coordinates_table.setVisible(False)

    # Function to create the 3D Object Coordinates table
    def createObjectCoordinatesTable(self):
        self.object_coordinates_table = QTableWidget(8, 3)  # 8 rows, 3 columns
        self.object_coordinates_table.setHorizontalHeaderLabels(['X', 'Y', 'Z'])
        self.object_coordinates_table_label = QLabel("3D Object Coordinates:")
        # Add widgets to the layout
        self.board_settings_layout.addWidget(self.object_coordinates_table_label)
        self.board_settings_layout.addWidget(self.object_coordinates_table)
        # Initialize all cells with a QDoubleSpinBox
        for i in range(8):  # 8 rows
            for j in range(3):  # 3 columns
                spin_box = QDoubleSpinBox()
                spin_box.setRange(-10000, 10000)  # Set an appropriate range
                spin_box.setDecimals(2)
                self.object_coordinates_table.setCellWidget(i, j, spin_box)

    def setupDoubleSpinBox(self, spin_box):
        spin_box.setMaximumWidth(100)
        spin_box.setDecimals(2)
        spin_box.setRange(0, 10000)  # Set an appropriate range

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ConverterCalculatorApp()
    sys.exit(app.exec_())
