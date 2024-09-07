#!/bin/bash

cd /Users/tomalcorn/Documents/University/pg/diss/fairseq

DATA_ROOT="/Users/tomalcorn/Documents/University/pg/diss/DATA_ROOT_FISHER"
MODEL_DIR="/Users/tomalcorn/Documents/University/pg/diss/2_TRAINING/models"
GEN_SUBSET="test"
RESULTS_PATH="/Users/tomalcorn/Documents/University/pg/diss/4_INFERENCE/inference_tiny"

fairseq-generate $DATA_ROOT \
  --config-yaml config.yaml --multitask-config-yaml config_multitask.yaml \
  --task speech_to_speech --target-is-code --target-code-size 100 --vocoder code_hifigan \
  --path $MODEL_DIR/checkpoint_best.pt  --gen-subset $GEN_SUBSET \
  --max-tokens 50000 \
  --beam 10 --max-len-a 1 \
  --results-path ${RESULTS_PATH}

echo "Job finished!"
