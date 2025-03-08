from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis, QScatterSeries, QLegend
from PyQt5.QtCore import Qt, QPointF, QMargins
from PyQt5.QtGui import QPen, QColor, QPainter, QFont, QBrush

from PyQt5 import QtWidgets

class ChartManager:
    def __init__(self, main_window):
        """Initialize the chart manager"""
        self.main_window = main_window
        
        # For analytics page
        self.current_chart = None
        self.current_view = None
        self.vertical_line = None
        self.time_data = None
        
        # For comparative page
        self.base_chart = None
        self.base_view = None
        self.base_vertical_line = None
        self.base_time_data = None
        
        self.versus_chart = None
        self.versus_view = None
        self.versus_vertical_line = None
        self.versus_time_data = None
        
    def display_data_in_chart(self, chart_widget, motion_data, scrollable=False, joint_filter="all"):
        """
        Displays the motion data in a chart widget.
        
        Args:
            chart_widget (QWidget): The widget to contain the chart
            motion_data (dict): Dictionary containing time and joint data
            scrollable (bool): If True, makes chart scrollable. If False, fits to available space
            joint_filter (str): Filter for chart series ("all", "hip", "knee", "ankle")
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if motion_data is None or 'time' not in motion_data:
                return False

            # Save time data for later use with vertical line based on the widget
            if chart_widget == self.main_window.ui.trialChart:
                self.time_data = motion_data['time']
            elif chart_widget == self.main_window.ui.baseTrialChart:
                self.base_time_data = motion_data['time']
            elif chart_widget == self.main_window.ui.versusTrialChart:
                self.versus_time_data = motion_data['time']

            # Create new chart
            chart = QChart()
            
            # Store the chart reference based on the widget
            if chart_widget == self.main_window.ui.trialChart:
                self.current_chart = chart
            elif chart_widget == self.main_window.ui.baseTrialChart:
                self.base_chart = chart
            elif chart_widget == self.main_window.ui.versusTrialChart:
                self.versus_chart = chart
            
            # Set up series for each joint
            joint_colors = {
                'hip_flexion_r': QColor(255, 0, 0),    # Red
                'hip_flexion_l': QColor(255, 100, 100), # Light red
                'knee_angle_r': QColor(0, 255, 0),     # Green
                'knee_angle_l': QColor(100, 255, 100), # Light green
                'ankle_angle_r': QColor(0, 0, 255),    # Blue
                'ankle_angle_l': QColor(100, 100, 255) # Light blue
            }

            # Determine which joints to display based on the filter
            if joint_filter == "all":
                visible_joints = list(joint_colors.keys())
            elif joint_filter == "hip":
                visible_joints = ['hip_flexion_r', 'hip_flexion_l']
            elif joint_filter == "knee":
                visible_joints = ['knee_angle_r', 'knee_angle_l']
            elif joint_filter == "ankle":
                visible_joints = ['ankle_angle_r', 'ankle_angle_l']
            else:
                visible_joints = list(joint_colors.keys())

            time_data = motion_data['time']
            joint_data = motion_data['joint_data']
            series_dict = {}

            # Create and populate series for visible joints only
            for joint_name in visible_joints:
                if joint_name in joint_colors and joint_name in joint_data:
                    series = QLineSeries()
                    series.setName(joint_name)
                    pen = QPen(joint_colors[joint_name])
                    pen.setWidth(2)
                    series.setPen(pen)
                    
                    # Add data points
                    for i, t in enumerate(time_data):
                        if i < len(joint_data[joint_name]):
                            series.append(t, joint_data[joint_name][i])
                    
                    series_dict[joint_name] = series
                    chart.addSeries(series)

            # If no series were added (shouldn't happen), return
            if not series_dict:
                return False

            # Create and set up axes
            axis_x = QValueAxis()
            axis_x.setTitleText("Time (s)")
            axis_x.setLabelFormat("%.2f")
            
            # Find min and max angles for y-axis
            all_angles = []
            for joint_name in visible_joints:
                if joint_name in joint_data:
                    all_angles.extend(joint_data[joint_name])
                    
            if not all_angles:
                return False
                
            min_angle = min(all_angles)
            max_angle = max(all_angles)
            padding = (max_angle - min_angle) * 0.1
            
            axis_y = QValueAxis()
            axis_y.setTitleText("Angle (°)")
            axis_y.setLabelFormat("%.1f")
            axis_y.setRange(min_angle - padding, max_angle + padding)

            # Add vertical line series (initially at first time point)
            vertical_line = QLineSeries()
            vertical_line.setName("Position")
            vertical_pen = QPen(QColor(0, 0, 0))  # Black color
            vertical_pen.setWidth(1)  # Line width
            vertical_pen.setStyle(Qt.SolidLine)
            vertical_line.setPen(vertical_pen)
            
            # Store the vertical line reference based on the widget
            if chart_widget == self.main_window.ui.trialChart:
                self.vertical_line = vertical_line
            elif chart_widget == self.main_window.ui.baseTrialChart:
                self.base_vertical_line = vertical_line
            elif chart_widget == self.main_window.ui.versusTrialChart:
                self.versus_vertical_line = vertical_line
            
            # Add two points to create vertical line from bottom to top of y-axis
            # Make sure line extends beyond the visible area
            vertical_line.append(time_data[0], min_angle - padding*2)
            vertical_line.append(time_data[0], max_angle + padding*2)
            
            # Add series to chart AFTER creating axes but BEFORE attaching axes to other series
            chart.addSeries(vertical_line)

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

            # Attach axes to all series, including vertical line
            for series in series_dict.values():
                series.attachAxis(axis_x)
                series.attachAxis(axis_y)
                
            # Make sure vertical line is attached to axes
            vertical_line.attachAxis(axis_x)
            vertical_line.attachAxis(axis_y)

            # Show legend if there's more than one series
            if len(series_dict) > 1:
                chart.legend().setVisible(True)
                chart.legend().setAlignment(Qt.AlignTop)  # Position at top instead of bottom
                chart.legend().setMarkerShape(QLegend.MarkerShapeFromSeries)
                # Optionally adjust legend layout for better space utilization
                chart.legend().setMaximumHeight(50)  # Limit legend height
            else:
                chart.legend().setVisible(False)
                
            # Make the vertical line not appear in the legend
            chart.legend().markers(vertical_line)[0].setVisible(False)

            # Configure chart view
            chart_view.setRenderHint(QPainter.Antialiasing)
            
            # Store the view reference based on the widget
            if chart_widget == self.main_window.ui.trialChart:
                self.current_view = chart_view
            elif chart_widget == self.main_window.ui.baseTrialChart:
                self.base_view = chart_view
            elif chart_widget == self.main_window.ui.versusTrialChart:
                self.versus_view = chart_view

            # Chart Margins
            chart.setMargins(QMargins(0, 0, 0, 0))
            chart.layout().setContentsMargins(0, 0, 0, 0)
            chart.setBackgroundRoundness(0)

            chart_view.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            chart_view.setRenderHint(QPainter.Antialiasing)
            chart_view.setContentsMargins(0, 0, 0, 0)
            
            chart.setTitleBrush(QBrush(Qt.black))
            chart.setTitleFont(QFont("Arial", 10))

            # OPTION 1: Clear existing widgets from layout and reuse it
            if chart_widget.layout() is not None:
                # Get the existing layout
                layout = chart_widget.layout()
                
                # Clear all widgets from the layout
                while layout.count():
                    item = layout.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()
                
                # Add the new chart view to the existing layout
                layout.setContentsMargins(0, 0, 0, 0)
                layout.addWidget(chart_view)
            else:
                # Create new layout only if one doesn't exist
                layout = QtWidgets.QVBoxLayout(chart_widget)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.addWidget(chart_view)
            
            return True
            
        except Exception as e:
            print(f"Error displaying data in chart: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

    def update_vertical_line(self, row_index):
        """
        Updates the position of the vertical line based on the current row index
        
        Args:
            row_index (int): The current row index corresponding to the slider value
        """
        try:
            # More thorough checks to prevent errors
            if self.vertical_line is None:
                print("Cannot update vertical line - vertical line is None")
                return
                
            if self.time_data is None:
                print("Cannot update vertical line - time data is None")
                return
                
            if row_index < 0 or row_index >= len(self.time_data):
                print(f"Cannot update vertical line - index {row_index} out of range (0-{len(self.time_data)-1})")
                return
                
            # Get time value at the current row index
            time_value = self.time_data[row_index]
            # print(f"Updating vertical line to time index {row_index}, value {time_value}")
            
            # Check if chart and axes are available
            if not self.current_chart:
                print("Cannot update vertical line - chart is None")
                return
                
            if not self.current_chart.axes(Qt.Vertical) or len(self.current_chart.axes(Qt.Vertical)) == 0:
                print("Cannot update vertical line - y-axis not available")
                return
                
            # Clear existing points
            self.vertical_line.clear()
            
            # Get current y-axis range
            axis_y = self.current_chart.axes(Qt.Vertical)[0]
            min_y = axis_y.min()
            max_y = axis_y.max()
            
            # Add two points to create vertical line from bottom to top of y-axis
            # Extend beyond visible area to ensure it spans the entire chart
            padding = (max_y - min_y) * 0.2  # 20% padding above and below
            self.vertical_line.append(time_value, min_y - padding)
            self.vertical_line.append(time_value, max_y + padding)
            
            # Force chart to update
            if self.current_view:
                self.current_view.update()
            else:
                print("Cannot update vertical line - chart view is None")
            
        except Exception as e:
            print(f"Error updating vertical line: {str(e)}")
            import traceback
            traceback.print_exc()  # More detailed error information
    def update_comparative_vertical_lines(self, row_index):
        """
        Updates the position of the vertical lines on both charts in the comparative page
        
        Args:
            row_index (int): The current row index corresponding to the slider value
        """
        try:
            # Update base trial chart vertical line
            if self.base_vertical_line is not None and self.base_time_data is not None:
                if 0 <= row_index < len(self.base_time_data):
                    # Get time value at the current row index
                    time_value = self.base_time_data[row_index]
                    
                    # Check if chart and axes are available
                    if not self.base_chart:
                        print("Cannot update base vertical line - chart is None")
                        return
                        
                    if not self.base_chart.axes(Qt.Vertical) or len(self.base_chart.axes(Qt.Vertical)) == 0:
                        print("Cannot update base vertical line - y-axis not available")
                        return
                        
                    # Clear existing points
                    self.base_vertical_line.clear()
                    
                    # Get current y-axis range
                    axis_y = self.base_chart.axes(Qt.Vertical)[0]
                    min_y = axis_y.min()
                    max_y = axis_y.max()
                    
                    # Add two points to create vertical line from bottom to top of y-axis
                    # Extend beyond visible area to ensure it spans the entire chart
                    padding = (max_y - min_y) * 0.2  # 20% padding above and below
                    self.base_vertical_line.append(time_value, min_y - padding)
                    self.base_vertical_line.append(time_value, max_y + padding)
                    
                    # Force chart to update
                    if self.base_view:
                        self.base_view.update()
            
            # Update versus trial chart vertical line
            if self.versus_vertical_line is not None and self.versus_time_data is not None:
                if 0 <= row_index < len(self.versus_time_data):
                    # Get time value at the current row index
                    time_value = self.versus_time_data[row_index]
                    
                    # Check if chart and axes are available
                    if not self.versus_chart:
                        print("Cannot update versus vertical line - chart is None")
                        return
                        
                    if not self.versus_chart.axes(Qt.Vertical) or len(self.versus_chart.axes(Qt.Vertical)) == 0:
                        print("Cannot update versus vertical line - y-axis not available")
                        return
                        
                    # Clear existing points
                    self.versus_vertical_line.clear()
                    
                    # Get current y-axis range
                    axis_y = self.versus_chart.axes(Qt.Vertical)[0]
                    min_y = axis_y.min()
                    max_y = axis_y.max()
                    
                    # Add two points to create vertical line from bottom to top of y-axis
                    # Extend beyond visible area to ensure it spans the entire chart
                    padding = (max_y - min_y) * 0.2  # 20% padding above and below
                    self.versus_vertical_line.append(time_value, min_y - padding)
                    self.versus_vertical_line.append(time_value, max_y + padding)
                    
                    # Force chart to update
                    if self.versus_view:
                        self.versus_view.update()
        
        except Exception as e:
            print(f"Error updating comparative vertical lines: {str(e)}")
            import traceback
            traceback.print_exc()  # More detailed error information

    def reapply_chart_vertical_line(self, row_index):
        """
        Ensures the vertical line in the chart is positioned correctly.
        Call this after any operation that might refresh the chart.
        
        Args:
            row_index (int): The index corresponding to the time point
        """
        if self.vertical_line is not None and self.time_data is not None:
            # Update the vertical line position based on specified row
            self.update_vertical_line(row_index)
    def reapply_comparative_chart_vertical_lines(self, row_index):
        """
        Ensures the vertical lines in both comparative charts are positioned correctly.
        Call this after any operation that might refresh the charts.
        
        Args:
            row_index (int): The index corresponding to the time point
        """
        # Update the vertical line positions on both charts
        self.update_comparative_vertical_lines(row_index)

    def cleanup(self):
        """Clean up resources"""
        if self.current_view:
            self.current_view.deleteLater()
            self.current_view = None
        if self.current_chart:
            self.current_chart.deleteLater()
            self.current_chart = None