import numpy as np
from scipy.signal import find_peaks
import pandas as pd
import os
def load_trc_file(file_path):
    """
    Load and parse a .trc file into a pandas DataFrame.
    """
    with open(file_path, 'r') as f:
        # Skip first three lines
        for _ in range(3):
            next(f)
        
        # Read the marker names line
        marker_line = next(f)
        markers = marker_line.strip().split('\t')
        markers = [m for m in markers if m.strip()]
        
        # Skip the coordinate labels line (X1, Y1, Z1, etc.)
        next(f)
        
        # Create column names: Frame#, Time, then each marker's X, Y, Z coordinates
        columns = ['Frame#', 'Time']
        for marker in markers[2:]:
            columns.extend([f'{marker}_X', f'{marker}_Y', f'{marker}_Z'])
        
        data = []
        for line in f:
            if line.strip():
                values = line.strip().split('\t')
                values = [float(v) for v in values if v.strip()]
                if len(values) == len(columns):
                    data.append(values)
    
    return pd.DataFrame(data, columns=columns)

def detect_heel_strikes(data, side='R', window_size=5):
    """
    Detect heel strikes using a smoothed vertical signal.
    
    Note: Adjust the axis used for vertical motion. Based on your TRC file, if
    Z is vertical instead of Y, change 'RAnkle_Y' to 'RAnkle_Z' accordingly.
    """
    # For this example, we assume vertical motion is captured in the Y coordinate.
    ankle_vert = data[f'{side}Ankle_Y'].values  
    # If vertical is actually Z, use: data[f'{side}Ankle_Z'].values

    def moving_average(x, w):
        
        return np.convolve(x, np.ones(w), 'valid') / w

    smooth_signal = moving_average(ankle_vert, window_size)
    offset = (window_size - 1) // 2
    # Detect local minima (heel strikes)
    min_peaks, _ = find_peaks(-smooth_signal, distance=10, prominence=0.001)
    heel_strikes = [peak + offset for peak in min_peaks]

    # Basic filtering: remove strikes that are too close together
    if heel_strikes:
        filtered = [heel_strikes[0]]
        for hs in heel_strikes[1:]:
            if hs - filtered[-1] > 20: # Minimum frame between heel strikes
                filtered.append(hs)
        heel_strikes = filtered

    return np.array(heel_strikes)

# def calculate_stride_length_dynamic(data, r_heel_strikes, l_heel_strikes):
#     """
#     Dynamically calculate stride length based on X-axis differences at heel strikes.
    
#     The algorithm:
#     - Combine heel strikes from both feet in chronological order.
#     - Determine which foot struck first and assume alternating events.
#     - For a full cycle (e.g., R -> L -> R), compute:
#          step1 = X(R_first) to X(L_middle)
#          step2 = X(L_middle) to X(R_next)
#          Stride length = step1 + step2
#     - Do the analogous calculation if L strikes first.
    
#     Returns the average stride length in centimeters.
#     """
#     # Build a list of events: each tuple is (frame index, side)
#     events = [(hs, 'R') for hs in r_heel_strikes] + [(hs, 'L') for hs in l_heel_strikes]
#     events.sort(key=lambda x: x[0])
    
#     stride_lengths = []
#     i = 0
#     while i < len(events) - 2:
#         e1, e2, e3 = events[i], events[i+1], events[i+2]
#         # Check that the first and third events are from the same foot and the middle is from the opposite foot.
#         if e1[1] == e3[1] and e1[1] != e2[1]:
#             if e1[1] == 'R':
#                 x1 = data['RAnkle_X'].iloc[e1[0]]
#                 x2 = data['LAnkle_X'].iloc[e2[0]]
#                 x3 = data['RAnkle_X'].iloc[e3[0]]
#             else:
#                 x1 = data['LAnkle_X'].iloc[e1[0]]
#                 x2 = data['RAnkle_X'].iloc[e2[0]]
#                 x3 = data['LAnkle_X'].iloc[e3[0]]
#             # Compute step lengths (assuming increasing X is forward)
#             step1 = np.abs(x2 - x1)
#             step2 = np.abs(x3 - x2)
#             stride_length = step1 + step2
#             stride_lengths.append(stride_length)
#             i += 2  # Skip ahead to the next cycle
#         else:
#             i += 1

