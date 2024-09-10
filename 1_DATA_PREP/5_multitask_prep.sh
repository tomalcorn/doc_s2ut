#!/bin/bash

# Check if the correct number of arguments is passed
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <data-root> <task-dict> <splits>"
    echo "Example: $0 /path/to/data \"{'decoder_target_ctc':'TGT_AUDIO_EP/', 'source_letter':'SRC_AUDIO_EP/', 'target_letter':'TGT_AUDIO_EP/'}\" \"['train', 'dev']\""
    exit 1
fi

# Assign arguments to variables
DATA_ROOT_PATH=""
MANIFEST_DIR_PATH=""

# dictionary string in the form {'$multitask': 'SRC_AUDIO/'|'TGT_AUDIO/', for each multitask}
# Currently available multitasks: decoder_tgt_ctc, source_letter, target_letter
TASK_DICT=""

# Comma separated splits eg train,dev,test
SPLITS=""

# Run the Python script with the provided arguments
python3 ./1_DATA_PREP/fairseq_dict_maker.py \
    --data-root $DATA_ROOT_PATH \
    --manifest-dir $MANIFEST_DIR_PATH \
    --task-dict "$TASK_DICT" \
    --splits "$SPLITS"