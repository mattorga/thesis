from PyQt5 import QtWidgets, QtCore

class TableManager:
    def __init__(self, main_window):
        self.main_window = main_window

    def display_data_in_table(self, table_widget, motion_data):
        """
        Displays the motion data in a QTableWidget.

        Args:
            table_widget (QTableWidget): The table widget to populate
            motion_data (dict): Dictionary containing time and joint data
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if motion_data is None or 'time' not in motion_data:
                return False
                
            time_data = motion_data['time']
            joint_data = motion_data['joint_data']
                
            # Clear the table
            table_widget.clear()
            table_widget.setRowCount(len(time_data))
            table_widget.setColumnCount(7)  # 7 columns for our data
            
            # Set headers
            headers = ['Time', 'Hip R', 'Hip L', 'Knee R', 'Knee L', 'Ankle R', 'Ankle L']
            table_widget.setHorizontalHeaderLabels(headers)
            
            # Populate data
            for row in range(len(time_data)):
                # Create items for each column
                items = [
                    QtWidgets.QTableWidgetItem(f"{time_data[row]:.3f}"),
                    QtWidgets.QTableWidgetItem(f"{joint_data['hip_flexion_r'][row]:.2f}"),
                    QtWidgets.QTableWidgetItem(f"{joint_data['hip_flexion_l'][row]:.2f}"),
                    QtWidgets.QTableWidgetItem(f"{joint_data['knee_angle_r'][row]:.2f}"),
                    QtWidgets.QTableWidgetItem(f"{joint_data['knee_angle_l'][row]:.2f}"),
                    QtWidgets.QTableWidgetItem(f"{joint_data['ankle_angle_r'][row]:.2f}"),
                    QtWidgets.QTableWidgetItem(f"{joint_data['ankle_angle_l'][row]:.2f}")
                ]
                
                # Make items read-only and add to table
                for col, item in enumerate(items):
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                    table_widget.setItem(row, col, item)
                
            # Set all columns to stretch evenly
            header = table_widget.horizontalHeader()
            for col in range(table_widget.columnCount()):
                header.setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)
            
            return True
            
        except Exception as e:
            print(f"Error displaying data in table: {str(e)}")
            return False