import os
import pandas as pd
import numpy as np
from scipy import signal
from scipy.stats import pearsonr
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt
import re

# Columns to skip in the analysis
skip_cols = [14, 22, 44, 45, 46, 47, 48, 53, 54, 60, 61]
#skip_cols = []

def load_mot_file(file_path):
    """
    Load .mot file and return numpy array of data
    """
    # Read the file and find endheader
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Find header index
    header_idx = next(i for i, line in enumerate(lines) if "endheader" in line) + 1
    
    # Convert to dataframe and then numpy array
    df = pd.read_csv(file_path, delim_whitespace=True, skiprows=header_idx)
    return df.to_numpy()

def scalar_distance(a, b):
    return abs(a - b)

def analyze_gait_patterns(before_data, after_data):
    """
    Analyze gait patterns using FastDTW and Cross-correlation
    """
    # Get minimum length
    min_length = min(len(before_data), len(after_data))
    
    # Trim data to same length
    before_data = before_data[:min_length]
    after_data = after_data[:min_length]
    
    # Initialize results containers
    num_features = before_data.shape[1]
    dtw_distances = np.zeros(num_features)
    cross_corr_max = np.zeros(num_features)
    cross_corr_lags = np.zeros(num_features)
    pearson_corr = np.zeros(num_features)
    p_values = np.zeros(num_features)
    
    # Analyze each column (skip time column)
    for col in range(1, num_features):  # Start from 1 to skip time column
        if col in skip_cols:
            continue
        # Extract sequences
        seq1 = before_data[:, col]
        seq2 = after_data[:, col]
        
        # Normalize sequences (z score norm)
        seq1_norm = (seq1 - np.mean(seq1)) / (np.std(seq1) + 1e-10)
        seq2_norm = (seq2 - np.mean(seq2)) / (np.std(seq2) + 1e-10)

        try:
            # FastDTW distance
            distance, path = fastdtw(seq1_norm, seq2_norm, dist=scalar_distance)
            dtw_distances[col] = distance
            
            # Cross-correlation
            cross_corr = signal.correlate(seq1_norm, seq2_norm, mode='full')
            lags = signal.correlation_lags(len(seq1_norm), len(seq2_norm), mode='full')
            # Normalize the cross-correlation
            norm_factor = np.sqrt(np.sum(seq1_norm**2) * np.sum(seq2_norm**2))
            normalized_cross_corr = cross_corr / norm_factor

            # Get maximum correlation and corresponding lag
            max_idx = np.argmax(np.abs(normalized_cross_corr))
            cross_corr_max[col] = normalized_cross_corr[max_idx]
            cross_corr_lags[col] = lags[max_idx]
            
            # Pearson correlation
            r, p = pearsonr(seq1_norm, seq2_norm)
            pearson_corr[col] = r
            p_values[col] = p
            
        except Exception as e:
            print(f"Error processing column {col}: {str(e)}")
            dtw_distances[col] = np.nan
            cross_corr_max[col] = np.nan
            cross_corr_lags[col] = np.nan
            pearson_corr[col] = np.nan
            p_values[col] = np.nan
    
    return {
        'dtw_distances': dtw_distances,
        'cross_corr_max': cross_corr_max,
        'cross_corr_lags': cross_corr_lags,
        'pearson_corr': pearson_corr,
        'p_values': p_values
    }

def print_analysis_results_to_file(results, trial1_info, trial2_info, filename):
    """
    Print the analysis results to a file with trial information
    """
    # Define columns to skip: time column (0) plus extra columns
    skip_cols_output = [0, 14, 22, 44, 45, 46, 47, 48, 53, 54, 55, 60, 61, 62]

    with open(filename, "w") as f:
        # Write header with trial information
        f.write(f"Gait Analysis Comparison: {trial1_info} vs {trial2_info}\n")
        f.write("-" * 100 + "\n")
        f.write(f"{'Column':^8} {'DTW Dist':^12} {'Cross-Corr':^12} {'Time Lag':^10} {'Pearson r':^12} {'P-value':^12}\n")
        f.write("-" * 100 + "\n")
        
        # Create lists to store values of included columns for averaging
        valid_dtw = []
        valid_cross_corr = []
        valid_pearson = []
        
        # Loop through each column and skip specified columns
        for col in range(len(results['dtw_distances'])):
            if col in skip_cols_output:
                continue
                
            dtw_dist = results['dtw_distances'][col]
            cross_corr = results['cross_corr_max'][col]
            time_lag = results['cross_corr_lags'][col]
            pearson = results['pearson_corr'][col]
            p_val = results['p_values'][col]
            
            # Collect values for averaging (only from non-skipped columns)
            if not np.isnan(dtw_dist):
                valid_dtw.append(dtw_dist)
            if not np.isnan(cross_corr):
                valid_cross_corr.append(cross_corr)
            if not np.isnan(pearson):
                valid_pearson.append(pearson)
            
            # Write the formatted results for this column
            f.write(f"{col:^8d} {dtw_dist:^12.4f} {cross_corr:^12.4f} {time_lag:^10.0f} "
                    f"{pearson:^12.4f} {p_val:^12.4f}\n")
        
        # Write summary statistics using only the included columns
        f.write("\nSummary Statistics:\n")
        f.write(f"Average DTW distance: {np.mean(valid_dtw):.4f}\n")
        f.write(f"Average cross-correlation: {np.mean(valid_cross_corr):.4f}\n")
        f.write(f"Average Pearson correlation: {np.mean(valid_pearson):.4f}\n")
    
