import numpy as np
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Dict
import pandas as pd
import os
import matplotlib.pyplot as plt


class GaitPhase(Enum):
    INIT_LEFT_SWING = "Initial-LSw"
    MID_LEFT_SWING = "Mid-LSw" 
    TERM_LEFT_SWING = "Term-LSw"
    DOUBLE_STANCE_1 = "DSt1"
    INIT_RIGHT_SWING = "Initial-RSw"
    MID_RIGHT_SWING = "Mid-RSw"
    TERM_RIGHT_SWING = "Term-RSw"
    DOUBLE_STANCE_2 = "DSt2"

@dataclass
class JointAngles:
    def __init__(self, left_hip, right_hip, left_knee, right_knee, left_ankle=0, right_ankle=0):
        # Store original angles
        self.orig_left_hip = left_hip
        self.orig_right_hip = right_hip
        self.orig_left_knee = left_knee
        self.orig_right_knee = right_knee
        self.orig_left_ankle = left_ankle
        self.orig_right_ankle = right_ankle
        
        # Apply sign convention as per paper (Figure 1)
        # Make left angles negative and right angles positive
        self.left_hip = -abs(left_hip)
        self.right_hip = abs(right_hip)
        self.left_knee = -abs(left_knee)
        self.right_knee = abs(right_knee)
        self.left_ankle = -abs(left_ankle)
        self.right_ankle = abs(right_ankle)
    
    def as_array(self) -> np.ndarray:
        """Return angles as a numpy array for calculations, excluding ankle angles as per paper"""
        return np.array([self.left_hip, self.right_hip, 
                         self.left_knee, self.right_knee])
    
    def get_original_angles(self) -> Dict[str, float]:
        """Return original angles as a dictionary for output"""
        return {
            'left_hip': self.orig_left_hip,
            'right_hip': self.orig_right_hip,
            'left_knee': self.orig_left_knee,
            'right_knee': self.orig_right_knee,
            'left_ankle': self.orig_left_ankle,
            'right_ankle': self.orig_right_ankle
        }
    
    def get_inverted_angles(self) -> Dict[str, float]:
        """Return inverted angles as a dictionary for output"""
        return {
            'left_hip': self.left_hip,
            'right_hip': self.right_hip,
            'left_knee': self.left_knee,
            'right_knee': self.right_knee,
            'left_ankle': self.left_ankle,
            'right_ankle': self.right_ankle
        }
    
