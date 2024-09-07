#!/bin/bash

SOURCE_DIR="/work/tc062/tc062/s2517781/TGT_AUDIO/train"
TARGET_DIR="/work/tc062/tc062/s2517781/mine/data/en/clipsslim"

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Source directory $SOURCE_DIR does not exist."
    exit 1
fi

# Check if target directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "Target directory $TARGET_DIR does not exist."
    exit 1
fi

# Create the target directory if it doesn't exist
mkdir -p "$TARGET_DIR"

# Move files using find and xargs
find "$SOURCE_DIR" -type f -print0 | xargs -0 -I {} mv {} "$TARGET_DIR"
