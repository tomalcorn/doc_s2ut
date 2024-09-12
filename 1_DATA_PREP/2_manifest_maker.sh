#!/bin/bash

# Path to DATA_ROOT
DATA_ROOT=""

# comma separated list of splits, e.g "train,dev,test"
SPLITS=""

# ABSOLOLUTE Path to SRC_AUDIO or TGT_AUDIO directories
AUDIO_DIR=""

# Short code for source or target language
LANG_CODE=""

IFS=','
for split in $SPLITS; do
    CURRENT_AUDIO_DIR="${AUDIO_DIR}/${split}"
    # Run the Python script with the provided arguments
    python3 ./1_DATA_PREP/manifest_maker.py \
        --manifest-dir "$DATA_ROOT" \
        --audio-dir "$CURRENT_AUDIO_DIR" \
        --lang-code "$LANG_CODE" \
        --split "$split"
done

echo "Job finished!"