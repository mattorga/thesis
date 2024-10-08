import argparse
import pandas as pd

from PyQt5.QtWidgets import QApplication

from main_window import MainWindow
from main_widget import Widget

from qt_material import apply_stylesheet

import sys

def read_data(file):
    df = pd.read_csv(file)

    hip_flexion_r = df["hip_flexion_r"]
    hip_flexion_l = df["hip_flexion_l"]

    knee_angle_r = df["knee_angle_r"]
    knee_angle_l = df["knee_angle_l"]

    ankle_angle_r = df["ankle_angle_r"]
    ankle_angle_l = df["ankle_angle_l"]

    time = df["time"]

    return time, hip_flexion_r, hip_flexion_l, knee_angle_r, knee_angle_l, ankle_angle_r, ankle_angle_l

if __name__ == "__main__":
    data = read_data("/Users/mattheworga/Documents/Git/DLSU/thesis/opensim-angle-plots/test_output_filtered.csv")

    print(data)

    app = QApplication(sys.argv)

    widget = Widget(data)
    window = MainWindow(widget)

    apply_stylesheet(app, theme='dark_teal.xml')

    window.show()

    sys.exit(app.exec_())