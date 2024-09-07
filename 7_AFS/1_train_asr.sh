AFS_DATA_ROOT="/Users/tomalcorn/Documents/University/pg/diss/7_AFS/AFS_DATA_ROOT_1"
SAVE_DIR="/Users/tomalcorn/Documents/University/pg/diss/7_AFS/ASR_SAVE"

cd /Users/tomalcorn/Documents/University/pg/diss/fairseq

fairseq-train ${AFS_DATA_ROOT} --save-dir ${SAVE_DIR} \
  --config-yaml config.yaml --train-subset train --valid-subset dev \
  --num-workers 1 --max-tokens 40000 --max-update 300000 \
  --task speech_to_text --criterion label_smoothed_cross_entropy_with_ctc --label-smoothing 0.1 --report-accuracy \
  --arch zero_asr_transformer --share-decoder-input-output-embed \
  --optimizer adam --lr 2e-3 --lr-scheduler inverse_sqrt --warmup-updates 4000 \
  --clip-norm 10.0 --seed 1 --num-workers 6 --update-freq 6 --max-epoch 3