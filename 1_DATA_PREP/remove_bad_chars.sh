#!/bin/bash

# Ensure an input file and main directory are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input_file.txt> <main_directory>"
    exit 1
fi

input_file="$1"
main_directory="$2"

# Check if the input file exists
if [ ! -f "$input_file" ]; then
    echo "Input file not found: $input_file"
    exit 1
fi

# Check if the main directory exists
if [ ! -d "$main_directory" ]; then
    echo "Main directory not found: $main_directory"
    exit 1
fi

# Read the input file line by line
while IFS= read -r filename; do
    # Find and delete files matching the filename in the main directory and its subdirectories
    find "$main_directory" -type f -name "$filename" -exec rm -v {} \;
done < "$input_file"

echo "Process completed."
