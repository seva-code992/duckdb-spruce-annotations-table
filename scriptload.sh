#!/bin/bash
#SBATCH --job-name=Embeddings
#SBATCH --output=output.txt
#SBATCH --time=10:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G

source .venv/bin/activate
uv run main.py
