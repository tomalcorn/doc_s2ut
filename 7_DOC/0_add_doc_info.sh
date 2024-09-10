#!/bin/bash

DATA_ROOT=""
DOC_CTXT_SIZE=1
SPLITS=""

IFS=','
for split in $SPLITS; do
    python ./0_add_doc_info.py --split $split \
        --data-root $DATA_ROOT --doc-context-size $DOC_CTXT_SIZE
done
    
echo "Job finished!"