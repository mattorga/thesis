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

def analyze_gait_patterns(base_mot, versus_mot):
    """
    Analyzes gait patterns from two MOT files and computes similarity metrics.
    
    Args:
        base_mot (str): Path to the first MOT file (base trial)
        versus_mot (str): Path to the second MOT file (verse trial)
        
    Returns:
        dict: Dictionary containing similarity metrics
    """
    # Suppress specific warnings that occur during analysis
    import warnings
    import numpy as np
    from scipy import stats
    
    base_trial = load_mot_file(base_mot)
    versus_trial = load_mot_file(versus_mot)

    min_length = min(len(base_trial), len(versus_trial))
    

    # Trim data to same length
    base_trial = base_trial[:min_length]
    versus_trial = versus_trial[:min_length]

    # Initialize results containers
    num_features = base_trial.shape[1]
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
        seq1 = base_trial[:, col]
        seq2 = versus_trial[:, col]
        
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
            dtw_distances[col] = np.nan
            cross_corr_max[col] = np.nan
            cross_corr_lags[col] = np.nan
            pearson_corr[col] = np.nan
            p_values[col] = np.nan
    
    return {
        # 'dtw_distances': dtw_distances,
        # 'cross_corr_max': cross_corr_max,
        # 'cross_corr_lags': cross_corr_lags,
        # 'pearson_corr': pearson_corr,
        'ave_p_values': np.nanmean(p_values),
        'ave_dtw': np.nanmean(dtw_distances),
        'ave_corr': np.nanmean(cross_corr_lags),
        'ave_pearson_corr': np.nanmean(pearson_corr)
    }