#!/bin/bash

# Define the directories
ROOT=$1
INPUT_FOLDER="$ROOT/clips"
OUTPUT_FOLDER1="$ROOT/train"
OUTPUT_FOLDER2="$ROOT/dev"
OUTPUT_FOLDER3="$ROOT/test"

# Ensure output directories exist
mkdir -p "$OUTPUT_FOLDER1"
mkdir -p "$OUTPUT_FOLDER2"
mkdir -p "$OUTPUT_FOLDER3"

# Initialize a counter
count=0

# Move the first 800 files to the train folder
for file in "$INPUT_FOLDER"/*; do
    if [ $count -ge 800 ]; then
        break
    fi

    # Get the base name of the file
    filename=$(basename "$file")
    
    # Move the file to the train folder
    mv "$file" "$OUTPUT_FOLDER1/$filename"

    # Increment the counter
    count=$((count + 1))
done

echo "Moved $count files to $OUTPUT_FOLDER1."

# Move the next 100 files to the dev folder
for file in "$INPUT_FOLDER"/*; do
    if [ $count -ge 900 ]; then
        break
    fi

    # Get the base name of the file
    filename=$(basename "$file")
    
    # Move the file to the dev folder
    mv "$file" "$OUTPUT_FOLDER2/$filename"

    # Increment the counter
    count=$((count + 1))
done

echo "Moved $((count - 800)) files to $OUTPUT_FOLDER2."

# Move the next 100 files to the test folder
for file in "$INPUT_FOLDER"/*; do
    if [ $count -ge 1000 ]; then
        break
    fi

    # Get the base name of the file
    filename=$(basename "$file")
    
    # Move the file to the test folder
    mv "$file" "$OUTPUT_FOLDER3/$filename"

    # Increment the counter
    count=$((count + 1))
done

echo "Moved $((count - 900)) files to $OUTPUT_FOLDER3."
