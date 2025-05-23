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
    left_hip: float
    right_hip: float
    left_knee: float
    right_knee: float
    left_ankle: float = 0
    right_ankle: float = 0
    
    def __post_init__(self):
        # Store original angles
        self.orig_left_hip = self.left_hip
        self.orig_right_hip = self.right_hip
        self.orig_left_knee = self.left_knee
        self.orig_right_knee = self.right_knee
        self.orig_left_ankle = self.left_ankle
        self.orig_right_ankle = self.right_ankle
        
        # Apply sign convention as per paper for calculation
        self.left_hip = -abs(self.left_hip)
        self.right_hip = abs(self.right_hip)
        self.left_knee = -abs(self.left_knee)
        self.right_knee = abs(self.right_knee)
        self.left_ankle = -abs(self.left_ankle)
        self.right_ankle = abs(self.right_ankle)
        
    def as_array(self) -> np.ndarray:
        return np.array([self.left_hip, self.right_hip, 
                        self.left_knee, self.right_knee,
                        self.left_ankle, self.right_ankle])
    
    def get_original_angles(self) -> Dict[str, float]:
        """Return original angles as a dictionary"""
        return {
            'left_hip': self.orig_left_hip,
            'right_hip': self.orig_right_hip,
            'left_knee': self.orig_left_knee,
            'right_knee': self.orig_right_knee,
            'left_ankle': self.orig_left_ankle,
            'right_ankle': self.orig_right_ankle
        }
    
    def get_inverted_angles(self) -> Dict[str, float]:
        """Return inverted angles as a dictionary"""
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
        
    def calculate_deviation_distances(self, angles: List[JointAngles]) -> np.ndarray:
        """Calculate deviation distances between consecutive poses"""
        angles_array = np.array([angle.as_array() for angle in angles])
        diff = np.diff(angles_array, axis=0)
        # Add difference between last and first pose for cyclic nature
        diff = np.vstack([diff, angles_array[0] - angles_array[-1]])
        distances = np.sqrt(np.sum(diff**2, axis=1))
        return distances
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
        """Find optimal threshold using iterative Fisher's discriminant with manual adjustment"""
        # Initial calculation using Fisher's method
        threshold = np.mean(distances)  # Initial guess
        prev_threshold = float('inf')
        iteration = 0
        
        while (abs(threshold - prev_threshold) > self.convergence_threshold and 
            iteration < self.max_iterations):
            prev_threshold = threshold
            
            # Calculate scatter matrices
            s_w, s_b = self.calculate_scatter_matrices(distances, threshold)
            
            if s_w == 0:
                break
                
            # Update threshold based on means of resulting classes
            high_class = distances[distances >= threshold]
            low_class = distances[distances < threshold]
            
            if len(high_class) > 0 and len(low_class) > 0:
                threshold = (np.mean(high_class) + np.mean(low_class)) / 2
                
            iteration += 1
        
        # Manual sensitivity adjustment - decrease threshold to detect more transitions
        # Adjust this factor based on your data (0.8-0.9 for more sensitivity)
        sensitivity_factor = 0.85
        adjusted_threshold = threshold * sensitivity_factor
        
        return adjusted_threshold
        
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
        
    def classify_gait_phases(self, angles: List[JointAngles]) -> List[GaitPhase]:
        """Classify gait phases using Fisher's discriminant for the entire dataset"""
        # Initialize with default phase
        phases = [GaitPhase.MID_LEFT_SWING] * len(angles)
        
        # Calculate deviation distances for the entire dataset
        distances = self.calculate_deviation_distances(angles)
        
        # Find optimal threshold using Fisher's discriminant
        threshold = self.optimize_threshold(distances)
        
        # Classify high/low activity regions for the entire dataset
        high_activity = distances >= threshold
        
        # Determine phase sequence based on high/low activity pattern
        prev_phase = None
        
        for i, is_high in enumerate(high_activity):
            current_phase = None
            
            if is_high:
                if prev_phase in [None, GaitPhase.DOUBLE_STANCE_2]:
                    current_phase = GaitPhase.INIT_LEFT_SWING
                elif prev_phase == GaitPhase.MID_LEFT_SWING:
                    current_phase = GaitPhase.TERM_LEFT_SWING
                elif prev_phase == GaitPhase.DOUBLE_STANCE_1:
                    current_phase = GaitPhase.INIT_RIGHT_SWING
                elif prev_phase == GaitPhase.MID_RIGHT_SWING:
                    current_phase = GaitPhase.TERM_RIGHT_SWING
            else:
                if prev_phase == GaitPhase.INIT_LEFT_SWING:
                    current_phase = GaitPhase.MID_LEFT_SWING
                elif prev_phase == GaitPhase.TERM_LEFT_SWING:
                    current_phase = GaitPhase.DOUBLE_STANCE_1
                elif prev_phase == GaitPhase.INIT_RIGHT_SWING:
                    current_phase = GaitPhase.MID_RIGHT_SWING
                elif prev_phase == GaitPhase.TERM_RIGHT_SWING:
                    current_phase = GaitPhase.DOUBLE_STANCE_2
                    
            if current_phase is None:
                current_phase = prev_phase or GaitPhase.MID_LEFT_SWING
                
            phases[i] = current_phase
            prev_phase = current_phase
                
        return phases

    def write_results_to_csv(self, result: Dict[str, List], output_file: str, time_data: pd.Series = None):
        """Write classification results to CSV files in separate folders for inverted and original angles"""
        # Get the base filename without extension
        output_base = os.path.basename(os.path.splitext(output_file)[0])
        
        # Get the directory path
        base_dir = os.path.dirname(output_file)
        
        # Define output file paths
        output_inverted = os.path.join(base_dir, f"{output_base}_inverted.csv")
        output_original = os.path.join(base_dir, f"{output_base}_original.csv")
        
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

    def process_mot_file(self, input_file: str, output_file: str = None) -> Dict[str, List]:
        """Process a MOT file, classify gait phases and visualize the threshold
        
        This method loads joint angles from a MOT file, calculates deviation distances,
        optimizes threshold, classifies gait phases, and generates visualizations and 
        CSV output files.
        
        Args:
            input_file: Path to the input MOT file
            output_file: Optional path for output files (CSV and visualization)
            
        Returns:
            Dictionary containing angles, gait phases, distances, and threshold
        """
        # We'll extract time data directly from the MOT file when parsing it
        time_data = None
        
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
        if 'time' in data.columns:
            time_data = data['time']
        
        required_columns = ['hip_flexion_l', 'hip_flexion_r', 
                        'knee_angle_l', 'knee_angle_r',
                        'ankle_angle_l', 'ankle_angle_r']
        
        # Verify all required columns exist
        missing_cols = [col for col in required_columns if col not in data.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns in MOT file: {missing_cols}")
        
        # Convert each row to JointAngles
        angles = []
        for _, row in data.iterrows():
            angles.append(JointAngles(
                left_hip=float(row['hip_flexion_l']),
                right_hip=float(row['hip_flexion_r']),
                left_knee=float(row['knee_angle_l']),
                right_knee=float(row['knee_angle_r']),
                left_ankle=float(row['ankle_angle_l']),
                right_ankle=float(row['ankle_angle_r'])
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
        
        # Handle output if specified
        if output_file:
            # Create visualization 
            output_base = os.path.splitext(output_file)[0]
            viz_output = f"{output_base}_threshold_visualization.png"
            
            # Generate and save visualization with phases
            self.add_threshold_visualization(distances, threshold, phases, viz_output)
            
            # Get the base filename without extension
            output_base = os.path.basename(os.path.splitext(output_file)[0])
            
            # Get the directory path
            base_dir = os.path.dirname(output_file)
            
            # Define output file paths
            output_inverted = os.path.join(base_dir, f"{output_base}_inverted.csv")
            output_original = os.path.join(base_dir, f"{output_base}_original.csv")
            
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
        
        return result

def gait_classification(trial_path):
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
    
    # Use the first .mot file found (or implement logic to choose a specific one)
    input_file = os.path.join(kinematics_dir, mot_files[0])
    
    # Extract the base filename without extension to use for output files
    input_base_name = os.path.splitext(os.path.basename(input_file))[0]
    input_base_name = input_base_name.split('_')[0]
    
    # Create gait-classification directory in the trial path
    output_dir = os.path.join(trial_path, "gait-classification")
    os.makedirs(output_dir, exist_ok=True)
    
    # Set up output files in the gait-classification directory
    results_file = os.path.join(output_dir, f"{input_base_name}_classification.csv")
    
    try:
        # Process the file with visualization
        result = classifier.process_mot_file(input_file, results_file)
        
        print(f"Classification complete. Results saved to {results_file}")
        print(f"Threshold visualization saved at: {os.path.splitext(results_file)[0]}_threshold_visualization.png")
        
    except Exception as e:
        print(f"Error processing {os.path.basename(input_file)}: {str(e)}")