MANIFEST=/Users/tomalcorn/Documents/University/pg/diss/mine/data/manifests/en_train.tsv
OUT_QUANTIZED_FILE=/Users/tomalcorn/Documents/University/pg/diss/TGT_AUDIO/train.txt
N_CLUSTERS=100
TYPE=hubert
CKPT_PATH=/Users/tomalcorn/Documents/University/pg/diss/mine/models/hubert_base_ls960.pt
LAYER=6
KM_MODEL_PATH=/Users/tomalcorn/Documents/University/pg/diss/mine/models/km.bin


cd fairseq

PYTHONPATH=. python examples/textless_nlp/gslm/speech2unit/clustering/quantize_with_kmeans.py \
    --feature_type $TYPE \
    --kmeans_model_path $KM_MODEL_PATH \
    --acoustic_model_path $CKPT_PATH \
    --layer $LAYER \
    --manifest_path $MANIFEST \
    --out_quantized_file_path $OUT_QUANTIZED_FILE \
    --extension ".wav"

MANIFEST=/Users/tomalcorn/Documents/University/pg/diss/mine/data/manifests/en_dev.tsv
OUT_QUANTIZED_FILE=/Users/tomalcorn/Documents/University/pg/diss/TGT_AUDIO/dev.txt
N_CLUSTERS=100
TYPE=hubert
CKPT_PATH=/Users/tomalcorn/Documents/University/pg/diss/mine/models/hubert_base_ls960.pt
LAYER=6
KM_MODEL_PATH=/Users/tomalcorn/Documents/University/pg/diss/mine/models/km.bin



PYTHONPATH=. python examples/textless_nlp/gslm/speech2unit/clustering/quantize_with_kmeans.py \
    --feature_type $TYPE \
    --kmeans_model_path $KM_MODEL_PATH \
    --acoustic_model_path $CKPT_PATH \
    --layer $LAYER \
    --manifest_path $MANIFEST \
    --out_quantized_file_path $OUT_QUANTIZED_FILE \
    --extension ".wav"

MANIFEST=/Users/tomalcorn/Documents/University/pg/diss/mine/data/manifests/en_test.tsv
OUT_QUANTIZED_FILE=/Users/tomalcorn/Documents/University/pg/diss/TGT_AUDIO/test.txt
N_CLUSTERS=100
TYPE=hubert
CKPT_PATH=/Users/tomalcorn/Documents/University/pg/diss/mine/models/hubert_base_ls960.pt
LAYER=6
KM_MODEL_PATH=/Users/tomalcorn/Documents/University/pg/diss/mine/models/km.bin


PYTHONPATH=. python examples/textless_nlp/gslm/speech2unit/clustering/quantize_with_kmeans.py \
    --feature_type $TYPE \
    --kmeans_model_path $KM_MODEL_PATH \
    --acoustic_model_path $CKPT_PATH \
    --layer $LAYER \
    --manifest_path $MANIFEST \
    --out_quantized_file_path $OUT_QUANTIZED_FILE \
    --extension ".wav"