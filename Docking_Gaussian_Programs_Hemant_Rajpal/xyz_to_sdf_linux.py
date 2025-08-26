
import os
import subprocess

def validate_xyz_file(file_path):
    """ Validate and clean .xyz files. """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    atom_count = int(lines[0].strip())  # First line is the atom count
    atom_lines = lines[2:]  # Skip the second line (comment)

    # Check if the number of atom lines matches the count
    if len(atom_lines) != atom_count:
        print(f"Warning: Atom count mismatch in {file_path}. Expected {atom_count}, found {len(atom_lines)}. Fixing...")
        # Fix by updating the atom count to the correct number
        lines[0] = f"{len(atom_lines)}\n"
        with open(file_path, 'w') as file:
            file.writelines(lines)

    return True  # Return True if validation passes

def convert_xyz_to_sdf(input_dir, output_dir, obabel_path):
    """ Convert all valid .xyz files in the input directory to .sdf using Open Babel. """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Loop through all .xyz files in the input directory
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.xyz'):
            input_file = os.path.join(input_dir, file_name)
            output_file = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.sdf")

            # Validate the .xyz file structure
            if validate_xyz_file(input_file):
                # Construct the Open Babel command, explicitly specifying 'xyz' as the input format and generating 3D coordinates
                command = f'"{obabel_path}" -ixyz "{input_file}" -O "{output_file}" --gen3D'

                # Run the command and capture the output and errors
                try:
                    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    print(f"Converted {input_file} to {output_file}")
                    print(f"Open Babel Output: {result.stdout.decode()}")
                    print(f"Open Babel Errors: {result.stderr.decode()}")
                except subprocess.CalledProcessError as e:
                    print(f"Error converting {input_file}: {e}")
                    print(e.stderr.decode())
            else:
                print(f"Skipping {input_file} due to validation failure.")

# Define input and output directories and Open Babel executable path (Linux paths)
input_dir = '/home/hrajp2/test_coconut_200/xyz'
output_dir = '/home/hrajp2/test_coconut_200/xyz/sdf'
obabel_path = '/usr/bin/obabel'  # Adjust this if Open Babel is installed in another location

# Convert all .xyz files to .sdf with 3D coordinate generation
convert_xyz_to_sdf(input_dir, output_dir, obabel_path)

print(f"Conversion complete. SDF files saved to {output_dir}")