from fairseq.checkpoint_utils import load_model_ensemble_and_task_from_hf_hub
import os
import nltk
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--model-dir", type=str, help="path to PRETRAINED_MODELS")

args = parser.parse_args()


# Define the directory to save the model checkpoints and nltk data
nltk_dir = f"{args.model_dir}/nltk"
os.makedirs(nltk_dir, exist_ok=True)
model_dir = f"{args.model_dir}/fastpitch"
os.makedirs(model_dir, exist_ok=True)

nltk.download('cmudict', download_dir=nltk_dir)
nltk.download('averaged_perceptron_tagger', download_dir=nltk_dir)
# Optionally, you can verify the path:
print(nltk.data.path)


# Load the model ensemble and task from the Hugging Face Hub
models, cfg, task = load_model_ensemble_and_task_from_hf_hub(
    "facebook/fastspeech2-en-ljspeech",
    arg_overrides={"vocoder": "hifigan", "fp16": False},
    cache_dir=model_dir
)

print("Model checkpoints and configuration saved locally.")
