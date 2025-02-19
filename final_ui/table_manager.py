import numpy as np
from PyQt5 import QtWidgets, QtCore

class TableManager:
    def __init__(self, main_window):
        self.main_window = main_window
        
        # Time series data
        self._time = None
        self._hip_flexion_r = None
        self._hip_flexion_l = None
        self._knee_angle_r = None
        self._knee_angle_l = None
        self._ankle_angle_r = None
        self._ankle_angle_l = None
        
    # Properties for time series data
    @property
    def time(self):
        return self._time
        
    @property
    def hip_flexion_r(self):
        return self._hip_flexion_r
        
    @property
    def hip_flexion_l(self):
        return self._hip_flexion_l
        
    @property
    def knee_angle_r(self):
        return self._knee_angle_r
        
    @property
    def knee_angle_l(self):
        return self._knee_angle_l
        
    @property
    def ankle_angle_r(self):
        return self._ankle_angle_r
        
    @property
    def ankle_angle_l(self):
        return self._ankle_angle_l
    
    def display_data_in_table(self, table_widget):
        """
        Displays the motion data in a QTableWidget.
        
        Args:
            table_widget (QTableWidget): The table widget to populate
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if self._time is None:
                return False
                
            # Clear the table
            table_widget.clear()
            table_widget.setRowCount(len(self._time))
            table_widget.setColumnCount(7)  # 7 columns for our data
            
            # Set headers
            headers = ['Time', 'Hip R', 'Hip L', 'Knee R', 'Knee L', 'Ankle R', 'Ankle L']
            table_widget.setHorizontalHeaderLabels(headers)
            
            # Populate data
            for row in range(len(self._time)):
                # Create items for each column
                time_item = QtWidgets.QTableWidgetItem(f"{self._time[row]:.3f}")
                hip_r_item = QtWidgets.QTableWidgetItem(f"{self._hip_flexion_r[row]:.2f}")
                hip_l_item = QtWidgets.QTableWidgetItem(f"{self._hip_flexion_l[row]:.2f}")
                knee_r_item = QtWidgets.QTableWidgetItem(f"{self._knee_angle_r[row]:.2f}")
                knee_l_item = QtWidgets.QTableWidgetItem(f"{self._knee_angle_l[row]:.2f}")
                ankle_r_item = QtWidgets.QTableWidgetItem(f"{self._ankle_angle_r[row]:.2f}")
                ankle_l_item = QtWidgets.QTableWidgetItem(f"{self._ankle_angle_l[row]:.2f}")
                
                # Make items read-only
                time_item.setFlags(time_item.flags() & ~QtCore.Qt.ItemIsEditable)
                hip_r_item.setFlags(hip_r_item.flags() & ~QtCore.Qt.ItemIsEditable)
                hip_l_item.setFlags(hip_l_item.flags() & ~QtCore.Qt.ItemIsEditable)
                knee_r_item.setFlags(knee_r_item.flags() & ~QtCore.Qt.ItemIsEditable)
                knee_l_item.setFlags(knee_l_item.flags() & ~QtCore.Qt.ItemIsEditable)
                ankle_r_item.setFlags(ankle_r_item.flags() & ~QtCore.Qt.ItemIsEditable)
                ankle_l_item.setFlags(ankle_l_item.flags() & ~QtCore.Qt.ItemIsEditable)
                
                # Set items in the table
                table_widget.setItem(row, 0, time_item)
                table_widget.setItem(row, 1, hip_r_item)
                table_widget.setItem(row, 2, hip_l_item)
                table_widget.setItem(row, 3, knee_r_item)
                table_widget.setItem(row, 4, knee_l_item)
                table_widget.setItem(row, 5, ankle_r_item)
                table_widget.setItem(row, 6, ankle_l_item)
                
            # Set all columns to stretch evenly
            header = table_widget.horizontalHeader()
            for col in range(table_widget.columnCount()):
                header.setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)
            
            return True
            
        except Exception as e:
            print(f"Error displaying data in table: {str(e)}")
            return False

    def read_mot_file(self, file_path):
        """
        Reads a .mot file and extracts specific joint angle data.
        
        Args:
            file_path (str): Path to the .mot file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Initialize data lists
            time_data = []
            hip_r_data = []
            hip_l_data = []
            knee_r_data = []
            knee_l_data = []
            ankle_r_data = []
            ankle_l_data = []
            
            # Read the file
            with open(file_path, 'r') as f:
                lines = f.readlines()
                
            # Find the header line with column names
            header_line = None
            data_start = 0
            for i, line in enumerate(lines):
                if 'time' in line:
                    header_line = line.strip().split()
                    data_start = i + 1
                    break
                    
            if not header_line:
                raise ValueError("Could not find header line in .mot file")
                
            # Get column indices for the data we want
            col_indices = {
                'time': header_line.index('time'),
                'hip_flexion_r': header_line.index('hip_flexion_r'),
                'hip_flexion_l': header_line.index('hip_flexion_l'),
                'knee_angle_r': header_line.index('knee_angle_r'),
                'knee_angle_l': header_line.index('knee_angle_l'),
                'ankle_angle_r': header_line.index('ankle_angle_r'),
                'ankle_angle_l': header_line.index('ankle_angle_l')
            }
            
            # Extract data
            for line in lines[data_start:]:
                if line.strip():  # Skip empty lines
                    values = line.strip().split()
                    if len(values) >= max(col_indices.values()):
                        time_data.append(float(values[col_indices['time']]))
                        hip_r_data.append(float(values[col_indices['hip_flexion_r']]))
                        hip_l_data.append(float(values[col_indices['hip_flexion_l']]))
                        knee_r_data.append(float(values[col_indices['knee_angle_r']]))
                        knee_l_data.append(float(values[col_indices['knee_angle_l']]))
                        ankle_r_data.append(float(values[col_indices['ankle_angle_r']]))
                        ankle_l_data.append(float(values[col_indices['ankle_angle_l']]))
            
            # Store data in properties
            self._time = np.array(time_data)
            self._hip_flexion_r = np.array(hip_r_data)
            self._hip_flexion_l = np.array(hip_l_data)
            self._knee_angle_r = np.array(knee_r_data)
            self._knee_angle_l = np.array(knee_l_data)
            self._ankle_angle_r = np.array(ankle_r_data)
            self._ankle_angle_l = np.array(ankle_l_data)
            
            return True
            
        except Exception as e:
            print(f"Error reading .mot file: {str(e)}")
            return False