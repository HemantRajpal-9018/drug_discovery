import os

class ConvertToGauss:
    def __init__(self, mol2_file, result_folder_name):
        self.mol2_file = mol2_file
        self.result_folder_name = result_folder_name

    def fWriteFile(self, fileName, lines):
        with open(fileName, 'w') as f:
            f.writelines(lines)

    def convert(self):
        if not os.path.exists(self.result_folder_name):
            os.makedirs(self.result_folder_name)

        # Check if the MOL2 file exists
        if not os.path.exists(self.mol2_file):
            print(f"Error: MOL2 file not found at {self.mol2_file}")
            return
        
        with open(self.mol2_file, 'r') as file:
            lines = file.readlines()

        # Split the MOL2 file into individual structures
        structures = []
        current_structure = []
        for line in lines:
            if line.startswith('@<TRIPOS>MOLECULE') and current_structure:
                structures.append(current_structure)
                current_structure = []
            current_structure.append(line)
        if current_structure:
            structures.append(current_structure)

        print(f"Found {len(structures)} structures in the MOL2 file.")

        file_num = 1
        for structure in structures:
            final_write_lines = []

            # Add Gaussian header
            final_write_lines.append(f"%chk=gaussian_input{file_num}.chk\n")
            final_write_lines.append("# b3lyp/6-31+g(d) freq\n")
            final_write_lines.append("\n")
            final_write_lines.append("Gaussian Input for Frequency Analysis\n")
            final_write_lines.append("\n")
            # Charge and multiplicity, set default values or modify as needed
            charge = 0  # Default charge
            multiplicity = 1  # Default multiplicity

            final_write_lines.append(f"{charge} {multiplicity}\n")

            # Add atoms from MOL2 file
            atom_section = False
            for line in structure:
                if line.startswith('@<TRIPOS>ATOM'):
                    atom_section = True
                    continue
                if line.startswith('@<TRIPOS>BOND'):
                    break
                if atom_section:
                    # Parse atom line and write to Gaussian input format
                    parts = line.split()
                    if len(parts) >= 6:
                        # Extract only the element symbol (remove the ".x" part)
                        atom_symbol = parts[5].split('.')[0]
                        x, y, z = parts[2], parts[3], parts[4]
                        final_write_lines.append(f"{atom_symbol} {x} {y} {z}\n")
            
            final_write_lines.append("\n")

            # Write to Gaussian input file
            write_file_name = os.path.join(self.result_folder_name, f"gauss_input{file_num}.gjf")
            self.fWriteFile(write_file_name, final_write_lines)
            print(f"Writing Gaussian input file {file_num}: {write_file_name}")
            file_num += 1

# Usage
mol2_file_path = r'C:\Users\heman\OneDrive\Desktop\coconut_200\combined_output.mol2'
result_folder_name = r'C:\Users\heman\OneDrive\Desktop\coconut_200\gaussian_inputs'

converter = ConvertToGauss(mol2_file_path, result_folder_name)
converter.convert()
