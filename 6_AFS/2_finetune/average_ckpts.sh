#!/bin/bash

cd fairseq

export PYTHONPATH=.:$PYTHONPATH

GLOBAL_ROOT="/work/tc062/tc062/s2517781/7_AFS"

# for value in $(seq 0.1 0.1 0.8); do
#     echo "Running Python script with value: $value"
#     MODEL_DIR="${GLOBAL_ROOT}/ASR_AFS_${value}"
#     OUTPUT="${MODEL_DIR}/checkpoint_avg.pt"

#     python3 scripts/average_checkpoints.py --inputs $MODEL_DIR --output ${OUTPUT} \
#     --num-epoch-checkpoints 5 --checkpoint-upper-bound 40
# done

value=0.1
echo "Running Python script with value: $value"
MODEL_DIR="${GLOBAL_ROOT}/ASR_AFS_${value}"
OUTPUT="${MODEL_DIR}/checkpoint_avg.pt"

python3 scripts/average_checkpoints.py --inputs $MODEL_DIR --output ${OUTPUT} \
--num-epoch-checkpoints 5 --checkpoint-upper-bound 40
done