#!/bin/bash

pushd fairseq

LANG_CODE=""
SPLIT=""
DATA_ROOT=""

# Path to pretrained hubert model and k-means clustering model
CKPT_PATH=""
QUANT_MODEL=""

# path to out file: ../TGT_AUDIO/${SPLIT}.txt
OUT_QUANTIZED_FILE=""

MANIFEST="${DATA_ROOT}/${LANG_CODE}_${SPLIT}.tsv"
N_CLUSTERS=100
TYPE=hubert
LAYER=6


PYTHONPATH=. python examples/textless_nlp/gslm/speech2unit/clustering/quantize_with_kmeans.py \
    --feature_type $TYPE \
    --kmeans_model_path $QUANT_MODEL \
    --acoustic_model_path $CKPT_PATH \
    --layer $LAYER \
    --manifest_path $MANIFEST \
    --out_quantized_file_path $OUT_QUANTIZED_FILE \
    --extension ".wav"

popd

echo "Job finished!"
