#!/bin/bash

#SBATCH --partition=gpu
#SBATCH --qos=gpu
#SBATCH --account=tc062-pool3
#SBATCH --job-name=3_train_st
#SBATCH --time=12:00:00
#SBATCH --nodes=1
#SBATCH --gres=gpu:4

module load pytorch/1.13.1-gpu

# set PATHS
export CUDA_HOME=/work/y07/shared/cirrus-software/nvidia/hpcsdk-22.2/Linux_x86_64/22.2/cuda
export PATH=/work/tc062/tc062/s2517781/py310torch113cu116/bin:/work/y07/shared/cirrus-software/pytorch/1.13.1-gpu/python/3.10.8/bin:/work/y07/shared/cirrus-software/libsndfile/1.0.28/bin:/work/y07/shared/cirrus-software/miniconda3/22.11.1-1-py310-gpu/bin:/work/y07/shared/cirrus-software/miniconda3/22.11.1-1-py310-gpu/condabin:/work/y07/shared/cirrus-software/openmpi/4.1.6-cuda-11.6/bin:/work/y07/shared/cirrus-software/gcc/10.2.0/bin:/work/y07/shared/cirrus-software/nvidia/hpcsdk-22.2/Linux_x86_64/22.2/compilers/extras/qd/bin:/work/y07/shared/cirrus-software/nvidia/hpcsdk-22.2/Linux_x86_64/22.2/compilers/bin:/work/y07/shared/cirrus-software/nvidia/hpcsdk-22.2/Linux_x86_64/22.2/cuda/bin:/mnt/cephfs/ceph01/site-home/home/tc062/tc062/s2517781/.vscode-server/cli/servers/Stable-611f9bfce64f25108829dd295f54a6894e87339d/server/bin/remote-cli:/work/y07/shared/cirrus-software/git/2.37.3/bin:/opt/clmgr/sbin:/opt/clmgr/bin:/opt/sgi/sbin:/opt/sgi/bin:/usr/share/Modules/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/c3/bin:/sbin:/bin:/work/tc062/tc062/s2517781/ffmpeg/ffmpeg-7.0.1-amd64-static

unset LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/work/tc062/shared/lib


export PYTHONPATH=$PYTHONPATH:/work/tc062/tc062/s2517781/fairseq
echo "PYTHONPATH is: $PYTHONPATH"

source /work/tc062/tc062/s2517781/py310torch113cu116/bin/activate
echo "activated python env"

cd /work/tc062/tc062/s2517781/fairseq

DATA_ROOT="/work/tc062/tc062/s2517781/DATA_ROOT"
SAVE_DIR="/work/tc062/tc062/s2517781/2_TRAINING/models/BASELINE_AFS_1.0"
FEAT_EXTRACTOR="/work/tc062/tc062/s2517781/7_AFS/ASR_AFS_SAVE_BIG/checkpoint_best.pt"
FEAT_EXTRACTOR_ARGS="/work/tc062/tc062/s2517781/7_AFS/feat_extractor_args.tsv"
# export CUDA_LAUNCH_BLOCKING=1

# export TORCH_DISTRIBUTED_DEBUG=DETAIL

echo "running python script..."
nvidia-smi --loop=10 --filename=out-nvidia-smi.txt &
srun fairseq-train $DATA_ROOT \
  --config-yaml config.yaml --multitask-config-yaml config_multitask.yaml \
  --task speech_to_speech --target-is-code --target-code-size 100 --vocoder code_hifigan  \
  --criterion speech_to_unit --label-smoothing 0.2 \
  --arch s2ut_transformer_afs --conv-version afs --feat-extractor-pretraining-path $FEAT_EXTRACTOR \
  --feat-extractor-args $FEAT_EXTRACTOR_ARGS --share-decoder-input-output-embed \
  --dropout 0.1 --attention-dropout 0.1 --relu-dropout 0.1 \
  --train-subset train --valid-subset dev \
  --save-dir ${SAVE_DIR} \
  --lr 0.0005 --lr-scheduler inverse_sqrt --warmup-init-lr 1e-7 --warmup-updates 10000 \
  --optimizer adam --adam-betas "(0.9,0.98)" --clip-norm 10.0 \
  --max-update 400000 --max-tokens 20000 --update-freq 4 \
  --seed 1 --fp16 --num-workers 8 --max-epoch 800 --save-interval 10

echo "Job finished!"
