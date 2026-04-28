#!/bin/bash
#SBATCH -t 10:00:00
#SBATCH -n 1
#SBATCH --output=output.txt

python3 main.py