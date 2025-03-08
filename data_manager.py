import numpy as np
import csv

class DataManager:
    def __init__(self):
        # Initialize data containers
        self._time = None
        self._joint_data = {}

    def read_mot_file(self, file_path):
        """
        Reads a .mot file and extracts joint angle data.
        
        Args:
            file_path (str): Path to the .mot file
            
        Returns:
            dict: Dictionary containing time series and joint angle data
        """
        try:
            # Initialize data lists
            time_data = []
            joint_data = {
                'hip_flexion_r': [],
                'hip_flexion_l': [],
                'knee_angle_r': [],
                'knee_angle_l': [],
                'ankle_angle_r': [],
                'ankle_angle_l': []
            }
            
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
                        for joint, idx in col_indices.items():
                            if joint != 'time':
                                joint_data[joint].append(float(values[idx]))
            
            # Convert lists to numpy arrays
            self._time = np.array(time_data)
            for joint in joint_data:
                joint_data[joint] = np.array(joint_data[joint])
            
            return {
                'time': self._time,
                'joint_data': joint_data
            }
            
        except Exception as e:
            print(f"Error reading .mot file: {str(e)}")
            return None

    def read_csv_file(self, file_path):
        """
        Read a CSV file containing motion capture data
        
        Args:
            file_path (str): Path to the CSV file
            
        Returns:
            dict: Dictionary containing time, joint_data, and gait_phase information
        """
        try:
            import pandas as pd
            
            # Read the CSV file
            df = pd.read_csv(file_path)
            
            # Extract time values
            time_values = df['time'].values.tolist()
            
            # Create a dictionary for joint data
            joint_data = {
                'hip_flexion_r': df['right_hip'].values.tolist() if 'right_hip' in df else [],
                'hip_flexion_l': df['left_hip'].values.tolist() if 'left_hip' in df else [],
                'knee_angle_r': df['right_knee'].values.tolist() if 'right_knee' in df else [],
                'knee_angle_l': df['left_knee'].values.tolist() if 'left_knee' in df else [],
                'ankle_angle_r': df['right_ankle'].values.tolist() if 'right_ankle' in df else [],
                'ankle_angle_l': df['left_ankle'].values.tolist() if 'left_ankle' in df else []
            }
            
            # Extract gait phase data if available
            gait_phase_data = None
            if 'gait_phase' in df:
                gait_phase_data = df['gait_phase'].values.tolist()
                
            # Extract cycle data if available
            cycle_data = {}
            if 'cycle_number' in df:
                cycle_data['cycle_number'] = df['cycle_number'].values.tolist()
            if 'cycle_boundary' in df:
                cycle_data['cycle_boundary'] = df['cycle_boundary'].values.tolist()
            
            # Return the data as a dictionary
            result = {
                'time': time_values,
                'joint_data': joint_data
            }
            
            # Add gait phase data if available
            if gait_phase_data is not None:
                result['gait_phase'] = gait_phase_data
                
            # Add cycle data if available
            if cycle_data:
                result['cycle_data'] = cycle_data
                
            return result
        
        except Exception as e:
            print(f"Error reading CSV file: {str(e)}")
            return None

    def get_data(self):
        """
        Returns the currently loaded data.
        
        Returns:
            dict: Dictionary containing time series and joint angle data
        """
        if self._time is None:
            return None
            
        return {
            'time': self._time,
            'joint_data': self._joint_data
        }