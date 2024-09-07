from transformers import WhisperForConditionalGeneration, WhisperProcessor

# Download and cache the model
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-medium")

# Download and cache the processor
processor = WhisperProcessor.from_pretrained("openai/whisper-medium")

model.save_pretrained("/work/tc062/tc062/s2517781/.cache/whisper-medium")
processor.save_pretrained("/work/tc062/tc062/s2517781/.cache/whisper-medium")

print("Model and processor downloaded successfully.")