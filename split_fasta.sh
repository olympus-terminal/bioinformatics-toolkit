#!/bin/bash

# Variables
INPUT_FASTA="input.fasta"
SEQUENCES_PER_FILE=1000
PREFIX="split"

# Split fasta maintaining headers
awk -v prefix="${PREFIX}" -v size="${SEQUENCES_PER_FILE}" '
/^>/ {
    if (count % size == 0) {
        if (out) close(out)
        file_num = int(count / size) + 1
        out = sprintf("%s_%04d.fasta", prefix, file_num)
    }
    count++
}
{print > out}
' "${INPUT_FASTA}"

echo "Splitting complete"
