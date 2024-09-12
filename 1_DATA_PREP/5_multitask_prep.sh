#!/bin/bash


# Assign arguments to variables
DATA_ROOT_PATH="/Users/tomalcorn/Documents/University/pg/github_practice/doc_s2ut/DATA_ROOT"

# dictionary string in the form "{'$multitask': 'SRC_AUDIO/'|'TGT_AUDIO/', for each multitask}"
# Currently available multitasks: decoder_tgt_ctc, source_letter, target_letter
TASK_DICT="{'source_letter': 'SRC_AUDIO', 'target_letter': 'TGT_AUDIO', 'decoder_tgt_ctc': 'TGT_AUDIO'}"

# Comma separated splits eg train,dev,test
SPLITS="train,dev,test"

# Run the Python script with the provided arguments
python3 ./fairseq_dict_maker.py \
    --data-root $DATA_ROOT_PATH \
    --task-dict "$TASK_DICT" \
    --splits "$SPLITS"