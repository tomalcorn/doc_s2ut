#!/bin/bash

cd fairseq

export PYTHONPATH=.:$PYTHONPATH

MODEL_DIR=""
OUTPUT="${MODEL_DIR}/checkpoint_avg.pt"

python3 scripts/average_checkpoints.py --inputs $MODEL_DIR --output ${OUTPUT} \
--num-epoch-checkpoints 5
done