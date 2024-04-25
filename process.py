import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QComboBox, QHBoxLayout,
                             QRadioButton, QLabel, QLineEdit, QGroupBox)

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
        self.layout.addWidget(self.mode_select)

        # Set initial window size
        self.setGeometry(300, 300, 800, 600)  # You can adjust the size as needed

        # Initialize the conversion and calculation layouts
        self.convert_layout = QVBoxLayout()
        self.createConvertOptions()
        self.convert_layout_widget = QWidget()  # Wrap convert_layout in a QWidget for easy show/hide
        self.convert_layout_widget.setLayout(self.convert_layout)
        self.layout.addWidget(self.convert_layout_widget)

        # Initially hide the conversion layout
        self.convert_layout_widget.hide()

        # Set main layout
        self.setLayout(self.layout)
        self.setWindowTitle('Convert or Calculate')
        self.show()

    def createConvertOptions(self):
        # Group box for conversion settings
        self.convert_group = QGroupBox("Convert From:")
        self.radio_button_layout = QHBoxLayout()

        # Radio buttons for each system
        systems = ['Qualisys', 'Optitrack', 'Vicon', 'Opencap', 'Easymocap', 'Biocv']
        self.radio_buttons = {system: QRadioButton(system) for system in systems}
        for system, radio_button in self.radio_buttons.items():
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

    def updateUI(self):
        mode = self.mode_select.currentText()
        if mode == "Convert":
            self.convert_layout_widget.show()
        else:
            self.convert_layout_widget.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ConverterCalculatorApp()
    sys.exit(app.exec_())
