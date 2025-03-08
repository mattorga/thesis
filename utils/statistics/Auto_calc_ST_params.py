import os
import re
import sys
import pandas as pd
import numpy as np
from scipy.signal import find_peaks

# Add the directory containing your script to the Python path
# This assumes the script is in the same directory as this automation script
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)


try:

    from Calc_ST_params import analyze_gait
except ImportError:
    try:
        # If your script has a different name (assuming it's in the same directory)
        # This imports the functions directly from your script by finding the .py file
        py_files = [f for f in os.listdir(script_dir) if f.endswith('.py') and f != os.path.basename(__file__)]
        if py_files:
            module_name = os.path.splitext(py_files[0])[0]
            print(f"Trying to import from {module_name}.py")
            
            # Import dynamically
            module = __import__(module_name)
            load_trc_file = module.load_trc_file
            detect_heel_strikes = module.detect_heel_strikes
            calculate_stride_length_dynamic = module.calculate_stride_length_dynamic
            calculate_stride_time = module.calculate_stride_time
            calculate_gait_speed_from_dynamic = module.calculate_gait_speed_from_dynamic
            calculate_stride_width = module.calculate_stride_width
            analyze_gait = module.analyze_gait
        else:
            raise ImportError("Could not find your gait analysis script in the current directory")
    except Exception as e:
        print(f"Error importing functions: {e}")
        sys.exit(1)

def process_trc_files(main_path):
    """
    Processes all TRC files with 'LSTM' in their filename located in T0X/pose-3d folders.
    Saves results to a Spatiotemporal_statistics folder.
    
    Args:
        main_path (str): Path to the main directory containing T0X folders
    """
    # Create Spatiotemporal_statistics folder if it doesn't exist
    stats_folder = os.path.join(main_path, "Spatiotemporal_statistics")
    if not os.path.exists(stats_folder):
        os.makedirs(stats_folder)
        print(f"Created output folder: {stats_folder}")
    
    # Find all folders containing T0X in their name with a more flexible pattern
    # This will match any folder with T0 followed by one or more digits anywhere in the name
    t0x_pattern = re.compile(r'.*T0\d+.*', re.IGNORECASE)
    t0x_folders = [f for f in os.listdir(main_path) 
                  if os.path.isdir(os.path.join(main_path, f)) and t0x_pattern.search(f)]
    
    # Sort folders to process them in a logical order
    t0x_folders.sort()
    
    print(f"Found {len(t0x_folders)} T0X folders to process")
    
    # Process each T0X folder
    for t0x_folder in t0x_folders:
        t0x_path = os.path.join(main_path, t0x_folder)
        pose_3d_path = os.path.join(t0x_path, "pose-3d")
        
        # Define a function to recursively search for pose-3d folders
        def find_pose_3d_folders(root_dir, max_depth=3, current_depth=0):
            """Recursively search for 'pose-3d' folders up to a maximum depth"""
            if current_depth > max_depth:
                return []
                
            pose_3d_folders = []
            try:
                # Check if current directory is the pose-3d folder
                if os.path.basename(root_dir).lower() == "pose-3d":
                    return [root_dir]
                    
                # Look for pose-3d in direct subdirectories
                for item in os.listdir(root_dir):
                    item_path = os.path.join(root_dir, item)
                    if os.path.isdir(item_path):
                        if item.lower() == "pose-3d":
                            pose_3d_folders.append(item_path)
                        elif current_depth < max_depth:
                            # Recursively search in subdirectories
                            pose_3d_folders.extend(find_pose_3d_folders(item_path, max_depth, current_depth + 1))
            except Exception as e:
                print(f"Error accessing {root_dir}: {e}")
                
            return pose_3d_folders
        
        # Search for pose-3d folders in the T0X folder
        pose_3d_folders = find_pose_3d_folders(t0x_path)
        
        if not pose_3d_folders:
            print(f"Could not find any pose-3d folders in {t0x_folder}, skipping...")
            continue
            
        print(f"Found {len(pose_3d_folders)} pose-3d folder(s) in {t0x_folder}")
        
        # Process each pose-3d folder
        for pose_3d_path in pose_3d_folders:
        
            # Find all TRC files with 'LSTM' in their filename (case insensitive)
            trc_files = [f for f in os.listdir(pose_3d_path) 
                        if f.lower().endswith('.trc') and ('lstm' in f.lower())]
            
            # If no LSTM files found, look for any .trc files
            if not trc_files:
                print(f"No LSTM TRC files found in {pose_3d_path}, checking for any .trc files")
                trc_files = [f for f in os.listdir(pose_3d_path) if f.lower().endswith('.trc')]
            
            if not trc_files:
                print(f"No TRC files found in {pose_3d_path}, skipping this folder")
                continue
                
            print(f"Found {len(trc_files)} TRC file(s) in {pose_3d_path}")
            
            # Process each TRC file
            for trc_file in trc_files:
                trc_path = os.path.join(pose_3d_path, trc_file)
                print(f"\nProcessing: {trc_path}")
                
                try:
                    # Run the gait analysis
                    results = analyze_gait(trc_path)
                    
                    if results['status'] == 'success':
                        # Print out the metrics
                        print(f"Dynamic stride length: {results['stride_length_cm']:.2f} cm")
                        print(f"Stride time: {results['stride_time_s']:.2f} s")
                        print(f"Gait speed: {results['gait_speed_ms']:.2f} m/s")
                        print(f"Stride width: {results['stride_width_cm']:.2f} cm")
                        
                        # Create the output CSV file with same name as the TRC file
                        filename_no_ext, _ = os.path.splitext(trc_file)
                        # Include T0X identifier in the output filename
                        t0x_id = re.search(r'T0\d+', t0x_folder, re.IGNORECASE).group(0)
                        output_filename = f"{t0x_id}_{filename_no_ext}.csv"
                        output_path = os.path.join(stats_folder, output_filename)
                        
                        # Prepare a DataFrame with the desired results and headers
                        df_out = pd.DataFrame({
                            "Dynamic stride length (cm)": [results['stride_length_cm']],
                            "Stride time (s)": [results['stride_time_s']],
                            "Gait speed (m/s)": [results['gait_speed_ms']],
                            "Stride width (cm)": [results['stride_width_cm']]
                        })
                        
                        # Save to CSV
                        df_out.to_csv(output_path, index=False)
                        print(f"Results saved to {output_path}")
                    else:
                        print(f"Gait analysis failed for {trc_file}: {results['message']}")
                except Exception as e:
                    print(f"Error processing {trc_file}: {str(e)}")

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
    print("=" * 80)
    print("TRC File Batch Processing Script")
    print("=" * 80)
    
    # Get the main path from user or command line
    main_path = get_folder_path()
    print(f"Using main path: {main_path}")
    
    # Verify the path exists
    if not os.path.exists(main_path):
        print(f"Error: The path {main_path} does not exist.")
        sys.exit(1)
    
    # Process all TRC files
    process_trc_files(main_path)
    
    print("\nProcessing complete!")
    print("=" * 80)