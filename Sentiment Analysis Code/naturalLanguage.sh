#!/bin/sh

#SBATCH --cpus-per-task=20
#SBATCH -o nltk.out
#SBATCH --job-name=nltk
python naturalLanguage.py