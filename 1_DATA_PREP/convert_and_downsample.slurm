#!/bin/bash

#SBATCH --partition=standard
#SBATCH --qos=standard
#SBATCH --account=tc062-pool3
#SBATCH --job-name=convert_and_downsample
#SBATCH --time=03:00:00
#SBATCH --ntasks=1

module load python/3.9.13

# set PATHS
export PATH=/work/tc062/tc062/s2517781/py310torch113/bin:/work/y07/shared/cirrus-software/pytorch/1.13.1/python/3.9.13/bin:/work/y07/shared/cirrus-software/libsndfile/1.0.28/bin:/work/y07/shared/cirrus-software/miniconda3/4.12.0-py39/bin:/work/y07/shared/cirrus-software/miniconda3/4.12.0-py39/condabin:/work/y07/shared/cirrus-software/openmpi/4.1.6/bin:/mnt/cephfs/ceph01/site-home/home/tc062/tc062/s2517781/.vscode-server/extensions/ms-python.python-2024.10.0-linux-x64/python_files/deactivate/bash:/work/tc062/tc062/s2517781/py310torch113cu116/bin:/work/y07/shared/cirrus-software/gcc/10.2.0/bin:/mnt/cephfs/ceph01/site-home/home/tc062/tc062/s2517781/.vscode-server/extensions/ms-python.python-2024.10.0-linux-x64/python_files/deactivate/bash:/work/tc062/tc062/s2517781/py310torch113cu116/bin:/work/y07/shared/cirrus-software/gcc/10.2.0/bin:/mnt/cephfs/ceph01/site-home/home/tc062/tc062/s2517781/.vscode-server/cli/servers/Stable-5437499feb04f7a586f677b155b039bc2b3669eb/server/bin/remote-cli:/work/y07/shared/cirrus-software/git/2.37.3/bin:/opt/clmgr/sbin:/opt/clmgr/bin:/opt/sgi/sbin:/opt/sgi/bin:/usr/share/Modules/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/c3/bin:/sbin:/bin:/work/tc062/tc062/s2517781/ffmpeg/ffmpeg-7.0.1-amd64-static

export PYTHONPATH=$PYTHONPATH:/work/tc062/tc062/s2517781/fairseq
echo "PYTHONPATH is: $PYTHONPATH"

source /work/tc062/tc062/s2517781/py310torch113/bin/activate
echo "activated python env"

INPUTDIR="/scratch/space1/tc062/s2517781/FISHER/TGT_AUDIO/test"
OUTPUTDIR="/scratch/space1/tc062/s2517781/FISHER/TGT_AUDIO/test1"


echo "running python script..."
srun python /work/tc062/tc062/s2517781/1_DATA_PREP/convert_and_downsample_audio.py \
    --input_dir ${INPUTDIR} --output_dir ${OUTPUTDIR}

echo "Job finished!"
