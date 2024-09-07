RESULTS_PATH="/Users/tomalcorn/Documents/University/pg/diss/4_INFERENCE/inference_base_1"
GEN_SUBSET="test"
VOCODER_CKPT="/Users/tomalcorn/Documents/University/pg/diss/2_TRAINING/models/vocoder"
VOCODER_CFG="/Users/tomalcorn/Documents/University/pg/diss/2_TRAINING/models/vox_config.json"

cd fairseq

grep "^D\-" ${RESULTS_PATH}/generate-${GEN_SUBSET}.txt | \
  sed 's/^D-//ig' | sort -V | cut -f3 \
  > ${RESULTS_PATH}/generate-${GEN_SUBSET}.unit

python examples/speech_to_speech/generate_waveform_from_code.py \
  --in-code-file ${RESULTS_PATH}/generate-${GEN_SUBSET}.unit \
  --vocoder $VOCODER_CKPT --vocoder-cfg $VOCODER_CFG \
  --results-path ${RESULTS_PATH} --dur-prediction