#!/bin/bash

cd /Users/tomalcorn/Documents/University/pg/diss/fairseq

DATA_ROOT="/Users/tomalcorn/Documents/University/pg/diss/DATA_ROOT_DOC"
MODEL_DIR="/Users/tomalcorn/Documents/University/pg/diss/12_DOC/models/test"
GEN_SUBSET="test"
RESULTS_PATH="/Users/tomalcorn/Documents/University/pg/diss/4_INFERENCE/doc_inference_test"
ATTN_SAVE_DIR="/Users/tomalcorn/Documents/University/pg/diss/12_DOC/3_attention/test"

fairseq-generate $DATA_ROOT \
  --config-yaml config.yaml --multitask-config-yaml config_multitask.yaml \
  --task doc_speech_to_speech --target-is-code --target-code-size 100 --vocoder code_hifigan \
  --path $MODEL_DIR/checkpoint_best.pt  --gen-subset $GEN_SUBSET \
  --max-tokens 1500 \
  --beam 2 --max-len-a 1 \
  --results-path ${RESULTS_PATH} \
  --doc-context-size 2 --attn-save-dir ${ATTN_SAVE_DIR}

echo "Job finished!"
