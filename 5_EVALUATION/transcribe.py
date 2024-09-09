import os
import csv
import whisper
from tqdm import tqdm
import re
from natsort import natsorted
import argparse

def asr_targets(data_root, in_folder, id_file, outfile, hypothesis_dict):
    # Set up Whisper client
    print("Loading whisper model...")
    model_path = f"{data_root}/../0_PRETRAINED_MODELS/whisper/medium.en.pt"

    # Assert that the path exists
    assert os.path.exists(model_path), f"Model path does not exist: {model_path}"

    # Load the model
    model = whisper.load_model(model_path)
    print("Whisper model complete.")

    # Get the number of wav files in the root folder and its sub-folders
    print("Getting number of files to transcribe...")
    num_files = sum(1 for filename in os.listdir(in_folder) if filename.endswith(".wav"))
    print("Number of files: ", num_files)

    # Transcribe the wav files and display a progress bar
    with tqdm(total=num_files, desc="Transcribing Files") as pbar:
        with open(id_file, 'r') as id_file, open(outfile, 'w', newline='') as f:
            writer = csv.writer(f, delimiter="\t")
            ids = csv.reader(id_file, delimiter="\t")
            next(ids)
            wavs = os.listdir(in_folder)
            wavs = natsorted(wavs)
            for id_line, filename in zip(ids, wavs):
                if filename.endswith(".wav"):
                    filepath = os.path.join(in_folder, filename)
                    result = model.transcribe(filepath, fp16=False)
                    pattern = r'[^\w\s]'
                    transcription = result["text"].lower()
                    transcription = re.sub(pattern, '', transcription)
                    # Write transcription to TSV file
                    id = id_line[0]
                    writer.writerow([id, transcription, hypothesis_dict[id][0]])
                    hypothesis_dict[id].append(transcription)
                    pbar.update(1)
    return hypothesis_dict

def init_dictionary(reference_tsv):
    hypothesis_dict = {}
    with open(reference_tsv, 'r') as tsv_file:
        refs = csv.reader(tsv_file, delimiter="\t")
        print("Building dictionary...")
        for line in refs:
            hypothesis_dict[line[0][:-4]] = [line[1]]
        print("Initialised dictionary")
    return hypothesis_dict

def main():
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "--variant",
        type=str,
        help = "base name of directory in 4_INFERENCE"
    )
    parser.add_argument(
        "--data-root",
        type=str,
        help = "DATA_ROOT basename"
    )
    
    args = parser.parse_args()
    
    variant = args.variant
    data_root = args.data_root
    
    # tsv with ids and gold sentences
    tgt_test_tsv = f"{data_root}/tgt_test.tsv"
    pred_wav_folder = f"{data_root}/../4_INFERENCE/{variant}"
    tgt_file = f"{data_root}/../5_EVALUATION/text_out/{variant}.tsv"
    # Cleaned tsv file with ids in the same order as the wav files
    id_file = f"{data_root}/../5_EVALUATION/cleaned/{variant}.tsv"
    
    hypothesis_dict = init_dictionary(tgt_test_tsv)
    hypothesis_dict = asr_targets(data_root, in_folder=pred_wav_folder, id_file=id_file, hypothesis_dict=hypothesis_dict, outfile=tgt_file)

if __name__ == "__main__":
    main()
