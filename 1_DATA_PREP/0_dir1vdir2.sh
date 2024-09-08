#!/bin/bash

# Define the directories
DIR1="/work/tc062/tc062/s2517781/SRC_AUDIO_EP/test"
DIR2="/work/tc062/tc062/s2517781/TGT_AUDIO_EP/test"
BACKUPDIR1="/work/tc062/tc062/s2517781/SRC_AUDIO_EP/test_backup"
BACKUPDIR2="/work/tc062/tc062/s2517781/TGT_AUDIO_EP/test_backup"

# Ensure backup directories exist
mkdir -p "$BACKUPDIR1"
mkdir -p "$BACKUPDIR2"

# Find files in DIR1 that are not in DIR2 and move them to BACKUPDIR1
for file in "$DIR1"/*; do
    filename=$(basename "$file")
    if [ ! -e "$DIR2/$filename" ]; then
        echo "Moving $file to $BACKUPDIR1"
        mv "$file" "$BACKUPDIR1"
    fi
done

# Find files in DIR2 that are not in DIR1 and move them to BACKUPDIR2
for file in "$DIR2"/*; do
    filename=$(basename "$file")
    if [ ! -e "$DIR1/$filename" ]; then
        echo "Moving $file to $BACKUPDIR2"
        mv "$file" "$BACKUPDIR2"
    fi
done

echo "Files not present in both directories have been moved to their respective backup directories."
