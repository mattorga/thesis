import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTabWidget, QGridLayout

class ConfigEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Configuration Editor for Markerless Gait Analysis')
        self.setGeometry(300, 300, 600, 300)
        
        layout = QVBoxLayout()
        
        # Tabs
        tabs = QTabWidget()
        project_tab = QWidget()
        processing_tab = QWidget()
        opensim_tab = QWidget()
        
        tabs.addTab(project_tab, "Project")
        tabs.addTab(processing_tab, "Processing")
        tabs.addTab(opensim_tab, "OpenSim")
        
        # Project Tab Layout
        project_layout = QGridLayout()
        project_tab.setLayout(project_layout)

        # Processing Tab Layout - Now Empty
        processing_tab.setLayout(QVBoxLayout())

        # OpenSim Tab Layout - Now Empty
        opensim_tab.setLayout(QVBoxLayout())

        # Frame rate display (not an input)
        frame_rate_label = QLabel('Frame rate:')
        frame_rate_display = QLabel('')  # Assuming 30 is the frame rate to display
        project_layout.addWidget(frame_rate_label, 0, 0)
        project_layout.addWidget(frame_rate_display, 0, 1)
        
        # Frame range display (not an input)
        frame_range_label = QLabel('Frame range:')
        frame_range_display = QLabel('')  # Assuming '1-100' is the frame range to display
        project_layout.addWidget(frame_range_label, 1, 0)
        project_layout.addWidget(frame_range_display, 1, 1)
        
        # Save button
        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save_config)
        layout.addWidget(tabs)
        layout.addWidget(self.save_button)
        
        self.setLayout(layout)

    def save_config(self):
        # Logic to save the configuration goes here
        print("Configuration saved.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ConfigEditor()
    ex.show()
    sys.exit(app.exec_())
