

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
5. Create `config_multitask.yaml`. Below is an example of the config used for S2UT reduced with two encoder multitasks (`source_letter`, `target_letter`) and one decoder CTC task (`decoder_target_ctc`).
```
source_letter:  # $TASK_NAME
   decoder_type: transformer
   dict: ${DATA_ROOT}/source_letter/dict.txt
   data: ${DATA_ROOT}/source_letter
   encoder_layer: 6
   loss_weight: 8.0
target_letter:
   decoder_type: transformer
   dict: ${DATA_ROOT}/target_letter/dict.txt
   data: ${DATA_ROOT}/target_letter
   encoder_layer: 8
   loss_weight: 8.0
decoder_target_ctc:
   decoder_type: ctc
   dict: ${DATA_ROOT}/decoder_target_ctc/dict.txt
   data: ${DATA_ROOT}/decoder_target_ctc
   decoder_layer: 3
   loss_weight: 1.6
```

## 2: Training

- Run `train.sh` with relevant paths to `$DATA_ROOT` and `$MODEL_DIR` to save model checkpoints. As an example:
```
fairseq-train $DATA_ROOT \
  --config-yaml config.yaml --multitask-config-yaml config_multitask.yaml \
  --task speech_to_speech --target-is-code --target-code-size 100 --vocoder code_hifigan  \
  --criterion speech_to_unit --label-smoothing 0.2 \
  --arch s2ut_transformer_fisher --share-decoder-input-output-embed \
  --dropout 0.1 --attention-dropout 0.1 --relu-dropout 0.1 \
  --train-subset train --valid-subset dev \
  --save-dir ${MODEL_DIR} \
  --lr 0.0005 --lr-scheduler inverse_sqrt --warmup-init-lr 1e-7 --warmup-updates 10000 \
  --optimizer adam --adam-betas "(0.9,0.98)" --clip-norm 10.0 \
  --max-update 400000 --max-tokens 20000 --max-target-positions 3000 --update-freq 4 \
  --seed 1 --fp16 --num-workers 8
```
- Adjust `--update-freq` accordingly for different GPUs. In the above we set `--update-freq` 4 to simulate training with 4 GPUs.
- If using multiple validation sets, replace `--validation-subset dev` with `--validation-subset dev,dev2` etc

## 3: Logging (Optional)

- To create a .tsv log file from the `fairseq` output file from training, run `create_logs.py`, passing the path to directory with the output files.
- To graph the loss from the resulting log files run `plot_loss.py`. `variants` should be a list of the output file names you wish to graph.
- `columns` is a dictionary where each key is a column from the .tsv log file to graph. Each key takes as values any of the following: $SPLIT, 'min' which shows the minimum dev loss, and 'box' which shows an info box for the minimum dev loss.

## 4: Inference


