#!/bin/bash
#SBATCH -t 10:00:00
#SBATCH -n 1
#SBATCH --output=output.txt

uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
uv run main.py