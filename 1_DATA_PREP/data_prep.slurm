#!/bin/bash

#SBATCH --partition=gpu
#SBATCH --qos=gpu
#SBATCH --account=tc062-pool3
#SBATCH --job-name=learn_k_means
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH --gres=gpu:1

module load pytorch/1.13.1-gpu

# set PATHS
export CUDA_HOME=/work/y07/shared/cirrus-software/nvidia/hpcsdk-22.2/Linux_x86_64/22.2/cuda
export PATH=/work/tc062/tc062/s2517781/py310torch113cu116/bin:/work/y07/shared/cirrus-software/pytorch/1.13.1-gpu/python/3.10.8/bin:/work/y07/shared/cirrus-software/libsndfile/1.0.28/bin:/work/y07/shared/cirrus-software/miniconda3/22.11.1-1-py310-gpu/bin:/work/y07/shared/cirrus-software/miniconda3/22.11.1-1-py310-gpu/condabin:/work/y07/shared/cirrus-software/openmpi/4.1.6-cuda-11.6/bin:/work/y07/shared/cirrus-software/gcc/10.2.0/bin:/work/y07/shared/cirrus-software/nvidia/hpcsdk-22.2/Linux_x86_64/22.2/compilers/extras/qd/bin:/work/y07/shared/cirrus-software/nvidia/hpcsdk-22.2/Linux_x86_64/22.2/compilers/bin:/work/y07/shared/cirrus-software/nvidia/hpcsdk-22.2/Linux_x86_64/22.2/cuda/bin:/mnt/cephfs/ceph01/site-home/home/tc062/tc062/s2517781/.vscode-server/cli/servers/Stable-611f9bfce64f25108829dd295f54a6894e87339d/server/bin/remote-cli:/work/y07/shared/cirrus-software/git/2.37.3/bin:/opt/clmgr/sbin:/opt/clmgr/bin:/opt/sgi/sbin:/opt/sgi/bin:/usr/share/Modules/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/c3/bin:/sbin:/bin

export PYTHONPATH=$PYTHONPATH:/work/tc062/tc062/s2517781/fairseq
echo "PYTHONPATH is: $PYTHONPATH"

source /work/tc062/tc062/s2517781/py310torch113cu116/bin/activate
echo "activated python env"

cd /work/tc062/tc062/s2517781/fairseq

SPLIT1="train"
SPLIT2="dev"
SPLIT3="dev2"
SPLIT4="test"

SRC_AUDIO="/work/tc062/tc062/s2517781/SRC_AUDIO_FISHER"
TGT_AUDIO="/work/tc062/tc062/s2517781/TGT_AUDIO_FISHER"
DATA_ROOT="/work/tc062/tc062/s2517781/11_FISHER/DATA_ROOT"
VOCODER_CKPT="/work/tc062/tc062/s2517781/2_TRAINING/models/vocoder"
VOCODER_CFG="/work/tc062/tc062/s2517781/2_TRAINING/models/vox_config.json"

echo "running python script..."
nvidia-smi --loop=10 --filename=out-nvidia-smi.txt &
srun python examples/speech_to_speech/preprocessing/prep_s2ut_data.py \
  --source-dir $SRC_AUDIO --target-dir $TGT_AUDIO --data-split $SPLIT1 $SPLIT2 $SPLIT3 $SPLIT4 \
  --output-root $DATA_ROOT --reduce-unit \
  --vocoder-checkpoint $VOCODER_CKPT --vocoder-cfg $VOCODER_CFG

echo "Job finished!"
