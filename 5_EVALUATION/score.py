import os
import csv
import numpy as np
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from sacrebleu.metrics import BLEU, CHRF, TER
# from comet import load_from_checkpoint
import argparse
from tqdm import tqdm
import sys
import io
import contextlib
import logging

# Set up logging
logging.getLogger("pytorch_lightning").setLevel(logging.ERROR)

@contextlib.contextmanager
def suppress_stdout_stderr():
    """A context manager that redirects stdout and stderr to devnull"""
    with open(os.devnull, 'w') as fnull:
        with contextlib.redirect_stderr(fnull) as err, contextlib.redirect_stdout(fnull) as out:
            yield (err, out)

def calculate_bleu(reference_sent, target_sent, smoothing_method):
    with suppress_stdout_stderr():
        chencherry = SmoothingFunction()
        smoothing_method = getattr(chencherry, smoothing_method)
        reference = [reference_sent.split()]
        target = target_sent.split()
        score = sentence_bleu(reference, target, smoothing_function=smoothing_method)
    return score

def calculate_sacrebleu(refs, tgts):
    bleu = BLEU(lowercase=True)
    scores = bleu.corpus_score(tgts, refs)
    print(bleu.get_signature())
    return(scores)

def score_targets(tgt_file, outfile, src_dict, comet_model_path, batch_size, use_comet, smoothing_method):
    
    if use_comet:
        # Load COMET model
        comet_model = load_from_checkpoint(comet_model_path, reload_hparams=True)
    
    bleu_scores = []
    comet_data = []
    comet_scores = []
    
    # Count total lines in the target file
    with open(tgt_file, 'r') as f:
        total_lines = sum(1 for _ in f)
    
    with open(tgt_file, 'r') as tgt_file, open(outfile, 'w', newline='') as out:
        tgts = csv.reader(tgt_file, delimiter="\t")
        writer = csv.writer(out, delimiter="\t")
        
        
        hypos, refs = [], [[]]
        sacrebleu_scores = []
        # Write header
        writer.writerow(["ID", "BLEU Score", "COMET Score"])
        
        for line_num, line in tqdm(enumerate(tgts, 1), desc="Scoring sentences", total=total_lines):
            id, target_sent, reference_sent = line[0], line[1], line[2]
            
            # Calculate BLEU score
            reference_sent, target_sent = reference_sent.lower(), target_sent.lower()
            
            hypos.append(target_sent)
            refs[0].append(reference_sent)
            
            # sacrebleu_scores.append(calculate_sacrebleu([[reference_sent]], [target_sent]))
            
            bleu_score = calculate_bleu(reference_sent, target_sent, smoothing_method) * 100
            bleu_scores.append(bleu_score)
            
            if use_comet:
                # Prepare data for COMET
                source_sent = src_dict.get(id, [""])[0]  # Use get() with default value
                comet_data.append({
                    "src": source_sent,
                    "mt": target_sent,
                    "ref": reference_sent
                })
                
                # If we have a full batch or it's the last item, calculate COMET scores
                if len(comet_data) == batch_size or line_num == total_lines:
                    with suppress_stdout_stderr():
                        batch_comet_scores = comet_model.predict(comet_data, batch_size=len(comet_data), gpus=0)
                    comet_scores.extend(batch_comet_scores.scores)
                    
                    # Write scores for this batch
                    for i, (bleu, comet) in enumerate(zip(bleu_scores[-len(comet_data):], batch_comet_scores.scores)):
                        writer.writerow([comet_data[i]['mt'][:40], bleu, comet])
                    
                    # Clear the batch
                    comet_data = []
            else:
                writer.writerow([id, bleu_score, "N/A"])
        
        
        
        # Calculate and write averages
        avg_bleu = np.average(bleu_scores)
        
        print(avg_bleu)
        sacrebleu_scores = calculate_sacrebleu(refs, hypos)
        print(sacrebleu_scores)
        avg_comet = np.average(comet_scores) if comet_scores else "N/A"
        
        writer.writerow(["-" * 50])
        writer.writerow(["Average BLEU", avg_bleu])
        writer.writerow(["Average sacreBLEU score", sacrebleu_scores])
        writer.writerow(["Average COMET", avg_comet])

def init_dictionary(src_tsv):
    src_dict = {}
    with open(src_tsv, 'r') as tsv_file:
        srcs = csv.reader(tsv_file, delimiter="\t")
        print("Building dictionary...")
        for line in srcs:
            src_dict[line[0][:-4]] = [line[1]]
        print("Initialised dictionary")
    return src_dict

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--tgt", type=str, help='name of experiment')
    parser.add_argument("--tgt_folder", type=str, help='transcriptions folder')
    parser.add_argument('--output_folder', type=str, help='path to folder for scores')
    parser.add_argument('--src_tsv', type=str, help='path to source tsv file with id, source sentence')
    parser.add_argument('--comet_ckpt', type=str, help='path to comet model')
    parser.add_argument('--use_comet', action='store_true', help='Use Comet for experiment tracking.')
    parser.add_argument('--batch_size', type=int, help='batch size for comet model')
    parser.add_argument('--bleu_smoothing_method', type=int, default=7, help='smoothing method variant for bleu score')
    
    args = parser.parse_args()
    
    use_comet = args.use_comet
    tgt = args.tgt
    tgt_folder = args.tgt_folder
    scores_folder = args.output_folder
    src_tsv = args.src_tsv
    tgt_file = f"{tgt_folder}/{tgt}.tsv"
    outfile = f"{scores_folder}/{tgt}_bleu_comet.tsv"
    smoothing_method = f"method{args.bleu_smoothing_method}"
    
    # Path to your pre-downloaded COMET model
    comet_model_path = args.comet_ckpt
    
    # Set batch size
    batch_size = args.batch_size
    
    src_dict = init_dictionary(src_tsv)
    score_targets(tgt_file, outfile, src_dict, comet_model_path, batch_size, use_comet, smoothing_method)

if __name__ == "__main__":
    main()