def extract_condition_from_folder(folder_name):
    """
    Extract the condition (antalgic/normal) and speed from a folder name
    """
    # Use regex to extract condition and speed
    match = re.search(r'T\d+_(\w+)_(\d+\.\d+)', folder_name)
    if match:
        condition = match.group(1)
        speed = match.group(2)
        return f"{condition}_{speed}"
    return folder_name  # Return the original name if pattern not found

def find_mot_file_in_kinematics(kinematics_path):
    """
    Find the first .mot file in the kinematics folder that contains 'butterworth_on_speed'
    """
    if not os.path.exists(kinematics_path):
        return None
    
    for file in os.listdir(kinematics_path):
        if file.endswith('.mot') and 'filt_butterworth_on_speed' in file:
            return os.path.join(kinematics_path, file)
    
    # If no file with the specific pattern is found, return the first .mot file
    for file in os.listdir(kinematics_path):
        if file.endswith('.mot'):
            return os.path.join(kinematics_path, file)
    
    return None

def process_comparison(main_dir, output_dir, trial1, trial2):
    """
    Process comparison between two trials and save results
    """
    # Find the folders for the trials
    trial1_folders = [folder for folder in os.listdir(main_dir) if folder.startswith(f'openpose_results_{trial1}_')]
    trial2_folders = [folder for folder in os.listdir(main_dir) if folder.startswith(f'openpose_results_{trial2}_')]
    
    if not trial1_folders or not trial2_folders:
        print(f"Could not find folders for {trial1} or {trial2}")
        return
    
    # Get the first matching folder for each trial
    trial1_folder = trial1_folders[0]
    trial2_folder = trial2_folders[0]
    
    # Extract conditions from folder names
    trial1_condition = extract_condition_from_folder(trial1_folder)
    trial2_condition = extract_condition_from_folder(trial2_folder)
    
    # Build paths to kinematics folders
    trial1_kinematics = os.path.join(main_dir, trial1_folder, 'kinematics')
    trial2_kinematics = os.path.join(main_dir, trial2_folder, 'kinematics')
    
    # Find .mot files
    trial1_mot = find_mot_file_in_kinematics(trial1_kinematics)
    trial2_mot = find_mot_file_in_kinematics(trial2_kinematics)
    
    if not trial1_mot or not trial2_mot:
        print(f"Could not find .mot files for {trial1} or {trial2}")
        return
    
    print(f"Processing comparison: {trial1} ({trial1_condition}) vs {trial2} ({trial2_condition})")
    print(f"Files: {os.path.basename(trial1_mot)} vs {os.path.basename(trial2_mot)}")
    
    try:
        # Load data
        trial1_data = load_mot_file(trial1_mot)
        trial2_data = load_mot_file(trial2_mot)
        
        # Run analysis
        results = analyze_gait_patterns(trial1_data, trial2_data)
        
        # Create output filename
        output_filename = f"{trial1}_{trial1_condition}_vs_{trial2}_{trial2_condition}.txt"
        output_path = os.path.join(output_dir, output_filename)
        
        # Print results to file
        print_analysis_results_to_file(results, f"{trial1} ({trial1_condition})", f"{trial2} ({trial2_condition})", output_path)
        
        print(f"Analysis complete. Results saved to {output_path}")
        
    except Exception as e:
        print(f"Error processing comparison {trial1} vs {trial2}: {str(e)}")

def run_all_comparisons(main_dir, output_dir):
    """
    Run all required comparisons
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    
    # Define the comparisons to run
    comparisons = [
        ('T00', 'T01'),
        ('T00', 'T02'),
        ('T01', 'T02'),
        ('T00', 'T03'),
        ('T01', 'T04'),
        ('T02', 'T05')
    ]
    
    # Process each comparison
    for trial1, trial2 in comparisons:
        process_comparison(main_dir, output_dir, trial1, trial2)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python Auto_angles_analysis.py <main_directory_path> <output_directory_path>")
        sys.exit(1)
    
    main_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    if not os.path.isdir(main_dir):
        print(f"Error: Main directory '{main_dir}' does not exist.")
        sys.exit(1)
    
    run_all_comparisons(main_dir, output_dir)

# python Auto_angles_analysis.py "D:\Miro Hernandez\Documents\openpose-1.7.0-binaries-win64-gpu-python3.7-flir-3d_recommended\FINAL_ACCURATE_OPENPOSE_DATASET\Matthew" "D:\Miro Hernandez\Documents\openpose-1.7.0-binaries-win64-gpu-python3.7-flir-3d_recommended\FINAL_ACCURATE_OPENPOSE_DATASET\Matthew\angles_statistics"