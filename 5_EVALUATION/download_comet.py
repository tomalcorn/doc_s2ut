from comet import download_model, load_from_checkpoint
from transformers import XLMRobertaTokenizerFast, XLMRobertaConfig
import os
import shutil

# Set the cache directory
cache_dir = "/work/tc062/tc062/s2517781/.cache"

# Ensure the directory exists
os.makedirs(cache_dir, exist_ok=True)

# Download the COMET model
model_path = download_model("Unbabel/wmt22-comet-da", saving_directory=cache_dir)

# Load the model to ensure it's working
model = load_from_checkpoint(model_path)

# Save XLM-RoBERTa tokenizer and config
xlmr_dir = os.path.join(cache_dir, "xlm-roberta-large")
os.makedirs(xlmr_dir, exist_ok=True)

tokenizer = XLMRobertaTokenizerFast.from_pretrained("xlm-roberta-large")
tokenizer.save_pretrained(xlmr_dir)

config = XLMRobertaConfig.from_pretrained("xlm-roberta-large")
config.save_pretrained(xlmr_dir)

# Copy config.json to the main cache directory
shutil.copy(os.path.join(xlmr_dir, "config.json"), cache_dir)

print(f"Model and tokenizer saved to: {cache_dir}")

# Verify the contents of the directory
print("\nContents of the cache directory:")
for root, dirs, files in os.walk(cache_dir):
    level = root.replace(cache_dir, '').count(os.sep)
    indent = ' ' * 4 * level
    print(f"{indent}{os.path.basename(root)}/")
    subindent = ' ' * 4 * (level + 1)
    for f in files:
        print(f"{subindent}{f}")