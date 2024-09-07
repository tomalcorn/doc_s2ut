#!/bin/bash

# Ensure the script is being called with the correct number of arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <source_directory> <target_directory>"
    exit 1
fi

# Define source and target directories
true_source=$1
target_dir=$2

# Subdirectories to process
subdirs=("train" "dev" "test")

# Create the target subdirectories if they don't exist
for subdir in "${subdirs[@]}"; do
    mkdir -p "$target_dir/$subdir"
done

# Create symbolic links for files from each subdirectory
for subdir in "${subdirs[@]}"; do
    find "$true_source/$subdir" -type f | while read -r file; do
        ln -s "$file" "$target_dir/$subdir/$(basename "$file")"
    done
done

echo "Symbolic links created successfully."
