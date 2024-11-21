# Document-level Speech to discrete unit translation

This repository contains the accompanying code to my master's dissertation project: [The eﬀect of extra-sentential context on Speech to Discrete Unit Translation](https://github.com/tomalcorn/doc_s2ut/blob/main/Speech_to_Discrete_Unit_Translation.pdf). In the aforememntioned project I implement a Speech to Discrete Unit Translation (S2UT) Model described in [Lee et al. (2021)](https://arxiv.org/pdf/2107.05604), whose implementation is described in brief here, and can be found in full in their [Fairseq github repo](https://github.com/facebookresearch/fairseq/blob/main/examples/speech_to_speech/docs/direct_s2st_discrete_units.md). 

I then extend this model to incorporate extra-sentential context from the input. Extending the context window like this necesitates removing redundant information from the input: for this I use Adaptive Feature Selection ([Zhang et al. (2020)](https://arxiv.org/pdf/2010.08518)).

<p align="center">
  <img src="https://github.com/tomalcorn/doc_s2ut/blob/main/AFS%20into%20S2UT.gif" />
</p>

To implement the sentence-level Speech to Discrete Unit translation model, follow steps 1-5 listed below. To add AFS and extend the context window to incorporate extra-sentential information follow the remaining steps.

## Installation and setup

1. Clone this repository:

    ```
    git clone https://github.com/tomalcorn/doc_s2ut.git
    cd doc_s2ut
    ```

2. Make a python virtual environment with Python version >= 3.8
3. Download necessary dependencies, then clone the doc-s2ut fairseq branch and install fairseq:

    ```
    pip install -r requirements.txt
    git clone --branch doc-s2ut https://github.com/tomalcorn/fairseq.git
    cd fairseq
    pip install --editable ./

    # on MacOS:
    # CFLAGS="-stdlib=libc++" pip install --editable ./

    # to install the latest stable release (0.10.x)
    # pip install fairseq
    ```

4. Run the code below:

    ```
    mkdir SRC_AUDIO
    mkdir TGT_AUDIO
    mkdir DATA_ROOT
    mkdir PRETRAINED_MODELS
    cd PRETRAINED_MODELS

    # Download Vocoder and Vocoder config
    wget https://dl.fbaipublicfiles.com/fairseq/speech_to_speech/vocoder/code_hifigan/hubert_base_100_lj/g_00500000
    wget https://dl.fbaipublicfiles.com/fairseq/speech_to_speech/vocoder/code_hifigan/hubert_base_100_lj/config.json
    mv ./config.json ./vocoder_config.json
    mv ./g_00500000 ./vocoder

    # Download Hubert model and Quantisation model
    wget https://dl.fbaipublicfiles.com/hubert/hubert_base_ls960.pt
    wget https://dl.fbaipublicfiles.com/textless_nlp/gslm/hubert/km100/km.bin
    mv ./km.bin ./quantisation_model.bin
    ```

## Data

To begin data preparation for S2UT or document-level S2UT, you need:

- Paired source and target speech. Optionally if you have source speech and target text or vice versa use section 0: Text-To-Speech to synthesise the text to speech.
- In [my experiments](https://github.com/tomalcorn/doc_s2ut/blob/main/Speech_to_Discrete_Unit_Translation.pdf) I used Fisher and CVSS Spanish-English datasets. For CVSS I used Common Voice corpus 7.0:
- [CVSS Spanish-English data - source audio](https://commonvoice.mozilla.org/en/datasets)
- [CVSS Spanish-English data - target audio](https://storage.googleapis.com/cvss/cvss_c_v1.0/cvss_c_es_en_v1.0.tar.gz)
- [Fisher data](https://catalog.ldc.upenn.edu/LDC2014T23)
- Information on how to split data in training, validation and test sets.
- Move all source audio files to `SRC_AUDIO` and all target audio to `TGT_AUDIO`. Each pair of files should be named identically in their respective directories.

## 0: Optional: Text-to-Speech

If your dataset is paired source speech with target text then you first need to synthesise the target text into speech with Text-To-Speech (TTS). Otherwise skip to section 1.

1. First follow steps 1-4 from section 1.
2. Run `0_download_fastpitch.sh` with `$MODEL_DIR` set to the path to `PRETRAINED_MODELS`.
3. Run `1_fastpitch.sh` for each dataset split eg. train, dev, test etc. `OUTPUT_DIR` should be the path to `TGT_AUDIO`. `$NLTK` should be the path to `NLTK` save directory in `PRETRAINED_MODELS`. `FASTPITCH_DIR` should be the path to the fastpitch model and should look something like this:

```
   ./PRETRAINED_MODELS/fastpitch/modelsmodels--facebook--fastspeech2-en-ljspeech/snapshots/a3e3e5e2e62bb7ca7514b11aa469e9c5b01a20bf
```

4. Proceed with step 5 from section 1.

## 1: Data Prep

1. Optional: Run `0_dir1vdir2.sh` to move any file in `SRC_AUDIO` and not `TGT_AUDIO` and vice versa to backup directories.
2. Run `1_convert_and_downsample.sh` to convert source and/or target audio to wav if necessary and to downsample to 16kHz. `--input_dir` should be path to `SRC_AUDIO` or `TGT_AUDIO`.
3. In `DATA_ROOT` create `src_$SPLIT.tsv` and `tgt_$SPLIT.tsv` for each dataset split, with format:
`$FILE_ID.wav   $corresponding_text`
4. Split downsampled files in `SRC_AUDIO` and `TGT_AUDIO` into splits, eg `SRC_AUDIO/train`, `SRC_AUDIO/dev`, `SRC_AUDIO/test`... If using CVSS and you followed the previous step this can be quickly done by running `python 1_DATA_PREP/split_cvss.py`.
5. Run `2_manifest_maker.sh` to create manifest files for `SRC_AUDIO` and `TGT_AUDIO` with the relevant arguments.
6. Run `3_quantise_tgts.sh` to quantise target audio for each split in `TGT_AUDIO`
7. Run `4_data_prep.sh` with relevant arguments.
8. Run `5_multitask_prep.sh` to prepare multitask information. Currently only `'source_letter'`, and/or`'target_letter'` and/or `'decoder_tgt_ctc'` are supported.
9. Create `./DATA_ROOT/config_multitask.yaml`. Below is an example of the config used for S2UT "reduced" with two encoder multitasks (`source_letter`, `target_letter`) and one decoder CTC task (`decoder_target_ctc`).

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


2. Make a transcription .tsv manifest file for the full dataset. `audio` should be the file basename for each file without any extension, `text` should be the corresponding transcription. The file should have the following header:
   
   ```
    audio   text
   ```
3. Run `0_prep_asr_data.sh` with given arguments. Run twice with `$AUDIOROOT` set to path to dataset used for asr training, then for finetuning. Use `DATA_ROOT_AFS_1` for asr pretraining and `DATA_ROOT_AFS_2` for finetuning. `$TRANSCRIPTIONS` should be the .tsv file made in step 2.
4. Run `1_train_asr.sh` with `DATA_ROOT_AFS_1`.
5. Run `2_finetune.sh`. `$PRETRAIN_CKPT` should be the `checkpoint_best.pt` file from the directory you used for `$SAVE_DIR` in the previous step. Use `DATA_ROOT_AFS_2`, and set a new `$SAVE_DIR` for this step. If you want to train AFS with temporal and/or feature pruning include `--enable_afs_t` `--enable_afs_f`. Increase `--l0-norm-reg-scalar` from 0 to 1 to increase AFS induced sparsity.
6. Optional: to average the final 5 checkpoints which I find improves stability, run `average_ckpts.sh` with `$MODEL_DIR` set to the previous `$SAVE_DIR`.
7. Optional: to evaluate the word error rate (WER) of the ASR and ASR + AFS models run `asr_infer.sh` with `LS_ROOT` set to `DATA_ROOT_AFS_2`. `$CHECKPOINT_FILENAME` should be `checkpoint_best.pt` or `checkpoint_avg.pt` if you followed the previous step. 
8. Run `3_train_st.sh` with `DATA_ROOT`. Set a new `$SAVE_DIR` to save checkpoints for S2UT + AFS model. `$FEAT_EXTTRACTOR` should be path to `chekpoint_best.pt` or `checkpoint_avg.pt` file from the previous step's `$SAVE_DIR`. `FEAT_EXTRACTOR_ARGS` should be the path to `feat_extractor_args.tsv` in `6_AFS`.
9. Inference and evaluation can then be performed as normal following sections 5 and 6 respectively.

## 7: Document-level S2UT

After training an S2UT model with AFS, this model can be finetuned for document translation. For the concatenative-ST approach you need a **pre-segmented dataset**, in other words a dataset where the samples are longer passages of speech, with accompanying instructions on how to split the passages into sentence like chunks. Split these samples into segments where each segment should be named with at least two fields separated by '_': the document id and either the start time of the segment in the document or some other ordered index to refer to the segments position in the document. For example, `doc116734_2.006_3.566.wav`. Move these samples into `SRC_AUDIO_DOC` and `TGT_AUDIO_DOC`, making sure that pairs of samples are named identically in the two folders.

1. Run preprocessing steps 1-7 from section 1, but using `SRC_AUDIO_DOC`, `TGT_AUDIO_DOC` and `DATA_ROOT_DOC` instead of the original values.
2. Run `7_DOC/0_add_doc_info.sh` to add document information to the created manifest files. `$SPLITS` should be a comma separated string of dataset split names, eg. "train,dev,test". `$DOC_CTXT_SIZE` is the number of prefix source and target segments the model is trained with. 
3. Continue with the preprocessing steps from section 1.
4. Run `1_train_doc.sh`. `$PRETRAINING_PATH` should point to the pretrained S2UT + AFS save directory. `$FEAT_EXTRACTOR` and `$FEAT_EXTRACTOR_ARGS` should point to the ASR + AFS save directory and `6_AFS/feat_extractor_args.tsv` respectively. Set `--doc-context-size` to the same used in step 2. By default the loss will be computed only over the current segment, I find better performance comes from computing the loss over the full sequence including prefix segments. To do this, include `--extended-loss`. 
5. Run `2_infer_doc.sh`. Ensure `--doc-context-size` is set to the same as from previous steps. To use SWBD-IMED interpolation include `--use-imed` and set `--imed-gamma` between 0 and 1, where closer to 1 results in greater reliance on the sentence-level prediction, closer to 0 results in greater reliance on the document-level prediction.
6. Perform evaluation following section 6.