#     if stride_lengths:
#         return np.mean(stride_lengths) * 100  # convert from meters to centimeters
#     else:
#         return np.nan

def calculate_stride_length_dynamic(data, r_heel_strikes, l_heel_strikes):
    """
    Dynamically calculate stride length using heel and big toe markers.
    
    For a gait cycle:
    - If the starting foot is R, then:
         step1 = |RHeel_X (initial R heel strike) - LBigToe_X (subsequent L heel strike)|
         step2 = |RHeel_X (next R heel strike) - LBigToe_X (same L heel strike)|
    - If the starting foot is L, then:
         step1 = |LHeel_X (initial L heel strike) - RBigToe_X (subsequent R heel strike)|
         step2 = |LHeel_X (next L heel strike) - RBigToe_X (same R heel strike)|
    Stride length is then the sum of step1 and step2.
    
    Returns the average stride length in centimeters.
    """
    # Combine events from both feet into a sorted list: (frame index, side)
    events = [(hs, 'R') for hs in r_heel_strikes] + [(hs, 'L') for hs in l_heel_strikes]
    events.sort(key=lambda x: x[0])
    
    stride_lengths = []
    i = 0
    while i < len(events) - 2:
        e1, e2, e3 = events[i], events[i+1], events[i+2]
        # Ensure the pattern: starting foot -> opposite foot -> same starting foot
        if e1[1] == e3[1] and e1[1] != e2[1]:
            if e1[1] == 'R':
                heel_start = data['RHeel_X'].iloc[e1[0]]
                bigtoe_mid = data['LBigToe_X'].iloc[e2[0]]
                heel_end   = data['RHeel_X'].iloc[e3[0]]
            else:  # starting foot is 'L'
                heel_start = data['LHeel_X'].iloc[e1[0]]
                bigtoe_mid = data['RBigToe_X'].iloc[e2[0]]
                heel_end   = data['LHeel_X'].iloc[e3[0]]
            # Calculate step lengths using X-axis differences (assuming X is forward)
            step1 = np.abs(bigtoe_mid - heel_start)
            step2 = np.abs(heel_end - bigtoe_mid)
            stride_length = step1 + step2
            stride_lengths.append(stride_length)
            i += 2  # Skip ahead to the next cycle
        else:
            i += 1

    if stride_lengths:
        return np.mean(stride_lengths) * 100  # convert from meters to centimeters
    else:
        return np.nan

def calculate_stride_time(data, heel_strikes):
    """
    Calculate the average stride (cycle) time from consecutive heel strikes of the same foot.
    """
    if len(heel_strikes) < 2:
        return np.nan
    times = []
    for i in range(len(heel_strikes)-1):
        t1 = data['Time'].iloc[heel_strikes[i]]
        t2 = data['Time'].iloc[heel_strikes[i+1]]
        times.append(t2 - t1)
    return np.mean(times) if times else np.nan

def calculate_gait_speed_from_dynamic(stride_length_cm, stride_time):
    """
    Calculate gait speed in m/s based on dynamic stride length and stride time.
    """
    if np.isnan(stride_length_cm) or np.isnan(stride_time) or stride_time == 0:
        return np.nan
    stride_length_m = stride_length_cm / 100.0
    return stride_length_m / stride_time

def calculate_stride_width(data, r_heel_strikes, l_heel_strikes):
    """
    Calculate stride width based on lateral (Z-axis) differences at heel strikes.
    """
    if len(r_heel_strikes) == 0 or len(l_heel_strikes) == 0:
        return np.nan
    widths = []
    for rhs in r_heel_strikes:
        try:
            lhs = l_heel_strikes[np.argmin(np.abs(l_heel_strikes - rhs))]
            y_r = data['RAnkle_Z'].iloc[rhs]
            y_l = data['LAnkle_Z'].iloc[lhs]
            widths.append(np.abs(y_r - y_l))
        except Exception:
            continue
    return np.mean(widths) * 100 if widths else np.nan

