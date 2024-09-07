#!/bin/bash

OUTPUTDIR="/Users/tomalcorn/Documents/University/pg/diss/6_TTS/TTS/2_speech"
MANIFESTDIR="/Users/tomalcorn/Documents/University/pg/diss/v1.1/es/manifests"
BATCH=10
MAX_DEC_T_STEPS=3000

python /Users/tomalcorn/Documents/University/pg/diss/6_TTS/TTS/1_generate_speech/Speech_Synthesys.py --output_dir $OUTPUTDIR --manifest_dir $MANIFESTDIR --batch_size 10 --max_decoder_tsteps $MAX_DEC_T_STEPS

echo "Job finished!"
 