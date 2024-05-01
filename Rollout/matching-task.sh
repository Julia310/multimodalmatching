#!/bin/bash

#SBATCH --time=48:00:00
#SBATCH --mem=50G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --job-name="Matching task"
#SBATCH --partition=clara-job
#SBATCH --gres=gpu:rtx2080ti:2

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
python3 multimodalmatching/main.py
