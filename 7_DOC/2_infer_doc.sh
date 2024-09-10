#!/bin/bash

cd fairseq

DATA_ROOT=""
MODEL_DIR=""
GEN_SUBSET=""
RESULTS_PATH=""


fairseq-generate $DATA_ROOT \
  --config-yaml config.yaml --multitask-config-yaml config_multitask.yaml \
  --task doc_speech_to_speech --target-is-code --target-code-size 100 --vocoder code_hifigan \
  --path $MODEL_DIR/checkpoint_best.pt  --gen-subset $GEN_SUBSET \
  --max-tokens 25000 --max-target-positions 10000 \
  --beam 10 --max-len-a 1 \
  --results-path ${RESULTS_PATH} \
  --skip-invalid-size-inputs-valid-test \
  --use-imed --imed-gamma 0.5 --doc-context-size 1 \

echo "Job finished!"
