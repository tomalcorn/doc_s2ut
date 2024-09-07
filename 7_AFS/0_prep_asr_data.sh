OUTPUTDIR="/Users/tomalcorn/Documents/University/pg/diss/7_AFS/AFS_DATA_ROOT_1"
AUDIOROOT="/Users/tomalcorn/Documents/University/pg/diss/VOXPOPULI/SRC_AUDIO_1"
TRANSCRIPTIONS="/Users/tomalcorn/Documents/University/pg/diss/VOXPOPULI/manifests/voxpop_all.tsv"
VOCAB_SIZE=10000
TMP="/Users/tomalcorn/Documents/University/pg/diss/tmp1.txt"

cd /Users/tomalcorn/Documents/University/pg/diss/fairseq

PYTHONPATH=. python examples/speech_to_text/1_prep_asr_data.py --output-root $OUTPUTDIR --audio-root $AUDIOROOT --transcription-file $TRANSCRIPTIONS --vocab-type unigram --vocab-size $VOCAB_SIZE --temp-file $TMP