#!/bin/bash

cd fairseq

# Name of folder in ./4_INFERENCE/results
VARIANT=""

DATA_ROOT=""
COMET_CKPT=""
SPEECH=false

echo "running python script..."
nvidia-smi --loop=10 --filename=out-nvidia-smi.txt &
srun python ./5_EVALUATION/score.py --tgt $VARIANT \
    --data-root $DATA_ROOT --comet-ckpt $COMET_CKPT --use-comet


if [ $SPEECH = true ]; then
    echo scoring document...

    srun python ./5_EVALUATION/join_segments.py \
        --variant $VARIANT --data-root $DATA_ROOT
    VARIANT="${VARIANT}_speech"
    
    srun python ./5_EVALUATION/score.py --tgt $VARIANT \
    --data-root $DATA_ROOT --comet-ckpt $COMET_CKPT --use-comet
fi 

echo "Job finished!"