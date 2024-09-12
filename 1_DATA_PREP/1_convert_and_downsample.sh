#!/bin/bash

SRC_AUDIO="./SRC_AUDIO"
TGT_AUDIO="./TGT_AUDIO"

python ./convert_and_downsample_audio.py --input-dir ${SRC_AUDIO}
python ./convert_and_downsample_audio.py --input-dir ${TGT_AUDIO}