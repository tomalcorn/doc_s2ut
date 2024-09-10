AFS_DATA_ROOT=""
AUDIOROOT=""
TRANSCRIPTIONS=""
VOCAB_SIZE=10000

cd /Users/tomalcorn/Documents/University/pg/diss/fairseq

PYTHONPATH=. python examples/speech_to_text/1_prep_asr_data.py --output-root $AFS_DATA_ROOT \
    --audio-root $AUDIOROOT --transcription-file $TRANSCRIPTIONS \
    --vocab-type unigram --vocab-size $VOCAB_SIZE