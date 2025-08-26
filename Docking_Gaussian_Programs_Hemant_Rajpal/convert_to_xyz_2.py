import os

# Atomic number to element symbol mapping (complete up to atomic number 118)
atomic_number_to_symbol = {
    1: 'H', 2: 'He', 3: 'Li', 4: 'Be', 5: 'B', 6: 'C', 7: 'N', 8: 'O', 9: 'F', 10: 'Ne',
    11: 'Na', 12: 'Mg', 13: 'Al', 14: 'Si', 15: 'P', 16: 'S', 17: 'Cl', 18: 'Ar', 19: 'K', 20: 'Ca',
    21: 'Sc', 22: 'Ti', 23: 'V', 24: 'Cr', 25: 'Mn', 26: 'Fe', 27: 'Co', 28: 'Ni', 29: 'Cu', 30: 'Zn',
    31: 'Ga', 32: 'Ge', 33: 'As', 34: 'Se', 35: 'Br', 36: 'Kr', 37: 'Rb', 38: 'Sr', 39: 'Y', 40: 'Zr',
    41: 'Nb', 42: 'Mo', 43: 'Tc', 44: 'Ru', 45: 'Rh', 46: 'Pd', 47: 'Ag', 48: 'Cd', 49: 'In', 50: 'Sn',
    51: 'Sb', 52: 'Te', 53: 'I', 54: 'Xe', 55: 'Cs', 56: 'Ba', 57: 'La', 58: 'Ce', 59: 'Pr', 60: 'Nd',
    61: 'Pm', 62: 'Sm', 63: 'Eu', 64: 'Gd', 65: 'Tb', 66: 'Dy', 67: 'Ho', 68: 'Er', 69: 'Tm', 70: 'Yb',
    71: 'Lu', 72: 'Hf', 73: 'Ta', 74: 'W', 75: 'Re', 76: 'Os', 77: 'Ir', 78: 'Pt', 79: 'Au', 80: 'Hg',
    81: 'Tl', 82: 'Pb', 83: 'Bi', 84: 'Po', 85: 'At', 86: 'Rn', 87: 'Fr', 88: 'Ra', 89: 'Ac', 90: 'Th',
    91: 'Pa', 92: 'U', 93: 'Np', 94: 'Pu', 95: 'Am', 96: 'Cm', 97: 'Bk', 98: 'Cf', 99: 'Es', 100: 'Fm',
    101: 'Md', 102: 'No', 103: 'Lr', 104: 'Rf', 105: 'Db', 106: 'Sg', 107: 'Bh', 108: 'Hs', 109: 'Mt',
    110: 'Ds', 111: 'Rg', 112: 'Cn', 113: 'Nh', 114: 'Fl', 115: 'Mc', 116: 'Lv', 117: 'Ts', 118: 'Og'
}

def reconstruct_smiles(atom_data):
    """
    Heuristically reconstruct a simple SMILES string from atom data.
    This is a basic approach and won't capture complex molecular structures.
    """
    smile_parts = []
    carbon_count = 0
    oxygen_count = 0

    for atom_symbol, x, y, z in atom_data:
        if atom_symbol == 'C':
            carbon_count += 1
        elif atom_symbol == 'O':
            oxygen_count += 1

    # Construct a simple SMILES based on the number of carbons and oxygens
    if carbon_count > 0:
        smile_parts.append('C' * carbon_count)
    if oxygen_count > 0:
        smile_parts.append('O' * oxygen_count)

    return ''.join(smile_parts) if smile_parts else "Unknown SMILES"

def convert_txt_to_xyz(input_file, output_file):
    atom_data = []
    file_name_without_ext = os.path.splitext(os.path.basename(input_file))[0]
    
    # Open the input file and read lines
    with open(input_file, 'r') as file:
        lines = file.readlines()

    read_coordinates = False
    for line in lines:
        # Skip known headers
        if "Number     Number       Type             X           Y           Z" in line or '------' in line:
            continue
        
        if "Coordinates" in line:
            read_coordinates = True
            continue
        
        # Check if the line contains atomic data
        if read_coordinates and len(line.split()) == 6:  # Expect 6 columns (Index, Atomic Number, Type, X, Y, Z)
            parts = line.split()
            try:
                atomic_number = int(parts[1])  # Extract atomic number
                x = float(parts[3])
                y = float(parts[4])
                z = float(parts[5])
                atom_symbol = atomic_number_to_symbol.get(atomic_number, 'X')  # Convert atomic number to symbol
                atom_data.append((atom_symbol, x, y, z))
            except ValueError:
                print(f"Skipping line due to invalid data: {line.strip()}")
                continue  # Skip lines with invalid data

    # Reconstruct SMILES based on the atomic data
    smiles_string = reconstruct_smiles(atom_data)

    # Write the XYZ file
    if atom_data:
        with open(output_file, 'w') as xyz_file:
            # Write the number of atoms
            xyz_file.write(f"{len(atom_data)}\n")
            # Write the input file name and SMILES string on the second line without ": ,"
            xyz_file.write(f"Input: {file_name_without_ext} SMILES: {smiles_string}\n")
            # Write the atoms with their coordinates
            for atom in atom_data:
                atom_symbol, x, y, z = atom
                xyz_file.write(f"{atom_symbol} {x:.6f} {y:.6f} {z:.6f}\n")
        print(f"Conversion complete. XYZ file saved to: {output_file}")
    else:
        print(f"No valid atom data found in {input_file}. Please check the input file format.")

def process_multiple_files(input_dir, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Loop through all files in the input directory
    for file_name in os.listdir(input_dir):
        if 'input_orientation' in file_name:  # Only process files with 'input_orientation' in the name
            input_file = os.path.join(input_dir, file_name)
            # Ensure the output file name ends with .xyz
            output_file = os.path.join(output_dir, f'{file_name.split("_input_orientation")[0]}.xyz')

            # Convert each file
            convert_txt_to_xyz(input_file, output_file)

# Define input and output directories
input_dir = r'C:\Users\heman\OneDrive\Desktop\coconut_200\input_orientations'
output_dir = r'C:\Users\heman\OneDrive\Desktop\coconut_200\xyz'

# Process all input_orientation files in the input directory
process_multiple_files(input_dir, output_dir)

print(f"All files have been processed and saved to {output_dir}")
