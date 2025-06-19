#!/bin/bash
#SBATCH -o slurm-logs/arrayJob_%A_%a.out
#SBATCH -e slurm-logs/arrayJob_%A_%a.err
#SBATCH -a 1-12
#SBATCH -n 1
#SBATCH --cpus-per-task=2
#SBATCH --mem=16GB
#SBATCH --time=24:00:00

LINE=$(sed -n "$SLURM_ARRAY_TASK_ID"p fa-files.txt)
echo $LINE

sed -i 's/\./_/g' $LINE;
sed -i 's/ /_/g' $LINE;
sed -i 's/,/_/g' $LINE;
sed -i 's/)/_/g' $LINE;
sed -i 's/(/_/g' $LINE;
sed -i 's/:/_/g' $LINE; 

perl filter-on-length.pl -minlen 1000 $LINE > "$LINE"-1kb.fa
