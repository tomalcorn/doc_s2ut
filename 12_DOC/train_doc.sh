DATA_ROOT="/Users/tomalcorn/Documents/University/pg/diss/DATA_ROOT_EP_DOC_TEST"
MODEL_DIR="/Users/tomalcorn/Documents/University/pg/diss/12_DOC/models_local/test2"
FEAT_EXTRACTOR_ARGS="/Users/tomalcorn/Documents/University/pg/diss/7_AFS/feat_extractor_args.tsv"
FEAT_EXTRACTOR="/Users/tomalcorn/Documents/University/pg/diss/7_AFS/ASR_AFS_SAVE_BIG/checkpoint_best.pt"

cd fairseq/

mprof run fairseq-train $DATA_ROOT \
  --config-yaml config.yaml --multitask-config-yaml config_multitask.yaml \
  --task doc_speech_to_speech --target-is-code --target-code-size 100 --vocoder code_hifigan  \
  --criterion doc_speech_to_unit --conv-version afs --feat-extractor-pretraining-path $FEAT_EXTRACTOR \
  --arch doc_s2ut_transformer --share-decoder-input-output-embed \
  --feat-extractor-args $FEAT_EXTRACTOR_ARGS --share-decoder-input-output-embed \
  --dropout 0.1 --attention-dropout 0.1 --relu-dropout 0.1 \
  --train-subset train --valid-subset dev \
  --save-dir ${MODEL_DIR} \
  --lr 0.00007 --lr-scheduler inverse_sqrt --warmup-init-lr 1e-7 --warmup-updates 10000 \
  --optimizer adam --adam-betas "(0.9,0.98)" --clip-norm 10.0 \
  --max-update 400000 --max-sentences 3 --max-source-positions 4000 --update-freq 4  \
  --seed 1 --num-workers 8 --max-epoch 3 --save-interval 1 \
  --skip-invalid-size-inputs-valid-test \
  --doc-context-size 1

  echo "job finished"