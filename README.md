

To begin data preparation for S2UT or document-level S2UT, you need:
- `SRC_AUDIO` and `TGT_AUDIO` directories with audio files for paired source and target audio. Each pair of files should be named identically in their respective directories.
- Optional: If you only have target text, use 6: TTS to create TGT_AUDIO from target text directory
- Information on how to split data in training, validation and test sets
- Pretrained checkpoints for hubert model, quantisation model, vocoder and vocoder config downloaded into 0_PRETRAINED_MODELS:
  
### Unit-based HiFi-GAN Vocoder
Unit config | Unit size | Vocoder dataset | Model
|---|---|---|---
[HuBERT Base, Librispeech](https://github.com/fairinternal/fairseq-py/tree/main/examples/hubert), layer 6 | 100 | [LJSpeech](https://keithito.com/LJ-Speech-Dataset/) | [ckpt](https://dl.fbaipublicfiles.com/fairseq/speech_to_speech/vocoder/code_hifigan/hubert_base_100_lj/g_00500000), [config](https://dl.fbaipublicfiles.com/fairseq/speech_to_speech/vocoder/code_hifigan/hubert_base_100_lj/config.json)

### Hubert and quantisation models
* [HuBERT-Base](https://dl.fbaipublicfiles.com/hubert/hubert_base_ls960.pt)
* [Quantisation Model](https://dl.fbaipublicfiles.com/textless_nlp/gslm/hubert/km100/km.bin)

## 1: Data Prep

1. Optional: Run `dir1vdir2.sh` to move any file in `SRC_AUDIO` and not `TGT_AUDIO` and vice versa to backup directories.
2. Run `convert_and_downsample.sh` to convert source and/or target audio to wav if necessary and to downsample to 16kHz. `--input_dir` should be path to `SRC_AUDIO` or `TGT_AUDIO`.
3. Split downsampled files in `SRC_AUDIO` and `TGT_AUDIO` into splits, eg `train`, `dev`, `test`...
4. In `MANIFESTS` create `src_$SPLIT.tsv` and `tgt_$SPLIT.tsv` for each split, with format:
`$FILE_ID.wav \t "corresponding text"`
1. Run `manifest_maker.sh` to create manifest files for `SRC_AUDIO` and `TGT_AUDIO` with the relevant arguments.
2. Run `quantise_tgts.sh` to quantise target audio for each split in `TGT_AUDIO`
3. Run `data_prep.sh` with relevant arguments.
4. Run `dict_maker.sh` to prepare multitask information. Currently only `'source_letter'`, `'target_letter'` and/or `'decoder_tgt_ctc'` are supported.
