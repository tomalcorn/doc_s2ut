AFS_DATA_ROOT=""
AUDIOROOT="/work/tc062/tc062/s2517781/VOXPOPULI/SRC_AUDIO"
TRANSCRIPTIONS="/work/tc062/tc062/s2517781/VOXPOPULI/manifests/voxpop_all.tsv"
VOCAB_SIZE=10000

cd /Users/tomalcorn/Documents/University/pg/diss/fairseq

PYTHONPATH=. python examples/speech_to_text/1_prep_asr_data.py --output-root $AFS_DATA_ROOT \
    --audio-root $AUDIOROOT --transcription-file $TRANSCRIPTIONS \
    --vocab-type unigram --vocab-size $VOCAB_SIZE