class GaitClassifier:
    def __init__(self, convergence_threshold: float = 1e-6, max_iterations: int = 100):
        self.convergence_threshold = convergence_threshold
        self.max_iterations = max_iterations
    
    def calculate_posture_deviation(self, angles: JointAngles) -> float:
        """
        Calculate posture deviation degree from standard standing as per equation 1 in the paper.
        
        In standard standing, all joint angles are defined as 0°.
        
        Args:
            angles: JointAngles object containing hip and knee joint angles
            
        Returns:
            Scalar value representing posture deviation degree
        """
        # Extract angles as array
        theta = angles.as_array()
        
        # Calculate posture deviation as per equation 1
        # y_pd = sqrt(sum((θ_i - θ_iss)^2)), where θ_iss = 0
        # This simplifies to: y_pd = sqrt(sum(θ_i^2))
        y_pd = np.sqrt(np.sum(theta**2))
        
        return y_pd
        
    def calculate_deviation_distances(self, angles: List[JointAngles]) -> np.ndarray:
        """
        Calculate deviation distances between consecutive poses as per equation 4 in the paper.
        
        Args:
            angles: List of JointAngles objects
            
        Returns:
            Array of deviation distances
        """
        # Convert angles to array for easier calculation
        angles_array = np.array([angle.as_array() for angle in angles])
        
        # Calculate difference between consecutive poses
        # For the first point, calculate difference from the last point to complete the cycle
        distances = []
        for j in range(len(angles)):
            if j == 0:
                # For first point, reference the last point (as in equation 4)
                diff = angles_array[0] - angles_array[-1]
            else:
                diff = angles_array[j] - angles_array[j-1]
            
            # Calculate Euclidean distance as in equation 4
            distance = np.sqrt(np.sum(diff**2))
            distances.append(distance)
        
        return np.array(distances)
    
    def divide_gait_cycles(self, angles_list: List[JointAngles]) -> List[List[JointAngles]]:
        """
        Divide a sequence of joint angles into gait cycles based on 
        minimal deviations from standard standing, as described in Section 2.1.1 of the paper.
        
        According to the paper: "the posture with the minimal lower-limb deviations from 
        standard standing is at the beginning of the gait cycle, and the same posture 
        that appears again is as the end."
        
        Args:
            angles_list: List of JointAngles objects
            
        Returns:
            List of lists, where each inner list represents one gait cycle
        """
        # Calculate posture deviation for each time point using equation 1
        deviations = [self.calculate_posture_deviation(angles) for angles in angles_list]
        
        # Find the global minimum of deviation as the reference posture
        # This is the posture most similar to standard standing
        cycles = []
        current_cycle_start = 0
        
        # Process the whole sequence to find complete gait cycles
        i = 1
        while i < len(deviations) - 1:
            # Find local minima of deviations
            if deviations[i] < deviations[i-1] and deviations[i] < deviations[i+1]:
                # If we already have a starting point and found another minimum,
                # this could be the end of a cycle
                if current_cycle_start != i:
                    # Extract the cycle from start to current position
                    cycle = angles_list[current_cycle_start:i+1]
                    cycles.append(cycle)
                    
                    # Update the cycle start point
                    current_cycle_start = i+1
            
            i += 1
        
        # If no cycles were identified, return the entire sequence as one cycle
        if not cycles:
            return [angles_list]
        
        return cycles
    
    def calculate_scatter_matrices(self, distances: np.ndarray, threshold: float) -> Tuple[float, float]:
        """Calculate within-class and between-class scatter matrices"""
        class1 = distances[distances >= threshold]
        class2 = distances[distances < threshold]
        
        if len(class1) == 0 or len(class2) == 0:
            return float('inf'), 0
            
        mean1 = np.mean(class1)
        mean2 = np.mean(class2)
        overall_mean = np.mean(distances)
        
        # Within-class scatter
        s_w = np.sum((class1 - mean1)**2) + np.sum((class2 - mean2)**2)
        
        # Between-class scatter
        s_b = (len(class1)*(mean1 - overall_mean)**2 + 
               len(class2)*(mean2 - overall_mean)**2)
               
        return s_w, s_b
    
    def optimize_threshold(self, distances: np.ndarray) -> float:
        """
        Find optimal threshold using Fisher's linear discriminant as described in
        Section 2.1.3 and equations 8-14 of the paper.
        
        The paper describes an iterative process:
        1. Set an initial threshold Q
        2. Classify data into two classes based on Q
        3. Calculate means of the two classes
        4. Update Q based on the means
        5. Repeat until Q is stable
        
        Args:
            distances: Array of deviation distances between consecutive poses
                
        Returns:
            Optimal threshold Q_c for classifying high/low activity
        """
        # Initialize with mean as starting threshold
        Q = np.mean(distances)
        max_J = float('-inf')
        optimal_Q = Q
        prev_Q = None
        
        # Iterative process to find optimal Q_c as described in Section 2.1.3
        while prev_Q is None or Q != prev_Q:  # Exact match required for convergence
            prev_Q = Q
            
            # Classify according to equation 8
            class_I = distances[distances >= Q]
            class_II = distances[distances < Q]
            
            # Check if either class is empty
            if len(class_I) == 0 or len(class_II) == 0:
                break
            
            # Calculate mean values according to equation 9
            mu_I = np.mean(class_I)
            mu_II = np.mean(class_II)
            
            # Calculate overall population mean according to equation 10
            mu = np.mean(distances)
            
            # Calculate within-class scatter according to equation 11
            S_w = np.sum((class_I - mu_I)**2) + np.sum((class_II - mu_II)**2)
            
            # Calculate between-class scatter according to equation 12
            S_b = len(class_I) * (mu_I - mu)**2 + len(class_II) * (mu_II - mu)**2
            
            # Check if S_w is zero to avoid division by zero
            if S_w == 0:
                break
            
            # Evaluation function J(w_p) as per equation 13
            J = S_b / S_w
            
            # Keep track of the Q that maximizes J as per equation 14
            if J > max_J:
                max_J = J
                optimal_Q = Q
            
            # Reclassify based on current Q and update Q to midpoint between class means
            Q = (mu_I + mu_II) / 2
        
        # Return optimal threshold Q_c as per equation 14
        # This is the Q that maximizes the evaluation function J
        return optimal_Q
    
    def classify_gait_phases(self, angles: List[JointAngles]) -> List[GaitPhase]:
        """
        Classify gait phases using the methodology described in Section 2.1 of the paper.
        
        Args:
            angles: List of JointAngles objects
            
        Returns:
            List of GaitPhase classifications for each pose
        """
        # Calculate deviation distances for the entire dataset as per equation 4
        distances = self.calculate_deviation_distances(angles)
        
        # Find optimal threshold using Fisher's discriminant as per equations 8-14
        threshold = self.optimize_threshold(distances)
        
        # Classify into two main classes: high activity and low activity
        # The high activity regions according to the paper include:
        # init-LSw, term-LSw, init-RSw, term-RSw
        # The low activity regions include:
        # mid-LSw, DSt1, mid-RSw, DSt2
        is_high_activity = distances >= threshold
        
        # Find transitions between high and low activity
        transitions = []
        for i in range(1, len(is_high_activity)):
            if is_high_activity[i] != is_high_activity[i-1]:
                transitions.append(i)
        
        # According to the paper, a single gait cycle should naturally yield 8 phases
        # If we don't have exactly 8 regions, we need to handle this situation
        # The paper doesn't explicitly discuss this, but we'll attempt to handle it gracefully
        
        # If there are less than 2 transitions, we can't properly segment the data
        if len(transitions) < 2:
            # Default to most common phase
            return [GaitPhase.INIT_LEFT_SWING] * len(angles)
        
        # Create regions based on transitions
        regions = []
        start_idx = 0
        
        for t in transitions:
            regions.append((start_idx, t))
            start_idx = t
        
        # Add the final region
        regions.append((start_idx, len(angles)))
        
        # According to the paper, the 8 phases should naturally emerge from the data
        # But if we don't have 8 regions, we need to adapt
        
        # If we don't have exactly 8 regions, we need to map them to the expected 8 phases
        # This attempts to preserve the natural boundaries in the data rather than forcing exactly 8 regions
        
        # Determine the activity level of each region
        region_activities = [is_high_activity[r[0]] for r in regions]
        
        # Initialize phase assignments
        phases = [None] * len(angles)
        
        # Expected pattern of activities for the 8 phases based on the paper:
        # HIGH (init-LSw), LOW (mid-LSw), HIGH (term-LSw), LOW (DSt1),
        # HIGH (init-RSw), LOW (mid-RSw), HIGH (term-RSw), LOW (DSt2)
        expected_pattern = [True, False, True, False, True, False, True, False]
        
        # If we have exactly 8 regions with the expected pattern, assign phases accordingly
        if len(regions) == 8 and region_activities[0] == expected_pattern[0]:
            phase_order = [
                GaitPhase.INIT_LEFT_SWING,
                GaitPhase.MID_LEFT_SWING,
                GaitPhase.TERM_LEFT_SWING,
                GaitPhase.DOUBLE_STANCE_1,
                GaitPhase.INIT_RIGHT_SWING,
                GaitPhase.MID_RIGHT_SWING,
                GaitPhase.TERM_RIGHT_SWING,
                GaitPhase.DOUBLE_STANCE_2
            ]
            
            for i, (start, end) in enumerate(regions):
                phase = phase_order[i]
                for j in range(start, end):
                    phases[j] = phase
        
        # If we have a different number of regions or the pattern doesn't match,
        # we need to adapt while preserving the natural transitions in the data
        else:
            # Identify high activity regions as swing phases and low activity regions as stance phases
            # Then, try to assign specific phases based on their position in the sequence
            
            # Phase assignments for high and low activity regions
            high_phases = [
                GaitPhase.INIT_LEFT_SWING,
                GaitPhase.TERM_LEFT_SWING,
                GaitPhase.INIT_RIGHT_SWING,
                GaitPhase.TERM_RIGHT_SWING
            ]
            
            low_phases = [
                GaitPhase.MID_LEFT_SWING,
                GaitPhase.DOUBLE_STANCE_1,
                GaitPhase.MID_RIGHT_SWING,
                GaitPhase.DOUBLE_STANCE_2
            ]
            
            high_count = 0
            low_count = 0
            
            for i, (start, end) in enumerate(regions):
                if region_activities[i]:
                    # High activity region
                    phase = high_phases[high_count % len(high_phases)]
                    high_count += 1
                else:
                    # Low activity region
                    phase = low_phases[low_count % len(low_phases)]
                    low_count += 1
                
                # Assign phase to all frames in the region
                for j in range(start, end):
                    phases[j] = phase
        
        return phases
    
    def add_threshold_visualization(self, distances, threshold, phases=None, output_file=None):
        """
        Visualize the deviation distances, threshold, and gait phases.
        
        Args:
            distances: Numpy array of deviation distances
            threshold: The Q threshold used for classification
            phases: Optional list of GaitPhase values corresponding to each frame
            output_file: Optional file path to save the plot
        """
        plt.figure(figsize=(14, 8))
        
        # Create two subplots - one for distances, one for phases
        if phases is not None:
            gs = plt.GridSpec(2, 1, height_ratios=[3, 1])
            ax1 = plt.subplot(gs[0])
            ax2 = plt.subplot(gs[1], sharex=ax1)
        else:
            ax1 = plt.gca()
        
        # Plot distances on the first subplot
        ax1.plot(distances, 'b-', label='Deviation Distances')
        
        # Plot threshold
        ax1.axhline(y=threshold, color='r', linestyle='--', label=f'Q Threshold: {threshold:.4f}')
        
        # Highlight high activity regions
        high_activity = distances >= threshold
        ax1.fill_between(range(len(distances)), 0, distances, 
                        where=high_activity, 
                        alpha=0.3, color='orange', 
                        label='High Activity Regions')
        
        # Add labels and legend
        ax1.set_ylabel('Deviation Distance')
        ax1.set_title('Gait Phase Deviation Distances with Q Threshold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # If phases are provided, plot them on the second subplot
        if phases is not None:
            # Convert phases to numeric values for visualization
            phase_dict = {phase: i for i, phase in enumerate(GaitPhase)}
            numeric_phases = [phase_dict[phase] for phase in phases]
            
            # Plot phases
            ax2.plot(numeric_phases, 'g-', linewidth=2)
            
            # Add markers for phase changes
            phase_changes = [i for i in range(1, len(phases)) if phases[i] != phases[i-1]]
            if phase_changes:
                ax2.plot(phase_changes, [numeric_phases[i] for i in phase_changes], 'ro', markersize=4)
            
            # Set y-ticks to match phase names
            ax2.set_yticks(list(range(len(GaitPhase))))
            ax2.set_yticklabels([phase.value for phase in GaitPhase])
            ax2.set_ylim(-0.5, len(GaitPhase) - 0.5)
            
            # Add grid and labels
            ax2.grid(True, axis='y', alpha=0.3)
            ax2.set_xlabel('Frame Index')
            ax2.set_ylabel('Gait Phase')
        else:
            ax1.set_xlabel('Frame Index')
        
        plt.tight_layout()
        
        # Save if output file provided
        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            
        return plt.gcf()
    
    def write_results_to_csv(self, result: Dict[str, List], output_file: str, time_data: pd.Series = None):
        """Write classification results to CSV files in separate folders for inverted and original angles"""
        # Get the base filename without extension
        output_base = os.path.basename(os.path.splitext(output_file)[0])
        
        # Get the directory path
        base_dir = os.path.dirname(output_file)
        
        # Define output file paths
        output_inverted = os.path.join(base_dir, f"{output_base}_paper_inverted.csv")
        output_original = os.path.join(base_dir, f"{output_base}_paper_original.csv")
        
        # Create rows for both CSVs
        inverted_rows = []
        original_rows = []
        
        for i, (angles, phase) in enumerate(zip(result['angles'], result['gait_phases'])):
            # Common data
            common_data = {
                'time': time_data.iloc[i] if time_data is not None else i/100.0,
                'gait_phase': phase.value
            }
            
            # Create row with inverted angles
            inverted_row = common_data.copy()
            inverted_row.update(angles.get_inverted_angles())
            inverted_rows.append(inverted_row)
            
            # Create row with original angles
            original_row = common_data.copy()
            original_row.update(angles.get_original_angles())
            original_rows.append(original_row)
            
        # Write to two separate CSV files
        inverted_df = pd.DataFrame(inverted_rows)
        inverted_df.to_csv(output_inverted, index=False, float_format='%.6f')
        
        original_df = pd.DataFrame(original_rows)
        original_df.to_csv(output_original, index=False, float_format='%.6f')
    
    def process_mot_file(self, input_file: str, output_dir: str = None) -> Dict[str, List]:
        """
        Process a MOT file to extract joint angles and classify gait phases.
        
        Args:
            input_file: Path to the input MOT file
            output_dir: Optional directory path for output files
                
        Returns:
            Dictionary containing angles, gait phases, distances, and threshold
        """
        # Load joint angles from MOT file
        with open(input_file, 'r') as f:
            lines = f.readlines()

        # Parse header
        data_start = 0
        for i, line in enumerate(lines):
            if line.startswith('endheader'):
                data_start = i + 1
                break
        
        # Get column names
        column_names = lines[data_start].strip().split('\t')
        
        # Read data
        data_lines = [line.strip().split('\t') for line in lines[data_start+1:]]
        data = pd.DataFrame(data_lines, columns=column_names)
        
        # Convert numeric columns to float
        for col in data.columns:
            try:
                data[col] = data[col].astype(float)
            except:
                continue
                
        # Extract time data if available in the MOT file
        time_data = None
        if 'time' in data.columns:
            time_data = data['time']
        
        # Check for required columns
        required_columns = ['hip_flexion_l', 'hip_flexion_r', 
                        'knee_angle_l', 'knee_angle_r']
        
        # Verify all required columns exist
        missing_cols = [col for col in required_columns if col not in data.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns in MOT file: {missing_cols}")
        
        # Optional ankle columns
        ankle_columns = ['ankle_angle_l', 'ankle_angle_r']
        has_ankle_data = all(col in data.columns for col in ankle_columns)
        
        # Convert each row to JointAngles
        angles = []
        for _, row in data.iterrows():
            if has_ankle_data:
                angles.append(JointAngles(
                    left_hip=float(row['hip_flexion_l']),
                    right_hip=float(row['hip_flexion_r']),
                    left_knee=float(row['knee_angle_l']),
                    right_knee=float(row['knee_angle_r']),
                    left_ankle=float(row['ankle_angle_l']),
                    right_ankle=float(row['ankle_angle_r'])
                ))
            else:
                angles.append(JointAngles(
                    left_hip=float(row['hip_flexion_l']),
                    right_hip=float(row['hip_flexion_r']),
                    left_knee=float(row['knee_angle_l']),
                    right_knee=float(row['knee_angle_r'])
                ))
        
        # Calculate distances
        distances = self.calculate_deviation_distances(angles)
        
        # Find optimal threshold
        threshold = self.optimize_threshold(distances)
        
        # Classify gait phases
        phases = self.classify_gait_phases(angles)
        
        # Create result dictionary
        result = {
            'angles': angles,
            'gait_phases': phases,
            'distances': distances,
            'threshold': threshold
        }
        
        # Handle output if directory specified
        if output_dir:
            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            # Define output file paths with fixed names
            output_inverted = os.path.join(output_dir, "joint_paper_inverted.csv")
            output_original = os.path.join(output_dir, "joint_paper_original.csv")
            viz_output = os.path.join(output_dir, "visualization.png")
            
            # Create rows for both CSVs
            inverted_rows = []
            original_rows = []
            
            for i, (angle, phase) in enumerate(zip(result['angles'], result['gait_phases'])):
                # Common data
                common_data = {
                    'time': time_data.iloc[i] if time_data is not None else i/100.0,
                    'gait_phase': phase.value
                }
                
                # Create row with inverted angles
                inverted_row = common_data.copy()
                inverted_row.update(angle.get_inverted_angles())
                inverted_rows.append(inverted_row)
                
                # Create row with original angles
                original_row = common_data.copy()
                original_row.update(angle.get_original_angles())
                original_rows.append(original_row)
                
            # Write to two separate CSV files
            inverted_df = pd.DataFrame(inverted_rows)
            inverted_df.to_csv(output_inverted, index=False, float_format='%.6f')
            
            original_df = pd.DataFrame(original_rows)
            original_df.to_csv(output_original, index=False, float_format='%.6f')
            
            # Generate and save visualization
            self.add_threshold_visualization(distances, threshold, phases, viz_output)
        
        return result


def gait_classification(trial_path):
    """
    Main function to process a trial directory and classify gait phases.
    
    Args:
        trial_path: Path to the trial directory containing kinematics data
    """
    # Initialize classifier
    classifier = GaitClassifier()
    
    # Find the .mot file in the kinematics folder
    kinematics_dir = os.path.join(trial_path, "kinematics")
    
    if not os.path.exists(kinematics_dir):
        print(f"Error: Kinematics directory not found at {kinematics_dir}")
        return
    
    # Look for .mot files in the kinematics directory
    mot_files = [f for f in os.listdir(kinematics_dir) if f.endswith(".mot")]
    
    if not mot_files:
        print(f"Error: No .mot files found in {kinematics_dir}")
        return
    
    # Use the first .mot file found
    input_file = os.path.join(kinematics_dir, mot_files[0])
    
    # Create gait-classification directory in the trial path
    output_dir = os.path.join(trial_path, "gait-classification-paper")
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Process the file, outputting to the gait-classification directory
        result = classifier.process_mot_file(input_file, output_dir)
        
        print(f"Classification complete. Results saved to {output_dir}")
        print(f"  - Joint angles (inverted): {os.path.join(output_dir, 'joint_inverted.csv')}")
        print(f"  - Joint angles (original): {os.path.join(output_dir, 'joint_origina.csv')}")
        print(f"  - Visualization: {os.path.join(output_dir, 'visualization.png')}")
        
    except Exception as e:
        print(f"Error processing {os.path.basename(input_file)}: {str(e)}")