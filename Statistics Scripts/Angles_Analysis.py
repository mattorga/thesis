import pandas as pd
import numpy as np
from scipy import signal
from scipy.stats import pearsonr
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt

skip_cols = [44, 45, 53, 54, 55, 60, 61, 62]

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
    
    print(before_data.shape)
    print(after_data.shape)

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

# def print_analysis_results(results):
#     """
#     Print analysis results in a formatted way
#     """
#     print("\nGait Analysis Results:")
#     print("-" * 100)
#     print(f"{'Column':^8} {'DTW Dist':^12} {'Cross-Corr':^12} {'Time Lag':^10} {'Pearson r':^12} {'P-value':^12}")
#     print("-" * 100)
    
#     for col in range(len(results['dtw_distances'])):
#         if col in skip_cols:
#             continue
            
#         dtw_dist = results['dtw_distances'][col]
#         cross_corr = results['cross_corr_max'][col]
#         time_lag = results['cross_corr_lags'][col]
#         pearson = results['pearson_corr'][col]
#         p_val = results['p_values'][col]
        
        
        
#         print(f"{col:^8d} {dtw_dist:^12.4f} {cross_corr:^12.4f} {time_lag:^10.0f} "
#               f"{pearson:^12.4f} {p_val:^12.4f}")
    
#     # Print summary statistics
#     print("\nSummary Statistics:")
#     print(f"Average DTW distance: {np.nanmean(results['dtw_distances'][1:]):.4f}")
#     print(f"Average cross-correlation: {np.nanmean(results['cross_corr_max'][1:]):.4f}")
#     print(f"Average Pearson correlation: {np.nanmean(results['pearson_corr'][1:]):.4f}")
def print_analysis_results_to_file(results, filename="gait_analysis_results.txt"):
    # Define columns to skip: time column (0) plus extra columns
    skip_cols = [0, 44, 45, 53, 54, 55, 60, 61, 62]

    with open(filename, "w") as f:
        # Write header
        f.write("\nGait Analysis Results:\n")
        f.write("-" * 100 + "\n")
        f.write(f"{'Column':^8} {'DTW Dist':^12} {'Cross-Corr':^12} {'Time Lag':^10} {'Pearson r':^12} {'P-value':^12}\n")
        f.write("-" * 100 + "\n")
        
        # Loop through each column and skip specified columns
        for col in range(len(results['dtw_distances'])):
            if col in skip_cols:
                continue
                
            dtw_dist = results['dtw_distances'][col]
            cross_corr = results['cross_corr_max'][col]
            time_lag = results['cross_corr_lags'][col]
            pearson = results['pearson_corr'][col]
            p_val = results['p_values'][col]
            
            # Write the formatted results for this column
            f.write(f"{col:^8d} {dtw_dist:^12.4f} {cross_corr:^12.4f} {time_lag:^10.0f} "
                    f"{pearson:^12.4f} {p_val:^12.4f}\n")
        
        # Write summary statistics
        f.write("\nSummary Statistics:\n")
        f.write(f"Average DTW distance: {np.nanmean(results['dtw_distances'][1:]):.4f}\n")
        f.write(f"Average cross-correlation: {np.nanmean(results['cross_corr_max'][1:]):.4f}\n")
        f.write(f"Average Pearson correlation: {np.nanmean(results['pearson_corr'][1:]):.4f}\n")

# Example usage:
if __name__ == "__main__":
    # Your file paths
    before_file = "D:\Miro Hernandez\Documents\openpose-1.7.0-binaries-win64-gpu-python3.7-flir-3d_recommended\Statistics test\BatchSession_Ronnel\T01_spastic_1.5\kinematics\T01_spastic_1_filt_butterworth_on_speed.mot"
    after_file = "D:\Miro Hernandez\Documents\openpose-1.7.0-binaries-win64-gpu-python3.7-flir-3d_recommended\Statistics test\BatchSession_Ronnel\T02_spastic_1.5\kinematics\T02_spastic_1_filt_butterworth_on_speed.mot"
    
    # Load data
    before_data = load_mot_file(before_file)
    after_data = load_mot_file(after_file)
    
    print(f'Before data dimensions: {before_data.shape}')
    print(f'After data dimensions: {after_data.shape}')
    
    # Run analysis
    results = analyze_gait_patterns(before_data, after_data)
    
    # Print results
    txt_filename = "Ronnel_T01_spastic_vs_T02_spastic.txt"
    print_analysis_results_to_file(results, txt_filename)