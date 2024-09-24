from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import (QHBoxLayout, QHeaderView, QSizePolicy, QTableView, QWidget)
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis

from table_model import CustomTableModel

class Widget(QWidget):
    def __init__(self, data):
        QWidget.__init__(self)

        # Getting the Model
        self.model = CustomTableModel(data)

        # Creating a QTableView
        self.table_view = QTableView()
        self.table_view.setModel(self.model)

        # QTableView Headers
        self.horizontal_header = self.table_view.horizontalHeader()
        self.vertical_header = self.table_view.verticalHeader()
        self.horizontal_header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.vertical_header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.horizontal_header.setStretchLastSection(True)

        # Creating QChart
        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.AllAnimations)
        self.add_series("Angle Over Time", [0, 1])

        # Creating QChartView
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        # QTableView Headers
        self.horizontal_header = self.table_view.horizontalHeader()
        self.vertical_header = self.table_view.verticalHeader()
        self.horizontal_header.setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        self.vertical_header.setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        self.horizontal_header.setStretchLastSection(True)

        # QWidget Layout
        self.main_layout = QHBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        ## Left layout
        size.setHorizontalStretch(1)
        self.table_view.setSizePolicy(size)
        self.main_layout.addWidget(self.table_view)

        ## Right Layout
        size.setHorizontalStretch(4)
        self.chart_view.setSizePolicy(size)
        self.main_layout.addWidget(self.chart_view)

        # Set the layout to the QWidget
        self.setLayout(self.main_layout)

    def add_series(self, name, columns):
        # Create QLineSeries for Right (y)
        self.series_right = QLineSeries()
        self.series_right.setName("Right")

        # Create QLineSeries for Left (y2)
        self.series_left = QLineSeries()
        self.series_left.setName("Left")

        # Filling QLineSeries
        for i in range(self.model.rowCount()):
            # Getting the data
            t = self.model.index(i, 0).data()
            x = float(t)
            y_right = float(self.model.index(i, 1).data())
            y_left = float(self.model.index(i, 2).data())

            if x > 0 and y_right > 0:
                self.series_right.append(x, y_right)
            if x > 0 and y_left > 0:
                self.series_left.append(x, y_left)
        
        self.chart.addSeries(self.series_right)
        self.chart.addSeries(self.series_left)

        # Setting X-axis
        self.axis_x = QValueAxis()
        self.axis_x.setTitleText("Time")
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.series_right.attachAxis(self.axis_x)
        self.series_left.attachAxis(self.axis_x)

        # Setting Y-axis
        self.axis_y = QValueAxis()
        self.axis_y.setLabelFormat("%.2f")
        self.axis_y.setTitleText("Knee Flexion (°)")
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series_right.attachAxis(self.axis_y)
        self.series_left.attachAxis(self.axis_y)

        # Add legend
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)

        # Getting the colors from the QChart to use them on the QTableView
        color_right = self.series_right.pen().color().name()
        color_left = self.series_left.pen().color().name()
        self.model.color_right = f"{color_right}"
        self.model.color_left = f"{color_left}"
