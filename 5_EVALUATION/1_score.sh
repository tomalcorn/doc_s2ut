#!/bin/bash

cd fairseq

VARIANT=""
DATA_ROOT=""
COMET_CKPT=""
SPEECH=false

echo "running python script..."
python ./5_EVALUATION/score.py --tgt $VARIANT \
    --data-root $DATA_ROOT --comet-ckpt $COMET_CKPT --use-comet


if [ $SPEECH = true ]; then
    echo scoring document...

    python ./5_EVALUATION/join_segments.py \
        --variant $VARIANT --data-root $DATA_ROOT
    VARIANT="${VARIANT}_speech"
    
    python ./5_EVALUATION/score.py --tgt $VARIANT \
    --data-root $DATA_ROOT --comet-ckpt $COMET_CKPT --use-comet
fi 

echo "Job finished!"