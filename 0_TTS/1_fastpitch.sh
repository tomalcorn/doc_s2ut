#!/bin/bash

pushd fairseq

DATA_ROOT="/work/tc062/tc062/s2517781/11_FISHER/manifests"
OUTPUT_DIR="/scratch/space1/tc062/s2517781/FISHER/TGT_AUDIO"
FASTPITCH_DIR="/work/tc062/tc062/s2517781/6_TTS/TTS/1_generate_speech/fastpitch_models/models--facebook--fastspeech2-en-ljspeech/snapshots/a3e3e5e2e62bb7ca7514b11aa469e9c5b01a20bf"
NLTK="/work/tc062/tc062/s2517781/.cache/nltk"
SPLIT=""

python ./0_TTS/1_generate_speech/fastpitch.py \
    --output_dir ${OUTPUT_DIR} --manifest_dir ${MANIFESTDIR} \
    --model-dir ${FASTPITCH_DIR} --nltk ${NLTK} --device "cuda" \
    --split ${SPLIT}

popd

echo "Job finished!"
