#!/bin/bash

# Define file paths for the txt files
SPLIT1="/Users/tomalcorn/Documents/University/pg/diss/mine/data/es/training.txt"
SPLIT2="/Users/tomalcorn/Documents/University/pg/diss/mine/data/es/devving.txt"
SPLIT3="/Users/tomalcorn/Documents/University/pg/diss/mine/data/es/testing.txt"

# Define source and target directories
SRC_DIR="/Users/tomalcorn/Documents/University/pg/diss/mine/data/es/clips"
TGT_DIR="/Users/tomalcorn/Documents/University/pg/diss/mine/data/es/clipsslim"

# Create target directory if it doesn't exist
mkdir -p "$TGT_DIR"

# Read filenames from the txt files into a list
file_list=()
while IFS= read -r line; do file_list+=("$line"); done < "$SPLIT1"
while IFS= read -r line; do file_list+=("$line"); done < "$SPLIT2"
while IFS= read -r line; do file_list+=("$line"); done < "$SPLIT3"

# Convert list to a set for efficient lookup
file_set=$(printf "%s\n" "${file_list[@]}" | sort -u)

# Initialize counter for files not moved
not_moved_count=0

# Check all files in the source directory
for file in "$SRC_DIR"/*; do
    filename=$(basename "$file")
    if echo "$file_set" | grep -q "^$filename$"; then
        mv "$file" "$TGT_DIR"
    else
        ((not_moved_count++))
    fi
done

# Output the number of files that weren't moved
echo "$not_moved_count files were not moved."
