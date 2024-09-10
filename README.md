
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
- [Quantisation Model](https://dl.fbaipublicfiles.com/textless_nlp/gslm/hubert/km100/km.bin)

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

If only training a document model with AFS skip this section and go to section 6.

1. Run `train.sh` with relevant paths to `$DATA_ROOT` and `$MODEL_DIR` to save model checkpoints. As an example:

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

1. Run `infer.sh` with the given arguments to generate discrete unit sequences for the test set.
2. Run `u2wav.sh` with given arguments to convert discrete unit sequences to .wav files
  
## 5: Evaluation

To evaluate the produced .wav files first they must be transcribed after which they can be scored. The scoring methods provided here are ASR-Bleu and ASR-COMET. I use `Whisper-medium` for the transcription and `SACREBLEU` for scoring. To use these methods, first run `download_whisper.py` and/or `download_comet.py` with the path to `0_PRETRAINED_MODELS` as the only argument.

1. Run `0_transcribe.sh` with the given arguments. `$VARIANT` should be the name of the folder in `4_INFERENCE/results`
2. Run `1_score.sh` with the given arguments. If using COMET set `--use-comet` and set `$COMET_CKPT` to the `model.pt` file downloaded in `0_PRETRAINED_MODELS`

## 6: AFS

Training and using AFS is done in 3 stages. First a separate encoder-decoder ASR model is trained. Then this ASR model is finetuned with AFS inserted between the encoder and decoder. Finally, the decoder is dropped, the encoder and afs modules are frozen into a feature extractor. An S2UT model can now be trained, where the standard subsample module in the encoder is replaced by the AFS feature extractor.

1. Download ASR data. I used Voxpopuli Spanish audio to English text data available here:

- [Voxpopuli data](https://github.com/facebookresearch/voxpopuli)


2. Make a transcription .tsv manifest file for the full dataset. The file should have the following header:
   
   ```
    audio   text
   ```
`audio` should be the file basename for each file without any extention, `text` should be the corresponding transcription.
3. Run `0_prep_asr_data.sh` with given arguments. Run twice with `$AUDIOROOT` set to path to dataset used for asr training, then for finetuning. Use `AFS_DATA_ROOT_1` for asr pretraining and `AFS_DATA_ROOT_2` for finetuning. `$TRANSCRIPTIONS` should be the .tsv file made in step 2.
4. Run `1_train_asr.sh` with `AFS_DATA_ROOT_1`.
5. Run `2_finetune.sh`. `$PRETRAIN_CKPT` should be the `checkpoint_best.pt` file from the directory you used for `$SAVE_DIR` in the previous step. Use `AFS_DATA_ROOT_2`, and set a new `$SAVE_DIR` for this step. If you want to train AFS with temporal and/or feature pruning include `--enable_afs_t` `--enable_afs_f`. Increase `--l0-norm-reg-scalar` from 0 to 1 to increase AFS induced sparsity.
6. Optional: to average the final 5 checkpoints which I find improves stability, run `average_cckpts.sh` with `$MODEL_DIR` set to the previous `$SAVE_DIR`.
7. Optional: to evaluate the word error rate (WER) of the ASR and ASR + AFS models run `asr_infer.sh` with `LS_ROOT` set to `AFS_DATA_ROOT_2`. `$CHECKPOINT_FILENAME` should be `checkpoint_best.pt` or `checkpoint_avg.pt` if you followed the previous step. 
8. Run `3_train_st.sh` with `DATA_ROOT`. Set a new `$SAVE_DIR` to save checkpoints for S2UT + AFS model. `$FEAT_EXTTRACTOR` should be path to `chekpoint_best.pt` file from the previous step's `$SAVE_DIR`. `FEAT_EXTRACTOR_ARGS` should be the path to `feat_extractor_args.tsv` in `6_AFS`.
9. Inference and evaluation can then be performed as normal following sections 4 and 5 respectively.

## 7: Document-level S2UT

After training an S2UT model with AFS 
