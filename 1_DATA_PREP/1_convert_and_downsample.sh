#!/bin/bash

SRC_AUDIO="./SRC_AUDIO"
TGT_AUDIO="./TGT_AUDIO"

python ./1_DATA_PREP/convert_and_downsample_audio.py --input-dir ${SRC_AUDIO}
python ./1_DATA_PREP/convert_and_downsample_audio.py --input-dir ${TGT_AUDIO}