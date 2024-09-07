N_CLUSTERS=100
TYPE=hubert
CKPT_PATH=/Users/tomalcorn/Documents/University/pg/diss/mine/models/hubert_base_ls960.pt
LAYER=6
MANIFEST=/Users/tomalcorn/Documents/University/pg/diss/mine/data/manifests/en_clips.tsv
KM_MODEL_PATH=/Users/tomalcorn/Documents/University/pg/diss/mine/models/kmeans.pt

cd fairseq

PYTHONPATH=. python examples/textless_nlp/gslm/speech2unit/clustering/cluster_kmeans.py \
    --num_clusters $N_CLUSTERS \
    --feature_type $TYPE \
    --checkpoint_path $CKPT_PATH \
    --layer $LAYER \
    --manifest_path $MANIFEST \
    --out_kmeans_model_path $KM_MODEL_PATH

