#!/bin/bash


# Assign arguments to variables
DATA_ROOT_PATH=""
SRC_AUDIO_PATH=""
TGT_AUDIO_PATH=""

# Comma separated multitasks. Currently available multitasks: decoder_target_ctc, source_letter, target_letter
TASK_DICT=""

# Comma separated splits eg train,dev,test
SPLITS="train,dev,test"

# Run the Python script with the provided arguments
python3 ./1_DATA_PREP/fairseq_dict_maker.py \
    --data-root $DATA_ROOT_PATH \
    --tasks "$TASK_DICT" \
    --src-audio "$SRC_AUDIO_PATH" \
    --tgt-audio "$TGT_AUDIO_PATH" \
    --splits "$SPLITS"