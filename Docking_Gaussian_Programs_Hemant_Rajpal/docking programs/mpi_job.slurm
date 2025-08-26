#!/bin/bash
#SBATCH --job-name=mpi_ligand_processing
#SBATCH --output=/home/hrajp2/test_coconut_200/docking/mpi_output-%j.out
#SBATCH --error=/home/hrajp2/test_coconut_200/docking/mpi_error-%j.err
#SBATCH --partition=PE2950
#SBATCH --ntasks=8
#SBATCH --nodes=5
#SBATCH --time=120:00:00




PYTHON_PATH=/usr/bin/python3
MPI4PY_PATH=/usr/lib/python3/dist-packages/mpi4py/__init__.py




cd  /home/hrajp2/test_coconut_200/docking

# Check if the file list exists
FILE_LIST="/home/hrajp2/test_coconut_200/docking/ligand.txt"
if [ ! -f "$FILE_LIST" ]; then
    echo "File list $FILE_LIST does not exist."
    exit 1
fi




# Run the MPI Python script
mpiexec -n $SLURM_NTASKS $PYTHON_PATH  /home/hrajp2/test_coconut_200/docking/mpi4.py /home/hrajp2/test_coconut_200/docking/ligand.txt



