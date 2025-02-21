from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QColor, QPainter
from PyQt5 import QtWidgets

class ChartManager:
    def __init__(self, main_window):
        """Initialize the chart manager"""
        self.main_window = main_window
        self.current_chart = None
        self.current_view = None
        
    def display_data_in_chart(self, chart_widget, motion_data, scrollable=False):
        """
        Displays the motion data in a chart widget.
        
        Args:
            chart_widget (QWidget): The widget to contain the chart
            motion_data (dict): Dictionary containing time and joint data
            scrollable (bool): If True, makes chart scrollable. If False, fits to available space
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if motion_data is None or 'time' not in motion_data:
                return False

            # Create new chart
            chart = QChart()
            self.current_chart = chart
            
            # Set up series for each joint
            joint_colors = {
                'hip_flexion_r': QColor(255, 0, 0),    # Red
                'hip_flexion_l': QColor(255, 100, 100), # Light red
                'knee_angle_r': QColor(0, 255, 0),     # Green
                'knee_angle_l': QColor(100, 255, 100), # Light green
                'ankle_angle_r': QColor(0, 0, 255),    # Blue
                'ankle_angle_l': QColor(100, 100, 255) # Light blue
            }

            time_data = motion_data['time']
            joint_data = motion_data['joint_data']
            series_dict = {}

            # Create and populate series
            for joint_name, color in joint_colors.items():
                series = QLineSeries()
                series.setName(joint_name)
                pen = QPen(color)
                pen.setWidth(2)
                series.setPen(pen)
                
                # Add data points
                for i, t in enumerate(time_data):
                    series.append(t, joint_data[joint_name][i])
                
                series_dict[joint_name] = series
                chart.addSeries(series)

            # Create and set up axes
            axis_x = QValueAxis()
            axis_x.setTitleText("Time (s)")
            axis_x.setLabelFormat("%.2f")
            
            # Find min and max angles for y-axis
            all_angles = []
            for angles in joint_data.values():
                all_angles.extend(angles)
            min_angle = min(all_angles)
            max_angle = max(all_angles)
            padding = (max_angle - min_angle) * 0.1
            
            axis_y = QValueAxis()
            axis_y.setTitleText("Angle (°)")
            axis_y.setLabelFormat("%.1f")
            axis_y.setRange(min_angle - padding, max_angle + padding)

            # Configure chart based on scrollable parameter
            if scrollable:
                # Set fixed time window for scrollable view (e.g., 5 seconds)
                window_size = 5.0
                axis_x.setRange(time_data[0], time_data[0] + window_size)
                chart.setAnimationOptions(QChart.NoAnimation)
                
                # Enable scrolling by handling mouse events in chart view
                class ScrollableChartView(QChartView):
                    def __init__(self, chart):
                        super().__init__(chart)
                        self.setRubberBand(QChartView.HorizontalRubberBand)
                        self.setMouseTracking(True)
                        self._last_mouse_pos = None
                        
                    def mousePressEvent(self, event):
                        if event.button() == Qt.LeftButton:
                            self._last_mouse_pos = event.pos()
                            event.accept()
                        super().mousePressEvent(event)
                        
                    def mouseMoveEvent(self, event):
                        if event.buttons() & Qt.LeftButton and self._last_mouse_pos:
                            delta = event.pos().x() - self._last_mouse_pos.x()
                            axis = self.chart().axisX()
                            dx = -delta * (axis.max() - axis.min()) / self.width()
                            axis.setRange(axis.min() + dx, axis.max() + dx)
                            self._last_mouse_pos = event.pos()
                            event.accept()
                        super().mouseMoveEvent(event)
                        
                    def mouseReleaseEvent(self, event):
                        if event.button() == Qt.LeftButton:
                            self._last_mouse_pos = None
                            event.accept()
                        super().mouseReleaseEvent(event)
                        
                    def wheelEvent(self, event):
                        factor = 1.1 if event.angleDelta().y() > 0 else 0.9
                        self.chart().zoom(factor)
                        event.accept()
                
                chart_view = ScrollableChartView(chart)
            else:
                # Fit to available space
                axis_x.setRange(min(time_data), max(time_data))
                chart_view = QChartView(chart)

            # Add axes to chart
            chart.addAxis(axis_x, Qt.AlignBottom)
            chart.addAxis(axis_y, Qt.AlignLeft)

            # Attach axes to all series
            for series in series_dict.values():
                series.attachAxis(axis_x)
                series.attachAxis(axis_y)

            # Set chart title and legend
            chart.setTitle("Joint Angles Over Time")
            chart.legend().setVisible(False)

            # Configure chart view
            self.current_view = chart_view
            chart_view.setRenderHint(QPainter.Antialiasing)

            # Clear existing layout and widgets
            if chart_widget.layout() is not None:
                while chart_widget.layout().count():
                    item = chart_widget.layout().takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()
                chart_widget.layout().deleteLater()

            # Create new layout
            layout = QtWidgets.QVBoxLayout(chart_widget)
            layout.setContentsMargins(0, 0, 0, 0)
            chart_widget.setLayout(layout)
            
            # Add chart view to layout
            layout.addWidget(chart_view)
            
            return True
            
        except Exception as e:
            print(f"Error displaying data in chart: {str(e)}")
            return False

    def cleanup(self):
        """Clean up resources"""
        if self.current_view:
            self.current_view.deleteLater()
            self.current_view = None
        if self.current_chart:
            self.current_chart.deleteLater()
            self.current_chart = None