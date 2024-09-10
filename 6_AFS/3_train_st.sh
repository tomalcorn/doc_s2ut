#!/bin/bash

cd fairseq

DATA_ROOT="/work/tc062/tc062/s2517781/DATA_ROOT"
SAVE_DIR="/work/tc062/tc062/s2517781/2_TRAINING/models/BASELINE_AFS_1.0"
FEAT_EXTRACTOR="/work/tc062/tc062/s2517781/7_AFS/ASR_AFS_SAVE_BIG/checkpoint_best.pt"
FEAT_EXTRACTOR_ARGS=""

fairseq-train $DATA_ROOT \
  --config-yaml config.yaml --multitask-config-yaml config_multitask.yaml \
  --task speech_to_speech --target-is-code --target-code-size 100 --vocoder code_hifigan  \
  --criterion speech_to_unit --label-smoothing 0.2 \
  --arch s2ut_transformer_afs --conv-version afs --feat-extractor-pretraining-path $FEAT_EXTRACTOR \
  --feat-extractor-args $FEAT_EXTRACTOR_ARGS --share-decoder-input-output-embed \
  --dropout 0.1 --attention-dropout 0.1 --relu-dropout 0.1 \
  --train-subset train --valid-subset dev \
  --save-dir ${SAVE_DIR} \
  --lr 0.0005 --lr-scheduler inverse_sqrt --warmup-init-lr 1e-7 --warmup-updates 10000 \
  --optimizer adam --adam-betas "(0.9,0.98)" --clip-norm 10.0 \
  --max-update 400000 --max-tokens 20000 --update-freq 4 \
  --seed 1 --fp16 --num-workers 8 --save-interval 10

echo "Job finished!"
