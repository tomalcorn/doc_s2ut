from comet import download_model, load_from_checkpoint
from transformers import XLMRobertaTokenizerFast, XLMRobertaConfig
import os
import shutil
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("pretrained_model_dir", type=str, required=True, help="Directory to save COMET")
args = parser.parse_args()

pretrained_model_dir = args.pretrained_model_dir

# Ensure the directory exists
os.makedirs(pretrained_model_dir, exist_ok=True)

# Download the COMET model
model_path = download_model("Unbabel/wmt22-comet-da", saving_directory=pretrained_model_dir)

# Load the model to ensure it's working
model = load_from_checkpoint(model_path)

# Save XLM-RoBERTa tokenizer and config
xlmr_dir = os.path.join(pretrained_model_dir, "xlm-roberta-large")
os.makedirs(xlmr_dir, exist_ok=True)

tokenizer = XLMRobertaTokenizerFast.from_pretrained("xlm-roberta-large")
tokenizer.save_pretrained(xlmr_dir)

config = XLMRobertaConfig.from_pretrained("xlm-roberta-large")
config.save_pretrained(xlmr_dir)

# Copy config.json to the main cache directory
shutil.copy(os.path.join(xlmr_dir, "config.json"), pretrained_model_dir)

print(f"Model and tokenizer saved to: {pretrained_model_dir}")

# Verify the contents of the directory
print("\nContents of the cache directory:")
for root, dirs, files in os.walk(pretrained_model_dir):
    level = root.replace(pretrained_model_dir, '').count(os.sep)
    indent = ' ' * 4 * level
    print(f"{indent}{os.path.basename(root)}/")
    subindent = ' ' * 4 * (level + 1)
    for f in files:
        print(f"{subindent}{f}")