#!/bin/bash

#SBATCH --partition=standard
#SBATCH --qos=standard
#SBATCH --account=tc062-pool3
#SBATCH --job-name=1_train_asr_cpu
#SBATCH --time=01:00:00
#SBATCH --ntasks=16

module load pytorch/1.13.1

# set PATHS
# export PATH=/work/tc062/tc062/s2517781/py310torch113/bin:/work/y07/shared/cirrus-software/pytorch/1.13.1/python/3.9.13/bin:/work/y07/shared/cirrus-software/libsndfile/1.0.28/bin:/work/y07/shared/cirrus-software/miniconda3/4.12.0-py39/bin:/work/y07/shared/cirrus-software/miniconda3/4.12.0-py39/condabin:/work/y07/shared/cirrus-software/openmpi/4.1.6/bin:/mnt/cephfs/ceph01/site-home/home/tc062/tc062/s2517781/.vscode-server/extensions/ms-python.python-2024.10.0-linux-x64/python_files/deactivate/bash:/work/tc062/tc062/s2517781/py310torch113cu116/bin:/work/y07/shared/cirrus-software/gcc/10.2.0/bin:/mnt/cephfs/ceph01/site-home/home/tc062/tc062/s2517781/.vscode-server/extensions/ms-python.python-2024.10.0-linux-x64/python_files/deactivate/bash:/work/tc062/tc062/s2517781/py310torch113cu116/bin:/work/y07/shared/cirrus-software/gcc/10.2.0/bin:/mnt/cephfs/ceph01/site-home/home/tc062/tc062/s2517781/.vscode-server/cli/servers/Stable-5437499feb04f7a586f677b155b039bc2b3669eb/server/bin/remote-cli:/work/y07/shared/cirrus-software/git/2.37.3/bin:/opt/clmgr/sbin:/opt/clmgr/bin:/opt/sgi/sbin:/opt/sgi/bin:/usr/share/Modules/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/c3/bin:/sbin:/bin


source /work/tc062/tc062/s2517781/py310torch113/bin/activate
echo "activated python env"

export PYTHONPATH=$PYTHONPATH:/work/tc062/tc062/s2517781/fairseq:/mnt/cephfs/ceph01/site-home/home/tc062/tc062/s2517781/.local/lib/python3.9/site-packages
echo "PYTHONPATH is: $PYTHONPATH"
which python

cd /work/tc062/tc062/s2517781/fairseq

FS_DATA_ROOT="/work/tc062/tc062/s2517781/7_AFS/AFS_DATA_ROOT_1"
SAVE_DIR="/work/tc062/tc062/s2517781/7_AFS/ASR_SAVE"

echo "running python script..."
srun fairseq-train ${AFS_DATA_ROOT} --save-dir ${SAVE_DIR} \
  --config-yaml config.yaml --train-subset train --valid-subset dev \
  --num-workers 1 --max-tokens 40000 --max-update 300000 \
  --task speech_to_text --criterion label_smoothed_cross_entropy_with_ctc --label-smoothing 0.1 --report-accuracy \
  --arch zero_asr_transformer --share-decoder-input-output-embed \
  --optimizer adam --lr 2e-3 --lr-scheduler inverse_sqrt --warmup-updates 4000 \
  --clip-norm 10.0 --seed 1 --update-freq 3 --max-epoch 3

echo "Job finished!"
