import subprocess
import os

def convert_smiles_to_mol2(smiles, temp_input, error_log_file, obabel_path):
    """
    Converts a SMILES string to mol2 using Open Babel without force field minimization.
    Handles wildcard (*) by removing them from the SMILES.
    """
    # Remove wildcards (*) from the SMILES string
    cleaned_smiles = smiles.replace('*', '')  # Keep the structure, remove wildcards

    # Log the modification if any wildcards were found
    if '*' in smiles:
        print(f"Removed wildcard (*), proceeding with: {cleaned_smiles}")
        with open(error_log_file, 'a') as errfile:
            errfile.write(f"Removed * from SMILES: {smiles} -> {cleaned_smiles}\n")

    # Write the cleaned-up SMILES to a temporary input file
    with open(temp_input, 'w') as temp_in:
        temp_in.write(cleaned_smiles)

    # Run the Open Babel command to convert SMILES to mol2
    command = f'"{obabel_path}" -i smi "{temp_input}" -o mol2 --gen3d --addh'
    result = subprocess.run(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    if result.returncode == 0:
        print(f"Successfully converted: {cleaned_smiles}")
        return result.stdout
    else:
        # Log error if Open Babel failed
        with open(error_log_file, 'a') as errfile:
            errfile.write(f"Open Babel failed to convert: {cleaned_smiles}. Error: {result.stderr}\n")
        return None


def process_smiles_file(smiles_file, output_mol2_file, error_log_file, obabel_path):
    """
    Processes a SMILES file and writes all outputs into a single .mol2 file.
    """
    temp_input = "temp_smiles.smi"

    with open(output_mol2_file, 'w') as mol2_output:
        with open(smiles_file, 'r') as infile:
            for line in infile:
                smiles = line.strip()

                # Skip empty lines
                if not smiles:
                    continue

                # Convert the SMILES to MOL2
                mol2_data = convert_smiles_to_mol2(smiles, temp_input, error_log_file, obabel_path)

                # Write the converted MOL2 data to the output file if successful
                if mol2_data:
                    mol2_output.write(mol2_data)
                else:
                    print(f"Failed to process SMILES: {smiles}")

    # Clean up temporary files
    if os.path.exists(temp_input):
        os.remove(temp_input)


if __name__ == "__main__":
    # Path to the SMILES input file
    smiles_file = r'C:\Users\heman\OneDrive\Desktop\coconut_200\all.txt'

    # Path to the output mol2 file where all structures will be written
    output_mol2_file = r'C:\Users\heman\OneDrive\Desktop\coconut_200\combined_output.mol2'

    # Path to the error log file
    error_log_file = r'C:\Users\heman\OneDrive\Desktop\coconut_200\conversion_errors.log'

    # Path to Open Babel executable
    obabel_path = r"C:\Program Files\OpenBabel-3.1.1\obabel.exe"

    # Process the SMILES file and convert them all into one combined .mol2 file
    process_smiles_file(smiles_file, output_mol2_file, error_log_file, obabel_path)
