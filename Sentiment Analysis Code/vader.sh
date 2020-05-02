#!/bin/sh
#SBATCH --cpus-per-task=20
#SBATCH -o vader.out
#SBATCH --job-name=vader
python vader.py