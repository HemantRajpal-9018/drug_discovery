#!/usr/bin/env python

import sys
from mpi4py import MPI
import subprocess
import time

def process_ligand(ligand, rank):
    ligand = ligand.strip()
    base_directory = "/home/hrajp2/test_coconut_200/docking"
    base_filename = ligand[:-6]  # Assuming ligand filenames end with '.pdbqt'
    output_file = f"{base_filename}_out.pdbqt"  # Output file with .pdbqt extension
    log_file = f"{base_filename}_log.log"  # Log file with .log extensio
    config_file = "/home/hrajp2/test_coconut_200/docking/conf.txt"
    receptor_file = "/home/hrajp2/test_coconut_200/docking/receptor.pdbqt"
    command = f"vina --config {config_file} --ligand {ligand} --receptor {receptor_file} --out {output_file}  > {log_file} 2>&1"
    subprocess.run(command, shell=True)

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        ligfile = "/home/hrajp2/test_coconut_200/docking/ligand.txt"
        try:
            with open(ligfile, "r") as file:
                files = file.readlines()
        except FileNotFoundError:
            print(f"File {ligfile} does not exist.")
            sys.exit(1)
        except Exception as e:
            print(f"An error occurred: {e}")
            sys.exit(1)
    else:
        files = None

    files = comm.bcast(files if files is not None else [], root=0)

    if not files:
        print("No files to process.")
        return

    start_time = time.time()

    for i in range(rank, len(files), size):
        process_ligand(files[i], rank)

    comm.Barrier()

    if rank == 0:
        total_time = time.time() - start_time
        print(f"Total time taken: {total_time} seconds")
        print(f"Number of files processed: {len(files)}")

if __name__ == "__main__":
    main()
