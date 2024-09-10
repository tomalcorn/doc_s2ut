#!/bin/bash

cd fairseq

LS_ROOT=""
SUBSET="test"
SAVE_DIR=""
CHECKPOINT_FILENAME=""

fairseq-generate ${LS_ROOT} --config-yaml config.yaml --gen-subset ${SUBSET} \
    --task speech_to_text --path ${SAVE_DIR}/${CHECKPOINT_FILENAME} \
    --max-tokens 50000 --beam 10 --scoring wer --skip-invalid-size-inputs-valid-test

echo "Job finished!"