def analyze_gait(file_path):
    """
    Main function to analyze gait parameters from a .trc file using a dynamic
    stride length calculation based on alternating heel strikes.
    
    Returns a dictionary containing the computed metrics as well as the frame indices
    of the detected heel strikes for both the left and right feet.
    """
    try:
        data = load_trc_file(file_path)
        print("Loaded Data")
        print("Available columns:", data.columns.tolist())
        
        # Detect heel strikes for both feet
        r_heel_strikes = detect_heel_strikes(data, side='R')
        l_heel_strikes = detect_heel_strikes(data, side='L')
        # print(f"Detected heel strikes:")
        # print(f"Right foot frames: {r_heel_strikes}")
        # print(f"Left foot frames: {l_heel_strikes}")
        
        if len(r_heel_strikes) == 0 and len(l_heel_strikes) == 0:
            print("Warning: No heel strikes detected. Cannot perform gait analysis.")
            return {
                'status': 'error',
                'message': 'No heel strikes detected'
            }
        
        # Compute dynamic stride length from X-axis differences
        stride_length_cm = calculate_stride_length_dynamic(data, r_heel_strikes, l_heel_strikes)
        
        # Compute average stride time (using one foot's events, e.g., right)
        stride_time = calculate_stride_time(data, r_heel_strikes)
        
        # Compute gait speed from these values
        gait_speed_ms = calculate_gait_speed_from_dynamic(stride_length_cm, stride_time)
        
        # Compute stride width (using lateral Y-axis differences)
        stride_width_cm = calculate_stride_width(data, r_heel_strikes, l_heel_strikes)
        
        # Return the computed metrics along with the heel strike frames
        return {
            'status': 'success',
            'stride_length_cm': stride_length_cm,
            'stride_time_s': stride_time,
            'gait_speed_ms': gait_speed_ms,
            'stride_width_cm': stride_width_cm,
            'right_heel_strikes': r_heel_strikes,
            'left_heel_strikes': l_heel_strikes
        }
        
    except Exception as e:
        print("Error during gait analysis:", str(e))
        return {
            'status': 'error',
            'message': str(e)
        }
if __name__ == "__main__":
    # Specify the input TRC file path and output directory
    trc_path = r'D:\Miro Hernandez\Documents\openpose-1.7.0-binaries-win64-gpu-python3.7-flir-3d_recommended\Statistics test\BatchSession_Ronnel\T05_normal_1.7\pose-3d\T05_normal_1_filt_butterworth_on_speed.trc'
    # output_path = r'D:\Miro Hernandez\Documents\openpose-1.7.0-binaries-win64-gpu-python3.7-flir-3d_recommended\Statistics test\Spatio temporal Kinematics\Ronnel'
    
    print(f"Processing TRC file at {trc_path}")
    results = analyze_gait(trc_path)
    
    if results['status'] == 'success':
        # Print out the metrics
        print(f"Dynamic stride length: {results['stride_length_cm']:.2f} cm")
        print(f"Stride time: {results['stride_time_s']:.2f} s")
        print(f"Gait speed: {results['gait_speed_ms']:.2f} m/s")
        print(f"Stride width: {results['stride_width_cm']:.2f} cm")
        print(f"Right heel strikes at frames: {results['right_heel_strikes']}")
        print(f"Left heel strikes at frames: {results['left_heel_strikes']}")
        
        # # Create the output CSV file name based on the input file name
        # base = os.path.basename(trc_path)
        # filename_no_ext, _ = os.path.splitext(base)
        # output_filename = f"{filename_no_ext}.csv"
        # full_output_path = os.path.join(output_path, output_filename)
        
        # # Prepare a DataFrame with the desired results and headers
        # df_out = pd.DataFrame({
        #     "Dynamic stride length (cm)": [results['stride_length_cm']],
        #     "Stride time (s)": [results['stride_time_s']],
        #     "Gait speed (m/s)": [results['gait_speed_ms']],
        #     "Stride width (cm)": [results['stride_width_cm']]
        # })
        # df_out.to_csv(full_output_path, index=False)
        # print(f"Results saved to {full_output_path}")
    else:
        print("Gait analysis failed:", results['message'])
