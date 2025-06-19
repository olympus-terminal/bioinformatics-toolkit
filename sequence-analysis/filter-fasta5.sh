#!/bin/bash

input_file="$1"
base_name=$(basename "$input_file" .fa)
output_file="${base_name}_filtered.fa"

awk '/^>/ {if (len >= 200) print seq; print $0; seq=""; len=0; next} {seq = seq $0; len += length($0)} END {if (len >= 200) print seq}' "$input_file" > "$output_file"

echo "Filtering complete. Filtered sequences saved in $output_file"
