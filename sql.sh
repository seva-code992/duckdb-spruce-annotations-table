#!/bin/bash
#SBATCH --job-name=DuckDB
#SBATCH --output=output_ii.txt
#SBATCH --time=10:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4      #Opt: Up to 20
#SBATCH --mem=16G          #Opt: Up to 32G
#SBATCH --gres=gpu:tesla:1  #Opt: I could request both Tesla GPUs --gres=gpu:tesla:2  
#SBATCH --partition=gpu



duckdb test.db
duckdb test.db -f spruce.sql
duckdb test.db -f cosine_similarity.sql 
