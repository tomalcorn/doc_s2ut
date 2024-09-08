#!/bin/bash

cd fairseq

# Path to pretrained hubert model and k-means clustering model
CKPT_PATH=""
KM_MODEL_PATH=""

# Path to manifest file: $MANIFEST_DIR/${LANG_CODE}_${SPLIT}.tsv
MANIFEST=""

# path to out file: ./TGT_AUDIO/${SPLIT}.txt
OUT_QUANTIZED_FILE=/work/tc062/tc062/s2517781/TGT_AUDIO_FISHER/train.txt

N_CLUSTERS=100
TYPE=hubert
LAYER=6


PYTHONPATH=. python examples/textless_nlp/gslm/speech2unit/clustering/quantize_with_kmeans.py \
    --feature_type $TYPE \
    --kmeans_model_path $KM_MODEL_PATH \
    --acoustic_model_path $CKPT_PATH \
    --layer $LAYER \
    --manifest_path $MANIFEST \
    --out_quantized_file_path $OUT_QUANTIZED_FILE \
    --extension ".wav"

echo "Job finished!"
