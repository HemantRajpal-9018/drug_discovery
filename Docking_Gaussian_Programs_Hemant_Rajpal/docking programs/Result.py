import re
import csv
import os

def parse_result_file(result_file):
    ligand_data = {}
    current_ligand = None
    reading_data = False  # Flag to start reading numeric data after the header

    # Check if file exists
    if not os.path.exists(result_file):
        print(f"Error: File '{result_file}' not found.")
        return ligand_data

    with open(result_file, 'r') as file:
        lines = file.readlines()

        for line in lines:
            # Print the line for debugging
            print(f"Processing line: {line.strip()}")

            # Skip any empty lines
            if line.strip() == "":
                continue

            # Match log file names like 'gauss_input10_log.log'
            match = re.match(r"==>\s+(gauss_input\d+)_log\.log\s+<==", line)
            if match:
                current_ligand = match.group(1)
                print(f"Found ligand: {current_ligand}")
                ligand_data[current_ligand] = []
                reading_data = False  # Reset reading flag when a new ligand is found
            elif current_ligand is not None:
                # Look for the header in the log file and set the flag to start reading data
                if "kcal/mol" in line and "rmsd" in line:
                    print("Header found, starting to read pose data.")
                    reading_data = True
                    continue  # Skip header

                # If we are past the header, read the numeric data
                if reading_data:
                    columns = line.strip().split()
                    print(f"Columns: {columns}")

                    # Validate columns: Check for 4 numeric values (pose, affinity, rmsd l.b., rmsd u.b.)
                    if len(columns) == 4 and all(re.match(r'-?\d*\.?\d+', column) for column in columns):
                        ligand_data[current_ligand].append(columns)
                        print(f"Pose data added for {current_ligand}: {columns}")
                    else:
                        print(f"Skipping non-numeric or invalid line: {line.strip()}")

    # Rank poses based on the second column (affinity)
    for ligand_name, poses_data in ligand_data.items():
        ligand_data[ligand_name] = sorted(poses_data, key=lambda x: float(x[1]))

    return ligand_data

def write_csv(ligand_data, output_file):
    # Check if there is data to write
    if not ligand_data:
        print("No ligand data found, skipping CSV generation.")
        return

    # Write CSV file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Ligand Name', 'Pose', 'Affinity', 'RMSD (Lower Bound)', 'RMSD (Upper Bound)'])

        for ligand_name, poses_data in ligand_data.items():
            for pose, affinity, rmsd_lb, rmsd_ub in poses_data:
                writer.writerow([ligand_name, pose, affinity, rmsd_lb, rmsd_ub])

    print(f"CSV file '{output_file}' generated successfully.")

if __name__ == "__main__":
    # Input result file and output CSV file paths
    result_file = r'C:\Users\heman\OneDrive\Desktop\coconut_200\docking\results.txt'
    output_file = r'C:\Users\heman\OneDrive\Desktop\coconut_200\docking\output.csv'

    # Parse the result file and generate ligand data
    ligand_data = parse_result_file(result_file)

    # Debug: Show parsed data
    print("Parsed Ligand Data: ", ligand_data)

    # Check if valid data was parsed, then write to CSV
    if ligand_data:
        write_csv(ligand_data, output_file)
    else:
        print(f"No valid ligand data found in '{result_file}'. Please verify the file format.")
