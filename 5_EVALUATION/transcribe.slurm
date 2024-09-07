#!/bin/bash

#SBATCH --partition=gpu
#SBATCH --qos=gpu
#SBATCH --account=tc062-pool3
#SBATCH --job-name=transcribe
#SBATCH --time=03:00:00
#SBATCH --nodes=1
#SBATCH --gres=gpu:1

module load pytorch/1.13.1-gpu

# set PATHS
export CUDA_HOME=/work/y07/shared/cirrus-software/nvidia/hpcsdk-22.2/Linux_x86_64/22.2/cuda
export PATH=/work/tc062/tc062/s2517781/py310torch113cu116/bin:/work/y07/shared/cirrus-software/pytorch/1.13.1-gpu/python/3.10.8/bin:/work/y07/shared/cirrus-software/libsndfile/1.0.28/bin:/work/y07/shared/cirrus-software/miniconda3/22.11.1-1-py310-gpu/bin:/work/y07/shared/cirrus-software/miniconda3/22.11.1-1-py310-gpu/condabin:/work/y07/shared/cirrus-software/openmpi/4.1.6-cuda-11.6/bin:/work/y07/shared/cirrus-software/gcc/10.2.0/bin:/work/y07/shared/cirrus-software/nvidia/hpcsdk-22.2/Linux_x86_64/22.2/compilers/extras/qd/bin:/work/y07/shared/cirrus-software/nvidia/hpcsdk-22.2/Linux_x86_64/22.2/compilers/bin:/work/y07/shared/cirrus-software/nvidia/hpcsdk-22.2/Linux_x86_64/22.2/cuda/bin:/mnt/cephfs/ceph01/site-home/home/tc062/tc062/s2517781/.vscode-server/cli/servers/Stable-611f9bfce64f25108829dd295f54a6894e87339d/server/bin/remote-cli:/work/y07/shared/cirrus-software/git/2.37.3/bin:/opt/clmgr/sbin:/opt/clmgr/bin:/opt/sgi/sbin:/opt/sgi/bin:/usr/share/Modules/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/c3/bin:/sbin:/bin:/work/tc062/tc062/s2517781/ffmpeg/ffmpeg-7.0.1-amd64-static

export PYTHONPATH=/work/tc062/tc062/s2517781/py310torch113cu116/lib/python3.10/site-packages:/work/y07/shared/cirrus-software/pytorch/1.13.1-gpu/python/3.10.8/lib/python3.10/site-packages:/work/y07/shared/cirrus-software/miniconda3/22.11.1-1-py310-gpu/lib/python3.10/site-packages
echo "PYTHONPATH is: $PYTHONPATH"

source /work/tc062/tc062/s2517781/py310torch113cu116/bin/activate
echo "activated python env"

# SCRIPT VARIABLES

echo "running python script..."
nvidia-smi --loop=10 --filename=out-nvidia-smi.txt &
srun python /work/tc062/tc062/s2517781/5_EVALUATION/transcribe.py

echo "Job finished!"
