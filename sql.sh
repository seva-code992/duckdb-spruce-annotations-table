#!/bin/bash
#SBATCH --job-name=DuckDB
#SBATCH --output=output_ii.txt
#SBATCH --time=10:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G

duckdb test.db
duckdb test.db -f spruce.sql
duckdb test.db -f cosine_similarity.sql 
