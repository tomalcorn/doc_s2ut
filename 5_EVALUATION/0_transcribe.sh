#!/bin/bash

DATA_ROOT=""
# Name of folder in 4_INFERENCE/results
VARIANT=""

# Inference doesn't always produce output for every item in test. First steps are to clean the id file so transcriptions match. 
python ./5_EVALUATION/find_missing.py \
    --variant ${VARIANT} --data-root ${DATA_ROOT}
if [ $? -ne 0 ]; then
    echo "find_missing.py failed. Exiting..."
    exit 1
fi
python ./5_EVALUATION/clean_id_file.py \
    --variant ${VARIANT} --data-root ${DATA_ROOT}
if [ $? -ne 0 ]; then
    echo "clean_id.py failed. Exiting..."
    exit 1
fi

echo cleaned id file

srun python ./5_EVALUATION/transcribe.py \
    --variant ${VARIANT} --data-root ${DATA_ROOT}
if [ $? -ne 0 ]; then
    echo "transcribe.py failed. Exiting..."
    exit 1
fi
echo "Job finished!"
