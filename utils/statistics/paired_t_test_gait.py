import pandas as pd
import numpy as np
from scipy import stats

def analyze_gait_parameters(base_trial, versus_trial):
    """
    Analyzes multiple CSV files for each condition and performs paired t-tests.
    
    Parameters:
    base_trial (list): List of paths to base trial CSV files.
    versus_trial (list): List of paths to versus trial CSV files.
    
    Returns:
    results (dict): Dictionary containing statistics including:
        - 'ave_p_value': Average p-value across all parameters
        - 'sig_params': Number of significantly different parameters
        - 'total_params': Total number of parameters compared
        - 'sig_percent': Percentage of significant differences
    output_str (str): Formatted string of the analysis results.
    """
    # Initialize dictionaries to store measurements
    base_data = {}
    versus_data = {}
    
    # Read all base trial CSVs
    for csv_path in base_trial:
        df = pd.read_csv(csv_path)
        for column in df.columns:
            if column not in base_data:
                base_data[column] = []
            base_data[column].append(df[column].values[0])  # Assuming single value per metric
            
    # Read all versus trial CSVs
    for csv_path in versus_trial:
        df = pd.read_csv(csv_path)
        for column in df.columns:
            if column not in versus_data:
                versus_data[column] = []
            versus_data[column].append(df[column].values[0])  # Assuming single value per metric
    
    # Initialize results dictionary
    results = {
        't_stats': {},
        'p_values': {},
        'means_base': {},        # Renamed from 'means_abnormal'
        'means_versus': {},      # Renamed from 'means_normal'
        'std_base': {},          # Renamed from 'std_abnormal'
        'std_versus': {}         # Renamed from 'std_normal'
    }
    
    # Perform paired t-test for each parameter
    for metric in base_data.keys():
        if metric in versus_data:  # Only compare metrics that exist in both datasets
            base_values = np.array(base_data[metric])
            versus_values = np.array(versus_data[metric])
            
            # Perform paired t-test
            t_stat, p_value = stats.ttest_rel(base_values, versus_values)
            
            # Store results
            results['t_stats'][metric] = t_stat
            results['p_values'][metric] = p_value
            results['means_base'][metric] = np.mean(base_values)
            results['means_versus'][metric] = np.mean(versus_values)
            results['std_base'][metric] = np.std(base_values)
            results['std_versus'][metric] = np.std(versus_values)
    
    # Calculate overall statistics
    ave_p_value = np.nanmean(list(results['p_values'].values()))
    significant_params = sum(p <= 0.05 for p in results['p_values'].values())
    total_params = len(results['p_values'])
    sig_percent = (significant_params / total_params) * 100 if total_params > 0 else 0
    
    # Add the UI-specific keys to the results dictionary
    results['ave_p_value'] = ave_p_value
    results['sig_params'] = significant_params
    results['total_params'] = total_params
    results['sig_percent'] = sig_percent
    
    return results