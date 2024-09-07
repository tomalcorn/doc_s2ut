# $SPLIT1, $SPLIT2, etc. are split names such as train, dev, test, etc.
SPLIT1="train"
SPLIT2="dev"
SPLIT3="test"

SRC_AUDIO="/Users/tomalcorn/Documents/University/pg/diss/SRC_AUDIO_EP"
TGT_AUDIO="/Users/tomalcorn/Documents/University/pg/diss/TGT_AUDIO_EP"
DATA_ROOT="/Users/tomalcorn/Documents/University/pg/diss/DATA_ROOT_EP"
VOCODER_CKPT="/Users/tomalcorn/Documents/University/pg/diss/2_TRAINING/models/vocoder"
VOCODER_CFG="/Users/tomalcorn/Documents/University/pg/diss/2_TRAINING/models/vox_config.json"

cd fairseq

PYTHONPATH=. python examples/speech_to_speech/preprocessing/prep_s2ut_data.py \
  --source-dir $SRC_AUDIO --target-dir $TGT_AUDIO --data-split $SPLIT1 $SPLIT2 $SPLIT3 \
  --output-root $DATA_ROOT --reduce-unit \
  --vocoder-checkpoint $VOCODER_CKPT --vocoder-cfg $VOCODER_CFG