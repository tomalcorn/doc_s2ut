#!/bin/bash

cd fairseq

MODEL_DIR=""

python ../0_TTS/download_fastpitch.py --model-dir $MODEL_DIR

echo "Job finished!"