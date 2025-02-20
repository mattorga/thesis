import numpy as np

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