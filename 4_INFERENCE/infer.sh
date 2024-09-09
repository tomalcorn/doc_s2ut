#!/bin/bash

cd fairseq

DATA_ROOT=""
MODEL_DIR=""
GEN_SUBSET="test"
RESULTS_PATH=""

fairseq-generate $DATA_ROOT \
  --config-yaml config.yaml --multitask-config-yaml config_multitask.yaml \
  --task speech_to_speech --target-is-code --target-code-size 100 --vocoder code_hifigan \
  --path $MODEL_DIR/checkpoint_best.pt  --gen-subset $GEN_SUBSET \
  --max-tokens 50000 \
  --beam 10 --max-len-a 1 \
  --results-path ${RESULTS_PATH}

echo "Job finished!"
