#!/bin/bash

cd fairseq

AFS_DATA_ROOT="/work/tc062/tc062/s2517781/7_AFS/AFS_DATA_ROOT_1"
SAVE_DIR="/work/tc062/tc062/s2517781/7_AFS/ASR_BASELINE"

fairseq-train ${AFS_DATA_ROOT} --save-dir ${SAVE_DIR} \
  --config-yaml config.yaml --train-subset train --valid-subset dev \
  --num-workers 1 --max-tokens 40000 --max-update 400000 \
  --task speech_to_text --criterion label_smoothed_cross_entropy_with_ctc --label-smoothing 0.1 --report-accuracy \
  --arch zero_asr_transformer --share-decoder-input-output-embed \
  --optimizer adam --lr 2e-3 --lr-scheduler inverse_sqrt --warmup-updates 4000 \
  --clip-norm 10.0 --seed 1 --update-freq 4

echo "Job finished!"
