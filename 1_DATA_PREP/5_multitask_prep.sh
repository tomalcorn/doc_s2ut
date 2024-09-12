#!/bin/bash


# Assign arguments to variables
DATA_ROOT_PATH=""

# dictionary string in the form "{'$multitask': 'SRC_AUDIO/'|'TGT_AUDIO/', for each multitask}"
# Currently available multitasks: decoder_target_ctc, source_letter, target_letter
TASK_DICT=""

# Comma separated splits eg train,dev,test
SPLITS="train,dev,test"

# Run the Python script with the provided arguments
python3 ./1_DATA_PREP/fairseq_dict_maker.py \
    --data-root $DATA_ROOT_PATH \
    --task-dict "$TASK_DICT" \
    --splits "$SPLITS"