import os
import csv
import argparse
from tqdm import tqdm
import soundfile as sf
import torch
from fairseq.checkpoint_utils import load_model_ensemble_and_task
from fairseq.models.text_to_speech.hub_interface import TTSHubInterface
import nltk

def move_to_device(obj, device):
    if torch.is_tensor(obj):
        return obj.to(device)
    elif isinstance(obj, dict):
        return {k: move_to_device(v, device) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [move_to_device(v, device) for v in obj]
    else:
        return obj

def generate_audio(text, output_file, task, model, generator, device):
    sample = TTSHubInterface.get_model_input(task, text)
    sample = move_to_device(sample, device)
    with torch.no_grad():
        wav, rate = TTSHubInterface.get_prediction(task, model, generator, sample)
    sf.write(output_file, wav.cpu().numpy(), rate)

def main():
    parser = argparse.ArgumentParser(description="Generating speech from text files.")
    parser.add_argument('--output-dir', type=str, required=True, help='output directory path for speech files.')
    parser.add_argument('--data-root', type=str, required=True, help='manifest directory for text and id tsv files.')
    parser.add_argument('--model-dir', type=str, required=True, help="path to model directory.")
    parser.add_argument('--nltk', type=str, required=True, help="nltk data path")
    parser.add_argument('--split', type=str, required=True, help='split name')
    parser.add_argument('--device', type=str, choices=['cpu', 'cuda'], default='cpu', help="Device to use (cpu or cuda)")
    args = parser.parse_args()

    MANIFESTDIR = args.manifest_dir
    OUTPUT_DIR_ROOT = args.output_dir
    SHARED_DIR = args.model_dir
    device = torch.device(args.device if torch.cuda.is_available() and args.device == 'cuda' else 'cpu')
    
    # Set the path to your copied NLTK data
    nltk_data_path = args.nltk
    nltk.data.path.append(nltk_data_path)
    

    print(f"Using device: {device}")

    # Build models
    models, cfg, task = load_model_ensemble_and_task(
        [os.path.join(SHARED_DIR, 'pytorch_model.pt')],
        arg_overrides={"data": SHARED_DIR, 'fp16': False}
    )
    model = models[0].to(device)
    TTSHubInterface.update_cfg_with_data_cfg(cfg, task.data_cfg)
    generator = task.build_generator(models, cfg)

    # Move generator to the same device as the model
    generator = move_to_device(generator, device)

    # Ensure task is on the correct device
    task = move_to_device(task, device)

    splits = [args.split]

    for split in splits:
        TSV_FILE = os.path.join(MANIFESTDIR, f'tgt_{split}.tsv')
        OUTPUT_DIR = os.path.join(OUTPUT_DIR_ROOT, split)
        
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        with open(TSV_FILE, 'r', newline='', encoding='utf-8') as tsvfile:
            reader = csv.reader(tsvfile, delimiter='\t')
            total_lines = sum(1 for line in tsvfile)
            tsvfile.seek(0)
            
            for row in tqdm(reader, desc=f"Synthesising speech for files in {split}", total=total_lines):
                if len(row) >= 2:
                    file_name = row[0]
                    text = row[1]
                    output_file = os.path.join(OUTPUT_DIR, f"{file_name}")
                    generate_audio(text, output_file, task, model, generator, device)

        print(f"All speech files have been generated for {split}.")

if __name__ == "__main__":
    main()