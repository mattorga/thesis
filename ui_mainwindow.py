import sys
from database.S00_V501.pose2sim import calibrate
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure()
        #self.axes = fig.add_subplot(111)
        super(MyMplCanvas, self).__init__(fig)
        self.setParent(parent)
        self.plot()

    def plot(self):
        calibrate("/Users/mattheworga/Documents/Git/thesis/database/S00_V501")

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)
        self.canvas = MyMplCanvas(self.widget)
        self.layout.addWidget(self.canvas)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())