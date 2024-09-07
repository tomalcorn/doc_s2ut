#!/bin/bash

SPLIT="dev"

FEAT_EXTRACTOR_CKPT="/Users/tomalcorn/Documents/University/pg/diss/7_AFS/ASR_AFS_4.0/checkpoint_best.pt"
ARGS_TSV="/Users/tomalcorn/Documents/University/pg/diss/7_AFS/feat_extractor_args.tsv"
DEFAULT_ARGS_TSV="/Users/tomalcorn/Documents/University/pg/diss/12_DOC/0_preprocessing/default_args.tsv"
AUDIO_DIR="/Users/tomalcorn/Documents/University/pg/diss/SRC_AUDIO_EP/${SPLIT}"
OUTPUT_DIR="/Users/tomalcorn/Documents/University/pg/diss/SRC_FEATS_EP/${SPLIT}"
INPUT_TSV="/Users/tomalcorn/Documents/University/pg/diss/DATA_ROOT_EP/${SPLIT}.tsv"
OUTPUT_TSV="/Users/tomalcorn/Documents/University/pg/diss/DATA_ROOT_EP_DOC/${SPLIT}_pre_concat.tsv"

pushd /Users/tomalcorn/Documents/University/pg/diss/fairseq

export PYTHONPATH=$PYTHONPATH:/Users/tomalcorn/Documents/University/pg/diss/fairseq

python /Users/tomalcorn/Documents/University/pg/diss/12_DOC/0_preprocessing/feature_extraction.py \
    --feat_extractor_ckpt ${FEAT_EXTRACTOR_CKPT} --args_tsv ${ARGS_TSV} \
    --default_args_tsv ${DEFAULT_ARGS_TSV} --audio_dir ${AUDIO_DIR} \
    --output_dir ${OUTPUT_DIR} --input_tsv ${INPUT_TSV} --output_tsv ${OUTPUT_TSV}

popd