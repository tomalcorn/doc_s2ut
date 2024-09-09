#!/bin/bash

#SBATCH --partition=gpu
#SBATCH --qos=gpu
#SBATCH --account=tc062-pool3
#SBATCH --job-name=train_asr
#SBATCH --time=03:00:00
#SBATCH --nodes=1
#SBATCH --gres=gpu:2

module load pytorch/1.13.1-gpu

# set PATHS
export CUDA_HOME=/work/y07/shared/cirrus-software/nvidia/hpcsdk-22.2/Linux_x86_64/22.2/cuda
export PATH=/work/tc062/tc062/s2517781/py310torch113cu116/bin:/work/y07/shared/cirrus-software/pytorch/1.13.1-gpu/python/3.10.8/bin:/work/y07/shared/cirrus-software/libsndfile/1.0.28/bin:/work/y07/shared/cirrus-software/miniconda3/22.11.1-1-py310-gpu/bin:/work/y07/shared/cirrus-software/miniconda3/22.11.1-1-py310-gpu/condabin:/work/y07/shared/cirrus-software/openmpi/4.1.6-cuda-11.6/bin:/work/y07/shared/cirrus-software/gcc/10.2.0/bin:/work/y07/shared/cirrus-software/nvidia/hpcsdk-22.2/Linux_x86_64/22.2/compilers/extras/qd/bin:/work/y07/shared/cirrus-software/nvidia/hpcsdk-22.2/Linux_x86_64/22.2/compilers/bin:/work/y07/shared/cirrus-software/nvidia/hpcsdk-22.2/Linux_x86_64/22.2/cuda/bin:/mnt/cephfs/ceph01/site-home/home/tc062/tc062/s2517781/.vscode-server/cli/servers/Stable-611f9bfce64f25108829dd295f54a6894e87339d/server/bin/remote-cli:/work/y07/shared/cirrus-software/git/2.37.3/bin:/opt/clmgr/sbin:/opt/clmgr/bin:/opt/sgi/sbin:/opt/sgi/bin:/usr/share/Modules/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/c3/bin:/sbin:/bin:/work/tc062/tc062/s2517781/ffmpeg/ffmpeg-7.0.1-amd64-static

export PYTHONPATH=$PYTHONPATH:/work/tc062/tc062/s2517781/fairseq
echo "PYTHONPATH is: $PYTHONPATH"

source /work/tc062/tc062/s2517781/py310torch113cu116/bin/activate
echo "activated python env"

cd /work/tc062/tc062/s2517781/fairseq

AFS_DATA_ROOT="/work/tc062/tc062/s2517781/7_AFS/AFS_DATA_ROOT_1"
SAVE_DIR="/work/tc062/tc062/s2517781/7_AFS/ASR_BASELINE"

echo "running python script..."
nvidia-smi --loop=10 --filename=out-nvidia-smi.txt &
srun fairseq-train ${AFS_DATA_ROOT} --save-dir ${SAVE_DIR} \
  --config-yaml config.yaml --train-subset train --valid-subset dev \
  --num-workers 1 --max-tokens 40000 --max-update 300000 \
  --task speech_to_text --criterion label_smoothed_cross_entropy_with_ctc --label-smoothing 0.1 --report-accuracy \
  --arch zero_asr_transformer --share-decoder-input-output-embed \
  --optimizer adam --lr 2e-3 --lr-scheduler inverse_sqrt --warmup-updates 4000 \
  --clip-norm 10.0 --seed 1 --update-freq 4 --max-epoch 300

echo "Job finished!"
