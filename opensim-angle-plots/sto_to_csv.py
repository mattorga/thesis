import csv

# Input: OpenSim Storage (.sto) generated file containing the joint angles
# Output: CSV file with only the following columns:
#    time, hip_flexion, knee_angle, ankle_angle
def parse_sto_file(input_file_path, output_file_path):
    headers = []
    data = []
    column_indices = []

    columns_to_extract = ['time', 'hip_flexion_r', 'knee_angle_r', 'ankle_angle_r', 
                      'hip_flexion_l', 'knee_angle_l', 'ankle_angle_l']
    
    # Read the .sto file
    with open(input_file_path, 'r') as file:
        # Skip header information
        for line in file:
            if line.startswith('endheader'):
                break
        
        # Use csv reader with tab delimiter
        reader = csv.reader(file, delimiter='\t')
        
        # Read headers
        all_headers = next(reader)
        all_headers = [header.strip() for header in all_headers if header.strip()]
        
        # Find indices of columns to extract
        column_indices = [all_headers.index(col) for col in columns_to_extract if col in all_headers]
        headers = [all_headers[i] for i in column_indices]
        
        # Read data
        for row in reader:
            # Remove any empty strings, convert to float, and extract only specified columns
            row_data = [float(row[i]) for i in column_indices if i < len(row) and row[i].strip()]
            if len(row_data) == len(column_indices):  # Only append rows with all required data
                data.append(row_data)
    
    # Write to CSV file
    with open(output_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write headers
        writer.writerows(data)    # Write data rows
    
    return headers, data

# Example usage
input_file_path = '/Users/mattheworga/Documents/Git/DLSU/thesis/database/S01_V501/S01_P04_Yu/S01_P04_T01/simulation/walking.sto'
output_file_path = '/Users/mattheworga/Documents/Git/DLSU/thesis/opensim-angle-plots/test_output_filtered.csv'


headers, parsed_data = parse_sto_file(input_file_path, output_file_path)

print("Extracted Headers:", headers)
print("Number of data rows:", len(parsed_data))
print("First data row:", parsed_data[0] if parsed_data else "No data")
print(f"Data has been written to {output_file_path}")