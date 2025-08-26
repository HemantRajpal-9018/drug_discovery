#!/bin/bash
#SBATCH --job-name=mpi_gaussian_processing
#SBATCH --output=/home/hrajp2/test_coconut_200/logs/mpi_output-%j.out
#SBATCH --error=/home/hrajp2/test_coconut_200/logs/mpi_error-%j.err
#SBATCH --partition=R250
#SBATCH --ntasks=8
#SBATCH --nodes=1
#SBATCH --time=120:00:00

# Define paths
PYTHON_PATH=/usr/bin/python3
WORKDIR=/home/hrajp2/test_coconut_200
GAUSSIAN_INPUT_DIR=$WORKDIR/gaussian_inputs
LOGDIR=$WORKDIR/logs
SCRATCH_BASE_DIR=/home/hrajp2/gaussian_scratch

# Set up Gaussian environment variables
export g16root=/home/gaussian
source $g16root/g16/bsd/g16.profile

# Check if Gaussian environment was sourced correctly
if [ $? -ne 0 ]; then
    echo "Failed to source Gaussian environment" >> $LOGDIR/mpi_error-$SLURM_JOB_ID.err
    exit 1
fi

# Create necessary directories
mkdir -p $LOGDIR
mkdir -p $SCRATCH_BASE_DIR

# Move to the working directory
cd $WORKDIR

# Run the MPI Python script to process Gaussian files
mpiexec -n $SLURM_NTASKS $PYTHON_PATH $WORKDIR/mpi_gaussian.py

# Check if the MPI job completed successfully
if [ $? -ne 0 ]; then
    echo "MPI job failed!" >> $LOGDIR/mpi_error-$SLURM_JOB_ID.err
else
    echo "MPI job completed successfully." >> $LOGDIR/mpi_output-$SLURM_JOB_ID.out
fi