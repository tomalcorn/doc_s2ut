

## 1: Data Prep
To begin data preparation for S2UT or document-level S2UT, you need:
- `SRC_AUDIO` and `TGT_AUDIO` directories with audio files for paired source and target audio. Each pair of files should be named identically in their respective directories.
- Optional: If you only have target text, use 6: TTS to create TGT_AUDIO from target text directory
- Information on how to split data in training, validation and test sets

1. Run `dir1vdir2.sh` to move any file in `SRC_AUDIO` and not `TGT_AUDIO` and vice versa to backup directories.
2. Run `convert_and_downsample_audio.py` to convert source and/or target audio to wav if necessary and to downsample to 16kHz. `--input_dir` should be `SRC_AUDIO` or `TGT_AUDIO`.
3. Split downsampled files in `SRC_AUDIO` and `TGT_AUDIO` into splits, eg `train`, `dev`, `test`...
4. In `MANIFESTS` create `src_$SPLIT.tsv` and `tgt_$SPLIT` for each split, with format `$FILE_ID.wav \t "corresponding text"`
5. Run `manifest_maker.sh` to create manifest files for `SRC_AUDIO` and `TGT_AUDIO` with the relevant arguments.
6. Run `quantise_tgts.sh` to quantise target audio for each split in `TGT_AUDIO`
7. Run `data_prep.sh` with relevant arguments
