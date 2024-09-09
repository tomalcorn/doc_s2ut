import os
from transformers import WhisperForConditionalGeneration, WhisperProcessor
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("pretrained_model_dir", type=str, required=True, help="Directory to save whisper")
args = parser.parse_args()

pretrained_model_dir = args.pretrained_model_dir

# Ensure the directory exists
os.makedirs(pretrained_model_dir, exist_ok=True)

# Download and cache the model
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-medium")

# Download and cache the processor
processor = WhisperProcessor.from_pretrained("openai/whisper-medium")

model.save_pretrained(pretrained_model_dir)
processor.save_pretrained(pretrained_model_dir)

print("Model and processor downloaded successfully.")