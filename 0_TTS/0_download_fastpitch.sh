#!/bin/bash

pushd fairseq

MODEL_DIR=""

python ../0_TTS/download_fastpitch.py --model-dir $MODEL_DIR

popd

echo "Job finished!"