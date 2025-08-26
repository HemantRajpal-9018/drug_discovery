#!/usr/bin/env python3

from mpi4py import MPI
import os
import subprocess

def run_gaussian(input_file, output_dir, log_dir, scratch_base_dir, rank):
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    scratch_dir = os.path.join(scratch_base_dir, f"{base_name}_{rank}")
    os.makedirs(scratch_dir, exist_ok=True)

    # Copy the input file to the scratch directory
    subprocess.run(["cp", input_file, scratch_dir])

    # Change to the scratch directory
    os.chdir(scratch_dir)

    # Set up Gaussian environment
    os.environ['g16root'] = '/home/gaussian'
    os.environ['GAUSS_SCRDIR'] = scratch_dir

    # Source Gaussian profile
    gaussian_profile = os.path.join(os.environ['g16root'], "g16/bsd/g16.profile")
    bash_command = f"source {gaussian_profile}; g16 {os.path.basename(input_file)}"

    print(f"Running Gaussian: {bash_command}")

    gaussian_process = subprocess.run(bash_command, shell=True, executable='/bin/bash', stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Check if Gaussian ran successfully
    if gaussian_process.returncode != 0:
        print(f"Error running Gaussian on {input_file}: {gaussian_process.stderr.decode()}")
    else:
        print(f"Gaussian ran successfully on {input_file}")

    # Write outputs to files
    output_file = os.path.join(output_dir, f"{base_name}.out")
    log_file = os.path.join(log_dir, f"{base_name}_log.log")
    with open(output_file, 'wb') as out_f:
        out_f.write(gaussian_process.stdout)
    with open(log_file, 'wb') as log_f:
        log_f.write(gaussian_process.stderr)

    # Move any additional output files to the output directory
    for file in os.listdir(scratch_dir):
        if file != os.path.basename(input_file):
            full_file_path = os.path.join(scratch_dir, file)
            if os.path.isfile(full_file_path):
                subprocess.run(["mv", full_file_path, output_dir])

    # Clean up the scratch directory
    os.chdir('/')
    subprocess.run(["rm", "-rf", scratch_dir])

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Main directories
main_dir = "/home/hrajp2/Test_coconut_50"
input_file_list = os.path.join(main_dir, "file_list1.txt")
output_dir = os.path.join(main_dir, "output_gaussian")
log_dir = os.path.join(main_dir, "logs")
scratch_base_dir = "/home/hrajp2/gaussian_scratch"

# Ensure output and log directories exist
if rank == 0:
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    # Read the file_list.txt to get input files
    with open(input_file_list, 'r') as f:
        gjf_files = [line.strip() for line in f.readlines() if line.strip().endswith('.gjf')]
else:
    gjf_files = None

# Broadcast the list of files to all processes
gjf_files = comm.bcast(gjf_files, root=0)

# Distribute files among processes
for i in range(rank, len(gjf_files), size):
    input_file = gjf_files[i]
    print(f"Process {rank} is processing {input_file}")
    run_gaussian(input_file, output_dir, log_dir, scratch_base_dir, rank)
    print(f"Process {rank} completed processing {input_file}")

# Synchronize processes
comm.Barrier()

if rank == 0:
    print("All processes have completed their tasks.")

