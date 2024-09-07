#!/bin/bash

# Define the directories
INPUT_FOLDER1="/Users/tomalcorn/Documents/University/pg/diss/mine/data/es/clipsslim"
INPUT_FOLDER2="/Users/tomalcorn/Documents/University/pg/diss/mine/data/en/clipsslim"
OUTPUT_FOLDER1="/Users/tomalcorn/Documents/University/pg/diss/SRC_AUDIO/clips"
OUTPUT_FOLDER2="/Users/tomalcorn/Documents/University/pg/diss/TGT_AUDIO/clips"

# Ensure output directories exist
mkdir -p "$OUTPUT_FOLDER1"
mkdir -p "$OUTPUT_FOLDER2"

# Initialize a counter
count=0

# Loop through the first 1000 files in input_folder1
for file1 in "$INPUT_FOLDER1"/*; do
    if [ $count -ge 1000 ]; then
        break
    fi

    # Get the base name of the file
    filename=$(basename "$file1")

    # Check if the same file exists in input_folder2
    if [ -e "$INPUT_FOLDER2/$filename" ]; then
        # Copy the file from input_folder1 to output_folder1
        cp "$file1" "$OUTPUT_FOLDER1/$filename"

        # Copy the file from input_folder2 to output_folder2
        cp "$INPUT_FOLDER2/$filename" "$OUTPUT_FOLDER2/$filename"

        # Increment the counter
        count=$((count + 1))
    fi
done

echo "Copied $count files from input_folder1 and input_folder2 to output_folder1 and output_folder2 respectively."
