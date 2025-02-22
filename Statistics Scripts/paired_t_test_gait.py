import pandas as pd
import numpy as np
from scipy import stats

def analyze_gait_parameters_multiple(abnormal_csvs, normal_csvs):
    """
    Analyzes multiple CSV files for each condition and performs paired t-tests.
    
    Parameters:
    abnormal_csvs (list): List of paths to abnormal gait CSV files.
    normal_csvs (list): List of paths to normal gait CSV files.
    
    Returns:
    results (dict): Dictionary containing t-stats, p-values, means, and standard deviations.
    output_str (str): Formatted string of the analysis results.
    """
    # Initialize dictionaries to store measurements
    abnormal_data = {}
    normal_data = {}
    
    # Read all abnormal CSVs
    for csv_path in abnormal_csvs:
        df = pd.read_csv(csv_path)
        for column in df.columns:
            if column not in abnormal_data:
                abnormal_data[column] = []
            abnormal_data[column].append(df[column].values[0])  # Assuming single value per metric
            
    # Read all normal CSVs
    for csv_path in normal_csvs:
        df = pd.read_csv(csv_path)
        for column in df.columns:
            if column not in normal_data:
                normal_data[column] = []
            normal_data[column].append(df[column].values[0])  # Assuming single value per metric
    
    # Initialize results dictionary
    results = {
        't_stats': {},
        'p_values': {},
        'means_abnormal': {},
        'means_normal': {},
        'std_abnormal': {},
        'std_normal': {}
    }
    
    # Perform paired t-test for each parameter
    for metric in abnormal_data.keys():
        abnormal_values = np.array(abnormal_data[metric])
        normal_values = np.array(normal_data[metric])
        
        # Perform paired t-test
        t_stat, p_value = stats.ttest_rel(abnormal_values, normal_values)
        
        # Store results
        results['t_stats'][metric] = t_stat
        results['p_values'][metric] = p_value
        results['means_abnormal'][metric] = np.mean(abnormal_values)
        results['means_normal'][metric] = np.mean(normal_values)
        results['std_abnormal'][metric] = np.std(abnormal_values)
        results['std_normal'][metric] = np.std(normal_values)
    
    # Prepare formatted output
    output_lines = []
    output_lines.append("\nStatistical Analysis Results:")
    output_lines.append("-" * 100)
    output_lines.append(f"{'Parameter':<25} {'T-statistic':>12} {'P-value':>12} "
                        f"{'Mean Abnormal':>15} {'Mean Normal':>15} "
                        f"{'Std Abnormal':>12} {'Std Normal':>12}")
    output_lines.append("-" * 100)
    
    for param in results['t_stats'].keys():
        output_lines.append(f"{param:<25} {results['t_stats'][param]:>12.4f} {results['p_values'][param]:>12.4f} "
                            f"{results['means_abnormal'][param]:>15.4f} {results['means_normal'][param]:>15.4f} "
                            f"{results['std_abnormal'][param]:>12.4f} {results['std_normal'][param]:>12.4f}")
    
    # Calculate overall statistics
    avg_p_value = np.mean(list(results['p_values'].values()))
    significant_params = sum(p <= 0.05 for p in results['p_values'].values())
    total_params = len(results['p_values'])
    
    output_lines.append("\nSummary Statistics:")
    output_lines.append(f"Average p-value across all parameters: {avg_p_value:.4f}")
    output_lines.append(f"Number of significantly different parameters: {significant_params} out of {total_params}")
    output_lines.append(f"Percentage of significant differences: {(significant_params/total_params)*100:.2f}%")
    
    # Join all lines into a single string
    output_str = "\n".join(output_lines)
    
    # Print the output to console
    print(output_str)
    
    return results, output_str

# Example usage:
if __name__ == "__main__":
    # Example file paths (replace with your actual paths)
    abnormal_csvs = [
        "D:\Miro Hernandez\Documents\openpose-1.7.0-binaries-win64-gpu-python3.7-flir-3d_recommended\Statistics test\Spatio temporal Kinematics\Ronnel\T00_spastic_1_filt_butterworth_on_speed.csv",
        "D:\Miro Hernandez\Documents\openpose-1.7.0-binaries-win64-gpu-python3.7-flir-3d_recommended\Statistics test\Spatio temporal Kinematics\Ronnel\T01_spastic_1_filt_butterworth_on_speed.csv",
        "D:\Miro Hernandez\Documents\openpose-1.7.0-binaries-win64-gpu-python3.7-flir-3d_recommended\Statistics test\Spatio temporal Kinematics\Ronnel\T02_spastic_1_filt_butterworth_on_speed.csv"
    ]
    
    normal_csvs = [
        "D:\Miro Hernandez\Documents\openpose-1.7.0-binaries-win64-gpu-python3.7-flir-3d_recommended\Statistics test\Spatio temporal Kinematics\Ronnel\T03_normal_1_filt_butterworth_on_speed.csv",
        "D:\Miro Hernandez\Documents\openpose-1.7.0-binaries-win64-gpu-python3.7-flir-3d_recommended\Statistics test\Spatio temporal Kinematics\Ronnel\T04_normal_1_filt_butterworth_on_speed.csv",
        "D:\Miro Hernandez\Documents\openpose-1.7.0-binaries-win64-gpu-python3.7-flir-3d_recommended\Statistics test\Spatio temporal Kinematics\Ronnel\T05_normal_1_filt_butterworth_on_speed.csv"
    ]
    # Specify the output path for writing the table to a text file
    output_path = "D:\Miro Hernandez\Documents\openpose-1.7.0-binaries-win64-gpu-python3.7-flir-3d_recommended\Statistics test\Spatio temporal Kinematics\Ronnel\Ronnel_paired_t_test_abnormal_vs_normal.txt"
    
    # Perform the analysis and capture the output string
    results, output_str = analyze_gait_parameters_multiple(abnormal_csvs, normal_csvs)
    
    # Write the output to a text file
    with open(output_path, "w") as file:
        file.write(output_str)
    
    print(f"\nResults written to {output_path}")