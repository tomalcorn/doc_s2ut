MANIFEST=/work/tc062/tc062/s2517781/mine/data/manifests/en_train_manifest.tsv
OUT_QUANTIZED_FILE=/work/tc062/tc062/s2517781/mine/data/TGT_AUDIO/train.txt
TYPE=hubert
CKPT_PATH=/work/tc062/tc062/s2517781//mine/models/hubert_base_ls960.pt
LAYER=6
KM_MODEL_PATH=/work/tc062/tc062/s2517781/mine/models/kmeans.pt

cd /work/tc062/tc062/s2517781/fairseq

export PYTHONPATH=.:/mnt/lustre/e1000/home/y07/shared/cirrus-software/pytorch/1.13.1/python/3.9.13/lib/python3.9/site-packages

python examples/textless_nlp/gslm/speech2unit/clustering/quantize_with_kmeans.py \
    --feature_type $TYPE \
    --kmeans_model_path $KM_MODEL_PATH \
    --acoustic_model_path $CKPT_PATH \
    --layer $LAYER \
    --manifest_path $MANIFEST \
    --out_quantized_file_path $OUT_QUANTIZED_FILE \
    --extension ".flac"