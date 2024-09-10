#!/bin/bash

# Check if the correct number of arguments is passed
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <manifest-dir> <root-dir> <lang-code> <split>"
    exit 1
fi

# Absolute path to DATA_ROOT
DATA_ROOT=""

# train, dev, test etc
SPLIT=""

# Path to SRC_AUDIO or TGT_AUDIO directories
AUDIO_DIR=""
AUDIO_DIR="${AUDIO_DIR}/${SPLIT}"

# Short code for source or target language
LANG_CODE=""

# Run the Python script with the provided arguments
python3 1_DATA_PREP/manifest_maker.py \
    --manifest-dir "$DATA_ROOT" \
    --audio-dir "$AUDIO_DIR" \
    --lang-code "$LANG_CODE" \
    --split "$SPLIT"