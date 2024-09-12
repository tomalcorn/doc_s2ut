#!/bin/bash

pushd fairseq

SPLIT1="train"
SPLIT2="dev"
SPLIT3="test"
# etc etc

SRC_AUDIO="/Users/tomalcorn/Documents/University/pg/github_practice/doc_s2ut/SRC_AUDIO"
TGT_AUDIO="/Users/tomalcorn/Documents/University/pg/github_practice/doc_s2ut/TGT_AUDIO"
# Absolute path to DATA_ROOT directory
DATA_ROOT="/Users/tomalcorn/Documents/University/pg/github_practice/doc_s2ut/DATA_ROOT"

# Paths to vocoder checkpoint and config file
VOCODER_CKPT="/Users/tomalcorn/Documents/University/pg/github_practice/doc_s2ut/PRETRAINED_MODELS/vocoder"
VOCODER_CFG="/Users/tomalcorn/Documents/University/pg/github_practice/doc_s2ut/PRETRAINED_MODELS/vocoder_config.json"


PYTHONPATH=. python examples/speech_to_speech/preprocessing/prep_s2ut_data.py \
  --source-dir $SRC_AUDIO --target-dir $TGT_AUDIO --data-split $SPLIT1 $SPLIT2 $SPLIT3 \
  --output-root $DATA_ROOT --reduce-unit \
  --vocoder-checkpoint $VOCODER_CKPT --vocoder-cfg $VOCODER_CFG

popd

echo "Job finished!"
