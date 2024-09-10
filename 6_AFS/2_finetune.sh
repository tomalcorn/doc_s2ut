#!/bin/bash

cd fairseq

PRETRAIN_CKPT=""
AFS_DATA_ROOT=""
SAVE_DIR=""

fairseq-train ${AFS_DATA_ROOT} --save-dir ${SAVE_DIR} \
  --config-yaml config.yaml --train-subset train --valid-subset dev \
  --num-workers 1 --max-tokens 40000 --max-updates 5000 \
  --task speech_to_text --criterion label_smoothed_cross_entropy_with_l0 --label-smoothing 0.1 --report-accuracy \
  --arch zero_asr_afs_transformer --load-pretrained-encoder-from $PRETRAIN_CKPT --load-pretrained-decoder-from $PRETRAIN_CKPT \
  --share-decoder-input-output-embed \
  --optimizer adam --lr 2e-3 --lr-scheduler inverse_sqrt --warmup-updates 4000 \
  --clip-norm 10.0 --seed 1 --save-interval 1  \
  --l0-norm-reg-scalar 0.5 --l0-norm-warm-up --l0-norm-end-reg-ramp-up 1000 \
  --enable-afs-t --enable-afs-f

echo "Job finished!" 
