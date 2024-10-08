from PyQt5.QtCore import QDateTime, Qt, pyqtSlot
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QHeaderView, QSizePolicy, QTableView, QWidget, QSlider, QTabWidget, QSplitter, QScrollArea)
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis, QScatterSeries

from table_model import CustomTableModel

class Widget(QWidget):
    def __init__(self, data):
        QWidget.__init__(self)

        # Getting the Models
        self.hip_model = CustomTableModel(data[0], data[1], data[2], "Hip")
        self.knee_model = CustomTableModel(data[0], data[3], data[4], "Knee")
        self.ankle_model = CustomTableModel(data[0], data[5], data[6], "Ankle")

        # Create tab widget
        self.tab_widget = QTabWidget()

        # Create tabs
        self.all_tab = self.create_all_tab()
        self.hip_tab = self.create_tab(self.hip_model, "Hip Flexion")
        self.knee_tab = self.create_tab(self.knee_model, "Knee Angle")
        self.ankle_tab = self.create_tab(self.ankle_model, "Ankle Angle")

        # Add tabs to the widget, with 'All' as the first tab
        self.tab_widget.addTab(self.all_tab, "All")
        self.tab_widget.addTab(self.hip_tab, "Hip")
        self.tab_widget.addTab(self.knee_tab, "Knee")
        self.tab_widget.addTab(self.ankle_tab, "Ankle")

        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.tab_widget)

        # Set the layout to the QWidget
        self.setLayout(self.main_layout)

    def create_tab(self, model, title):
        tab = QWidget()
        
        # Creating a QTableView
        table_view = QTableView()
        table_view.setModel(model)

        # QTableView Headers
        horizontal_header = table_view.horizontalHeader()
        vertical_header = table_view.verticalHeader()
        
        # Set all columns to stretch mode
        for i in range(model.columnCount()):
            horizontal_header.setSectionResizeMode(i, QHeaderView.Stretch)
        
        vertical_header.setSectionResizeMode(QHeaderView.ResizeToContents)

        # Creating QChart
        chart = QChart()
        chart.setAnimationOptions(QChart.AllAnimations)
        self.add_series(chart, title, model)

        # Creating QChartView
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        # Create a vertical line series
        vertical_line = QLineSeries()
        chart.addSeries(vertical_line)
        vertical_line.attachAxis(chart.axes(Qt.Horizontal)[0])
        vertical_line.attachAxis(chart.axes(Qt.Vertical)[0])

        # Create scatter series for the selected points
        selected_point_right = QScatterSeries()
        selected_point_left = QScatterSeries()
        chart.addSeries(selected_point_right)
        chart.addSeries(selected_point_left)
        selected_point_right.attachAxis(chart.axes(Qt.Horizontal)[0])
        selected_point_right.attachAxis(chart.axes(Qt.Vertical)[0])
        selected_point_left.attachAxis(chart.axes(Qt.Horizontal)[0])
        selected_point_left.attachAxis(chart.axes(Qt.Vertical)[0])

        # Create Slider
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(model.rowCount() - 1)

        # Layout
        layout = QVBoxLayout()
        chart_layout = QHBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Left layout (Table)
        size.setHorizontalStretch(1)
        table_view.setSizePolicy(size)
        chart_layout.addWidget(table_view)

        # Right Layout (Chart)
        size.setHorizontalStretch(4)
        chart_view.setSizePolicy(size)
        chart_layout.addWidget(chart_view)

        layout.addLayout(chart_layout)
        layout.addWidget(slider)

        tab.setLayout(layout)

        # Connect signals
        table_view.selectionModel().selectionChanged.connect(lambda selected, deselected: self.on_row_selected(selected, deselected, model, vertical_line, selected_point_right, selected_point_left, slider))
        slider.valueChanged.connect(lambda value: self.on_slider_value_changed(value, model, table_view, vertical_line, selected_point_right, selected_point_left))

        # Set initial state
        slider.setValue(0)
        table_view.selectRow(0)
        self.update_chart_indicators(0, model, vertical_line, selected_point_right, selected_point_left)

        return tab

    def create_all_tab(self):
        tab = QWidget()
        main_layout = QHBoxLayout()

        # Create a splitter for resizable sections
        splitter = QSplitter(Qt.Horizontal)

        # Left side: Tables
        tables_widget = QWidget()
        tables_layout = QVBoxLayout(tables_widget)

        # Create tables for each joint
        hip_table = self.create_table(self.hip_model, "Hip Flexion")
        knee_table = self.create_table(self.knee_model, "Knee Angle")
        ankle_table = self.create_table(self.ankle_model, "Ankle Angle")

        tables_layout.addWidget(hip_table)
        tables_layout.addWidget(knee_table)
        tables_layout.addWidget(ankle_table)

        # Right side: Charts
        charts_widget = QWidget()
        charts_layout = QVBoxLayout(charts_widget)

        # Create charts without legends
        hip_chart = self.create_chart(self.hip_model, "Hip Flexion", show_legend=False)
        knee_chart = self.create_chart(self.knee_model, "Knee Angle", show_legend=False)
        ankle_chart = self.create_chart(self.ankle_model, "Ankle Angle", show_legend=False)

        charts_layout.addWidget(hip_chart)
        charts_layout.addWidget(knee_chart)
        charts_layout.addWidget(ankle_chart)

        # Create a slider for all charts and tables
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(self.hip_model.rowCount() - 1)
        charts_layout.addWidget(slider)

        # Add widgets to splitter
        splitter.addWidget(tables_widget)
        splitter.addWidget(charts_widget)

        # Set initial sizes
        splitter.setSizes([int(self.width() * 0.2), int(self.width() * 0.8)])

        main_layout.addWidget(splitter)
        tab.setLayout(main_layout)

        # Connect signals
        slider.valueChanged.connect(lambda value: self.update_all_charts_and_tables(value, [hip_chart, knee_chart, ankle_chart], [hip_table, knee_table, ankle_table], [self.hip_model, self.knee_model, self.ankle_model]))

        # Set initial state
        slider.setValue(0)
        self.update_all_charts_and_tables(0, [hip_chart, knee_chart, ankle_chart], [hip_table, knee_table, ankle_table], [self.hip_model, self.knee_model, self.ankle_model])

        return tab
    
    def create_chart(self, model, title, show_legend=True):
        chart = QChart()
        chart.setAnimationOptions(QChart.AllAnimations)
        self.add_series(chart, title, model)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        # Create a vertical line series
        vertical_line = QLineSeries()
        chart.addSeries(vertical_line)
        vertical_line.attachAxis(chart.axes(Qt.Horizontal)[0])
        vertical_line.attachAxis(chart.axes(Qt.Vertical)[0])

        # Create scatter series for the selected points
        selected_point_right = QScatterSeries()
        selected_point_left = QScatterSeries()
        chart.addSeries(selected_point_right)
        chart.addSeries(selected_point_left)
        selected_point_right.attachAxis(chart.axes(Qt.Horizontal)[0])
        selected_point_right.attachAxis(chart.axes(Qt.Vertical)[0])
        selected_point_left.attachAxis(chart.axes(Qt.Horizontal)[0])
        selected_point_left.attachAxis(chart.axes(Qt.Vertical)[0])

        # Set legend visibility based on the show_legend parameter
        chart.legend().setVisible(show_legend)

        return chart_view

    def create_table(self, model, title):
        table_view = QTableView()
        table_view.setModel(model)

        # QTableView Headers
        horizontal_header = table_view.horizontalHeader()
        vertical_header = table_view.verticalHeader()
        
        # Set all columns to stretch mode
        for i in range(model.columnCount()):
            horizontal_header.setSectionResizeMode(i, QHeaderView.Stretch)
        
        vertical_header.setSectionResizeMode(QHeaderView.ResizeToContents)

        return table_view

    def update_all_charts_and_tables(self, value, charts, tables, models):
        for chart, model in zip(charts, models):
            self.update_individual_chart(value, model, chart.chart().series()[-3], chart.chart().series()[-2], chart.chart().series()[-1])
        for table in tables:
            table.selectRow(value)


    def on_all_charts_row_selected(self, selected, deselected, charts, slider):
        if selected.indexes():
            row = selected.indexes()[0].row()
            self.update_all_charts(row, charts, selected.model())
            slider.setValue(row)

    def add_series(self, chart, name, model):
        # Create QLineSeries for Right (y)
        series_right = QLineSeries()
        series_right.setName(f"Right {name}")

        # Create QLineSeries for Left (y2)
        series_left = QLineSeries()
        series_left.setName(f"Left {name}")

        # Variables to store min and max values
        min_y = float('inf')
        max_y = float('-inf')

        # Filling QLineSeries
        for i in range(model.rowCount()):
            # Getting the data
            t = model.index(i, 0).data()
            x = float(t)
            y_right = float(model.index(i, 1).data())
            y_left = float(model.index(i, 2).data())

            if x > 0 and y_right > 0:
                series_right.append(x, y_right)
                min_y = min(min_y, y_right)
                max_y = max(max_y, y_right)
            if x > 0 and y_left > 0:
                series_left.append(x, y_left)
                min_y = min(min_y, y_left)
                max_y = max(max_y, y_left)

        # Set colors for the series
        pen_right = QPen(QColor(0, 0, 255))  # Blue for right joint
        pen_right.setWidth(2)
        series_right.setPen(pen_right)

        pen_left = QPen(QColor(255, 165, 0))  # Orange for left joint
        pen_left.setWidth(2)
        series_left.setPen(pen_left)

        chart.addSeries(series_right)
        chart.addSeries(series_left)

        # Setting X-axis
        axis_x = QValueAxis()
        axis_x.setTitleText("Time")
        chart.addAxis(axis_x, Qt.AlignBottom)
        series_right.attachAxis(axis_x)
        series_left.attachAxis(axis_x)

        # Setting Y-axis
        axis_y = QValueAxis()
        axis_y.setLabelFormat("%.2f")
        axis_y.setTitleText(f"{name} (°)")
        
        # Set the range with some padding
        padding = (max_y - min_y) * 0.1  # 10% padding
        axis_y.setRange(min_y - padding, max_y + padding)
        
        chart.addAxis(axis_y, Qt.AlignLeft)
        series_right.attachAxis(axis_y)
        series_left.attachAxis(axis_y)

        # Add legend
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
    
    def update_individual_chart(self, row, model, vertical_line, selected_point_right, selected_point_left):
        time = float(model.index(row, 0).data())
        right_angle = float(model.index(row, 1).data())
        left_angle = float(model.index(row, 2).data())

        # Update the vertical line
        vertical_line.clear()
        chart = vertical_line.chart()
        y_min = chart.axes(Qt.Vertical)[0].min()
        y_max = chart.axes(Qt.Vertical)[0].max()
        vertical_line.append(time, y_min)
        vertical_line.append(time, y_max)

        # Update the selected points
        selected_point_right.clear()
        selected_point_left.clear()
        selected_point_right.append(time, right_angle)
        selected_point_left.append(time, left_angle)

        # Set the line and points color and width
        pen = QPen(Qt.black)
        pen.setWidth(1)
        vertical_line.setPen(pen)
        selected_point_right.setMarkerSize(10)
        selected_point_left.setMarkerSize(10)
        selected_point_right.setColor(Qt.red)
        selected_point_left.setColor(Qt.red)

        chart.update()

    @pyqtSlot('QItemSelection', 'QItemSelection')
    def on_row_selected(self, selected, deselected, model, vertical_line, selected_point_right, selected_point_left, slider):
        if selected.indexes():
            row = selected.indexes()[0].row()
            self.update_chart_indicators(row, model, vertical_line, selected_point_right, selected_point_left)
            slider.setValue(row)

    @pyqtSlot(int)
    def on_slider_value_changed(self, value, model, table_view, vertical_line, selected_point_right, selected_point_left):
        self.update_chart_indicators(value, model, vertical_line, selected_point_right, selected_point_left)
        table_view.selectRow(value)

    def update_chart_indicators(self, row, model, vertical_line, selected_point_right, selected_point_left):
        if model is None:
            # This is for the "All Charts" tab
            time = float(self.hip_model.index(row, 0).data())
            right_angle = float(self.hip_model.index(row, 1).data())
            left_angle = float(self.hip_model.index(row, 2).data())
        else:
            time = float(model.index(row, 0).data())
            right_angle = float(model.index(row, 1).data())
            left_angle = float(model.index(row, 2).data())

        # Update the vertical line
        vertical_line.clear()
        chart = vertical_line.chart()
        y_min = chart.axes(Qt.Vertical)[0].min()
        y_max = chart.axes(Qt.Vertical)[0].max()
        vertical_line.append(time, y_min)
        vertical_line.append(time, y_max)

        # Update the selected points
        selected_point_right.clear()
        selected_point_left.clear()
        selected_point_right.append(time, right_angle)
        selected_point_left.append(time, left_angle)

        # Set the line and points color and width
        pen = QPen(Qt.black)
        pen.setWidth(1)
        vertical_line.setPen(pen)
        selected_point_right.setMarkerSize(10)
        selected_point_left.setMarkerSize(10)
        selected_point_right.setColor(Qt.red)
        selected_point_left.setColor(Qt.red)

        chart.update()