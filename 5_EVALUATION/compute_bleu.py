import os
import csv
# import whisper
from tqdm import tqdm
import numpy as np
from nltk.translate.bleu_score import sentence_bleu


def asr_targets(in_folder, id_file, outfile, hypothesis_dict):
    # Set up Whisper client
    print("Loading whisper model...")
    # model = whisper.load_model("medium")
    print("Whisper model complete.")

    # Get the number of wav files in the root folder and its sub-folders
    print("Getting number of files to transcribe...")
    num_files = sum(1 for filename in os.listdir(in_folder) if filename.endswith(".wav"))
    print("Number of files: ", num_files)

    # Transcribe the wav files and display a progress bar
    with tqdm(total=num_files, desc="Transcribing Files") as pbar:
        with open(id_file, 'r') as id_file, open(outfile, 'w') as f:
            ids = csv.reader(id_file, delimiter="\t")
            next(ids)  
            for id_line, filename in zip(ids, os.listdir(in_folder)):
                if filename.endswith(".wav"):
                    filepath = os.path.join(in_folder, filename)
                    # result = model.transcribe(filepath, fp16=False, verbose=True)
                    transcription = "blah blah"
                    # Write transcription to text file
                    id = id_line[0]
                    if id in hypothesis_dict:
                        f.write(f"{id}\t{transcription}\t{hypothesis_dict[id][0]}\n")
                        hypothesis_dict[id].append(transcription)
                        pbar.update(1)
    return hypothesis_dict


# def add_targets_to_dict(tgt_file, hypothesis_dict):
#     with open(tgt_file, 'r') as tgt_file:
#         tgts = csv.reader(tgt_file, delimiter="\t")
#         for line in tgts:
#             try:
#                 hypothesis_dict[line[0]].append(line[1])
#             except KeyError:
#                 raise KeyError("Not in dict??")
            
            

def calculate_bleu(reference_sent, target_sent):
    reference = reference_sent.split()
    target = target_sent.split()
    score = sentence_bleu(reference, target)
    return score

def score_targets(id_file, hypothesis_dict, outfile):
    scores = []
    with open(id_file, 'r') as id_file, open(outfile, 'w') as out:
        ids = csv.reader(id_file, delimiter="\t")
        next(ids)
        for line in ids:
            reference_sent, target_sent = hypothesis_dict[line[0]]
            score = calculate_bleu(reference_sent, target_sent)
            scores.append(score)
            out.write(f'{line[0]}\t{score}\n')
        avg_score = np.average(scores)
        out.write("-" * 50, "\n")
        out.write(f"Average Bleu: {avg_score}")

def init_dictionary(reference_tsv):
    hypothesis_dict ={}
    with open(reference_tsv, 'r') as tsv_file:
        refs = csv.reader(tsv_file, delimiter="\t")
        for line in refs:
            hypothesis_dict[line[0][:-4]] = [line[1]]
    return hypothesis_dict
    
    
def main():
    reference_tsv = "/Users/tomalcorn/Documents/University/pg/diss/DATA_ROOT/tgt_test.tsv"
    pred_wav_folder = "/Users/tomalcorn/Documents/University/pg/diss/4_INFERENCE/inference_tiny"
    tgt_file = "/Users/tomalcorn/Documents/University/pg/diss/5_EVALUATION/inference2.txt"
    id_file = "/Users/tomalcorn/Documents/University/pg/diss/DATA_ROOT/test.tsv"
    outfile = "/Users/tomalcorn/Documents/University/pg/diss/5_EVALUATION/inference2_bleu.txt"
    
    hypothesis_dict = init_dictionary(reference_tsv)
    hypothesis_dict = asr_targets(pred_wav_folder, id_file, hypothesis_dict=hypothesis_dict, outfile=tgt_file)
    # add_targets_to_dict(tgt_file, hypothesis_dict)
    
    score_targets(id_file, hypothesis_dict, outfile)
    
    
if __name__ == "__main__":
    main()
    