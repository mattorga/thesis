import os
import sys
import re
import glob

def import_original_script():
    """
    Attempts to import the analyze_gait_parameters_multiple function from the original script.
    Tries different filenames in case the script was renamed.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    

    try:
        from paired_t_test_gait import analyze_gait_parameters_multiple
        print("Successfully imported from paste.py")
        return analyze_gait_parameters_multiple
    except ImportError:
        # If that fails, try to find any Python file that might contain the function
        try:
            py_files = [f for f in os.listdir(script_dir) 
                       if f.endswith('.py') and f != os.path.basename(__file__)]
            
            if not py_files:
                raise ImportError("No Python files found in the directory")
            
            for py_file in py_files:
                module_name = os.path.splitext(py_file)[0]
                print(f"Trying to import from {module_name}.py...")
                
                try:
                    # Import the module dynamically
                    module = __import__(module_name)
                    
                    # Check if it has the function we need
                    if hasattr(module, 'analyze_gait_parameters_multiple'):
                        print(f"Successfully imported from {module_name}.py")
                        return module.analyze_gait_parameters_multiple
                except (ImportError, AttributeError):
                    continue
                    
            raise ImportError("Could not find analyze_gait_parameters_multiple in any Python file")
        except Exception as e:
            print(f"Error importing function: {str(e)}")
            sys.exit(1)

def run_automated_paired_ttest(main_path):
    """
    Automates the paired t-test analysis for CSV files in the Spatiotemporal_statistics folder.
    Automatically groups files as abnormal (T00-T02) and normal (T03-T05).
    
    Parameters:
    main_path (str): Path to the main directory containing the Spatiotemporal_statistics folder.
    
    Returns:
    bool: True if successful, False otherwise.
    """
    print("=" * 80)
    print("Automated Paired T-Test Analysis")
    print("=" * 80)
    
    # Import the analysis function from the original script
    analyze_gait_parameters_multiple = import_original_script()
    
    # Check if main path exists
    if not os.path.exists(main_path):
        print(f"Error: Main path '{main_path}' does not exist.")
        return False
    
    # Find Spatiotemporal_statistics folder
    stats_folder = os.path.join(main_path, "Spatiotemporal_statistics")
    if not os.path.exists(stats_folder):
        print(f"Error: Spatiotemporal_statistics folder not found in {main_path}")
        return False
    
    print(f"Found Spatiotemporal_statistics folder: {stats_folder}")
    
    # Create output folder for paired t-test results
    output_folder = os.path.join(main_path, "paired_t_test_results")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")
    else:
        print(f"Using existing output folder: {output_folder}")
    
    # Find all CSV files in the statistics folder
    csv_files = glob.glob(os.path.join(stats_folder, "*.csv"))
    print(f"Found {len(csv_files)} CSV files in total")
    
    if len(csv_files) == 0:
        print("Error: No CSV files found in the Spatiotemporal_statistics folder.")
        return False
    
    # Group CSV files based on pattern
    abnormal_pattern = re.compile(r'T0[0-2]', re.IGNORECASE)
    normal_pattern = re.compile(r'T0[3-5]', re.IGNORECASE)
    
    abnormal_csvs = [f for f in csv_files if abnormal_pattern.search(os.path.basename(f))]
    normal_csvs = [f for f in csv_files if normal_pattern.search(os.path.basename(f))]
    
    # Sort the file lists to ensure consistent order
    abnormal_csvs.sort()
    normal_csvs.sort()
    
    print(f"Found {len(abnormal_csvs)} abnormal CSV files (T00-T02)")
    print(f"Found {len(normal_csvs)} normal CSV files (T03-T05)")
    
    # Verify we have files in both groups
    if len(abnormal_csvs) == 0 or len(normal_csvs) == 0:
        print("Error: Missing either abnormal or normal CSV files.")
        return False
    
    # Print file paths for verification
    print("\nAbnormal CSV files:")
    for csv in abnormal_csvs:
        print(f"  - {csv}")
    
    print("\nNormal CSV files:")
    for csv in normal_csvs:
        print(f"  - {csv}")
    
    # Run the paired t-test analysis
    print("\nRunning paired t-test analysis...")
    try:
        results, output_str = analyze_gait_parameters_multiple(abnormal_csvs, normal_csvs)
        
        # Create output file name based on main directory name
        main_dir_name = os.path.basename(os.path.normpath(main_path))
        output_path = os.path.join(output_folder, f"{main_dir_name}_paired_t_test_abnormal_vs_normal.txt")
        
        # Write the output to a text file
        with open(output_path, "w") as f:
            f.write(output_str)
        
        print(f"\nResults written to {output_path}")
        print("Analysis completed successfully!")
        return True
    
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        return False

def get_folder_path():
    """Prompt user for folder path or use command line argument"""
    if len(sys.argv) > 1:
        # Use command line argument if provided
        return sys.argv[1]
    else:
        # Prompt user for path
        default_path = r"D:\Miro Hernandez\Documents\openpose-1.7.0-binaries-win64-gpu-python3.7-flir-3d_recommended\Statistics test"
        path = input(f"Enter the main folder path (press Enter to use default: {default_path}): ")
        return path.strip() if path.strip() else default_path


if __name__ == "__main__":

    
    # Get the main path from user or command line
    main_path = get_folder_path()
    print(f"Using main path: {main_path}")
    
    # Run the analysis
    success = run_automated_paired_ttest(main_path)
    
    print("\nProcess complete!")
    print("=" * 80)