#!/bin/bash

DATA_ROOT="/work/tc062/tc062/s2517781/DATA_ROOT_EP_DOC_TEST"
SAVE_DIR="/work/tc062/tc062/s2517781/12_DOC/models/doc_extended_loss_${VARIANT}"
PRETRAINING_PATH="/work/tc062/tc062/s2517781/2_TRAINING/models/BASELINE/checkpoint_best.pt"
FEAT_EXTRACTOR="/work/tc062/tc062/s2517781/7_AFS/ASR_AFS_${VARIANT}/checkpoint${CKPT}.pt"
FEAT_EXTRACTOR_ARGS="/work/tc062/tc062/s2517781/7_AFS/feat_extractor_args.tsv"

fairseq-train $DATA_ROOT \
  --config-yaml config.yaml --multitask-config-yaml config_multitask.yaml \
  --task doc_speech_to_speech --target-is-code --target-code-size 100 --vocoder code_hifigan  \
  --criterion doc_speech_to_unit --conv-version afs --feat-extractor-pretraining-path $FEAT_EXTRACTOR \
  --arch doc_s2ut_transformer --share-decoder-input-output-embed \
  --feat-extractor-args $FEAT_EXTRACTOR_ARGS --share-decoder-input-output-embed \
  --dropout 0.1 --attention-dropout 0.1 --relu-dropout 0.1 \
  --train-subset train --valid-subset dev \
  --save-dir ${SAVE_DIR} \
  --lr 0.00007 --lr-scheduler inverse_sqrt --warmup-init-lr 1e-7 --warmup-updates 10000 \
  --optimizer adam --adam-betas "(0.9,0.98)" --clip-norm 10.0 \
  --max-update 400000 --max-tokens 15000 --max-source-positions 5000 --max-target-positions 2048 \
  --update-freq 16  --seed 1 --num-workers 8 --max-epoch 800 --save-interval 10 \
  --pretraining-path ${PRETRAINING_PATH} --fp16  --skip-invalid-size-inputs-valid-test \
  --doc-context-size 1 --extended-loss


echo "Job finished!"
