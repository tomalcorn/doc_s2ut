#!/bin/bash


TGT="inference_afs_1"

TGT_FOLDER="/Users/tomalcorn/Documents/University/pg/diss/5_EVALUATION/text_out"
OUT_FOLDER="/Users/tomalcorn/Documents/University/pg/diss/5_EVALUATION/scores_out"
SRC_TSV="/Users/tomalcorn/Documents/University/pg/diss/DATA_ROOT/src_sents.tsv"
COMET_CKPT="/Users/tomalcorn/Documents/University/pg/diss/.cache/wmt20-comet-da/checkpoints/model.ckpt"
BATCH_SIZE=8
BLEU_SMOOTHING_METHOD=2

echo "running python script..."
python /Users/tomalcorn/Documents/University/pg/diss/5_EVALUATION/score.py --tgt $TGT \
    --tgt_folder $TGT_FOLDER --output_folder $OUT_FOLDER \
    --src_tsv $SRC_TSV --comet_ckpt $COMET_CKPT --batch_size $BATCH_SIZE --bleu_smoothing_method ${BLEU_SMOOTHING_METHOD}

echo "Job finished!"
