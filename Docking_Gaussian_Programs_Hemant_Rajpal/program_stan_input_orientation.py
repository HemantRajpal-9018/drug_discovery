import os

def extract_orientation(input_file, output_file):
    # Initialize variables to store data
    coordinates_block = []
    extract = False
    header_written = False
    input_orientation_found = False

    # Headers for input and standard orientations
    input_header = """                         Input orientation:                          
 ---------------------------------------------------------------------
 Center     Atomic      Atomic             Coordinates (Angstroms)
 Number     Number       Type             X           Y           Z
 ---------------------------------------------------------------------"""

    standard_header = """                         Standard orientation:                          
 ---------------------------------------------------------------------
 Center     Atomic      Atomic             Coordinates (Angstroms)
 Number     Number       Type             X           Y           Z
 ---------------------------------------------------------------------"""

    # Open and read the input file
    with open(input_file, 'r') as file:
        for line in file:
            # Start extracting after 'Input orientation:'
            if 'Input orientation:' in line and not header_written:
                extract = True
                input_orientation_found = True  # Mark that Input orientation was found
                coordinates_block.append(input_header)
                header_written = True  # Ensure header is written only once
            # Stop extracting when 'Distance matrix' or other unrelated sections are reached
            elif 'Distance matrix' in line or 'Rotational constants' in line:
                break
            # Extract the data when in extraction mode, skip extra headers
            elif extract:
                if 'Center     Atomic' in line or 'Number     Number' in line or '------' in line:
                    continue
                coordinates_block.append(line.strip())

    # If Input orientation was not found, search for Standard orientation
    if not input_orientation_found:
        with open(input_file, 'r') as file:
            for line in file:
                # Start extracting after 'Standard orientation:'
                if 'Standard orientation:' in line and not header_written:
                    extract = True
                    coordinates_block.append(standard_header)
                    header_written = True  # Ensure header is written only once
                # Stop extracting when 'Distance matrix' or other unrelated sections are reached
                elif 'Distance matrix' in line or 'Rotational constants' in line:
                    break
                # Extract the data when in extraction mode, skip extra headers
                elif extract:
                    if 'Center     Atomic' in line or 'Number     Number' in line or '------' in line:
                        continue
                    coordinates_block.append(line.strip())

    # Write the extracted block to the output file
    with open(output_file, 'w') as output_file:
        for line in coordinates_block:
            output_file.write(line + '\n')

def process_multiple_logs(input_dir, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Loop through all files in the input directory
    for file_name in os.listdir(input_dir):
        # Process only .log or appropriate files
        if file_name.endswith('.log'):
            input_file = os.path.join(input_dir, file_name)
            output_file = os.path.join(output_dir, f'{os.path.splitext(file_name)[0]}_input_orientation.txt')

            # Call the extraction function for each log file
            extract_orientation(input_file, output_file)
            print(f"Processed {file_name} and saved input/standard orientation to {output_file}")

# Define the input and output directories
input_dir = r'C:\Users\heman\OneDrive\Desktop\coconut_200\output_gaussian'
output_dir = r'C:\Users\heman\OneDrive\Desktop\coconut_200\input_orientations'

# Process all log files in the input directory
process_multiple_logs(input_dir, output_dir)

print(f"All input/standard orientations have been extracted to {output_dir}")
