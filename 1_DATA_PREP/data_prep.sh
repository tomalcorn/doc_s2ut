#!/bin/bash

cd fairseq

SPLIT1="train"
SPLIT2="dev"
# etc etc

# Absolute path to SRC_AUDIO and TGT_AUDIO
SRC_AUDIO=""
TGT_AUDIO=""
# Absolute path to DATA_ROOT directory
DATA_ROOT=""

# Paths to vocoder checkpoint and config file
VOCODER_CKPT=""
VOCODER_CFG=""


PYTHONPATH=. python examples/speech_to_speech/preprocessing/prep_s2ut_data.py \
  --source-dir $SRC_AUDIO --target-dir $TGT_AUDIO --data-split $SPLIT1 $SPLIT2 $SPLIT3 $SPLIT4 \
  --output-root $DATA_ROOT --reduce-unit \
  --vocoder-checkpoint $VOCODER_CKPT --vocoder-cfg $VOCODER_CFG

echo "Job finished!"
