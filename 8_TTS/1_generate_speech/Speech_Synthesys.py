#!/usr/bin/env python
# coding: utf-8
import csv
import torch
import torchaudio
import speechbrain as sb
from tqdm import tqdm
from speechbrain.inference.TTS import Tacotron2
from speechbrain.inference.vocoders import HIFIGAN
import os
import argparse
import re
from num2words import num2words
import nltk
from nltk.tokenize import word_tokenize

# Set the NLTK data path
os.environ['NLTK_DATA'] = '/path/to/your/nltk_data'
nltk.data.path.append('/path/to/your/nltk_data')

class SpeechToText:
    def __init__(self, device='cuda' if torch.cuda.is_available() else 'cpu', max_decoder_steps=3000) -> None:
        self.tacotron2 = Tacotron2.from_hparams(
            source="speechbrain/tts-tacotron2-ljspeech",
            savedir="tmpdir_tts",
            run_opts={"device": device}
        )
        # Increase max_decoder_steps
        self.tacotron2.hparams.modules['model'].decoder.max_decoder_steps = max_decoder_steps
        
        self.hifi_gan = HIFIGAN.from_hparams(
            source="speechbrain/tts-hifigan-ljspeech",
            savedir="tmpdir_vocoder",
            run_opts={"device": device}
        )
        self.device = device

    # Function to generate speech from a batch of texts and save as WAV files
    def batch_text_to_speech(self, texts, filenames):
        sorted_texts, sorted_filenames = self.sort_by_text_length(texts, filenames)
        
        mel_outputs, mel_lengths, alignments = self.tacotron2.encode_batch(sorted_texts)
        
        waveforms = self.hifi_gan.decode_batch(mel_outputs)
        
        for (waveform, mel_length, filename) in zip(waveforms, mel_lengths, sorted_filenames):
            ratio = waveform.shape[1] / mel_outputs.shape[2]
            wav_length = int(mel_length * ratio)
            trimmed_waveform = waveform[:, :wav_length]
            
            torchaudio.save(filename, trimmed_waveform.cpu().squeeze(1), 22050)

            
    def sort_by_text_length(self, texts, filenames):
        # Get the length of encoded sequences
        lens = [len(self.tacotron2.text_to_seq(item)[0]) for item in texts]
        # Sort based on these lengths
        sorted_data = sorted(zip(lens, texts, filenames), key=lambda x: x[0], reverse=True)
        _, sorted_texts, sorted_filenames = zip(*sorted_data)
        return list(sorted_texts), list(sorted_filenames)
    
def preprocess_text(text):
    # Define abbreviations
    abbreviations = {
        "Mr.": "Mister",
        "Mrs.": "Misses",
        "Dr.": "Doctor",
        "Prof.": "Professor",
        # Add more abbreviations as needed
    }

    # Tokenize the text
    words = word_tokenize(text)

    # Process each word
    processed_words = []
    for word in words:
        # Expand abbreviations
        if word in abbreviations:
            processed_words.append(abbreviations[word])
        # Handle years
        elif re.match(r'\d{4}$', word):
            processed_words.append(num2words(int(word), to='year'))
        # Convert numbers to words
        elif word.isdigit():
            processed_words.append(num2words(int(word)))
        # Handle ordinals (1st, 2nd, 3rd, etc.)
        elif re.match(r'\d+(?:st|nd|rd|th)$', word):
            number = int(re.findall(r'\d+', word)[0])
            processed_words.append(num2words(number, to='ordinal'))
        else:
            processed_words.append(word)

    # Join the words back into a string
    processed_text = ' '.join(processed_words)
    
    # Use regex to fix spacing around punctuation
    processed_text = re.sub(r'\s([?.!,;:](?:\s|$))', r'\1', processed_text)
    processed_text = re.sub(r'\s+', ' ', processed_text)  # Remove extra spaces

    return processed_text

def main():
    parser = argparse.ArgumentParser(description="Generating speech from text files.")
    parser.add_argument('--output_dir', type=str, required=True, help='output directory path for speech files.')
    parser.add_argument('--manifest_dir', type=str, required=True, help='manifest directory for text and id tsv files.')
    parser.add_argument('--batch_size', type=int, default=32, help='batch size for processing')
    parser.add_argument('--max_decoder_tsteps', type=int, default=2000, help='num decoder time steps')
    
    args = parser.parse_args()

    OUTPUTDIR = args.output_dir
    MANIFESTDIR = args.manifest_dir
    BATCH_SIZE = args.batch_size
    DECODERTSTEPS = args.max_decoder_tsteps
    splits = ['train', 'dev', 'test']

    os.makedirs(OUTPUTDIR, exist_ok=True)

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    tts = SpeechToText(device, max_decoder_steps=DECODERTSTEPS)

    for split in splits:
        manifest_file = f'segments_{split}.tsv'
        textfile = os.path.join(MANIFESTDIR, manifest_file)

        # Read the input text file
        with open(textfile, "r") as file:
            reader = csv.reader(file, delimiter="\t")
            total_lines = sum(1 for _ in open(textfile)) - 1  # Subtract 1 for the header
            file.seek(0)  # Reset file pointer to beginning
            next(reader)  # Skip header

            batch_texts = []
            batch_filenames = []
            batches_processed = 0

            for i, line in tqdm(enumerate(reader), desc=f"Generating speech files for {split} split", total=total_lines):
                id, start, finish, sentence = line
                preprocessed_sentence = preprocess_text(sentence)
                output_file_name = f"{id}_{start}_{finish}.wav"  # Changed ':' to '_'
                output_dir = os.path.join(OUTPUTDIR, split)
                # Check exists
                os.makedirs(output_dir, exist_ok=True)
                output_file = os.path.join(output_dir, output_file_name)

                batch_texts.append(preprocessed_sentence)
                batch_filenames.append(output_file)

                if len(batch_texts) == BATCH_SIZE:
                    # sorted_texts, sorted_filenames = sort_by_text_length(batch_texts, batch_filenames)
                    tts.batch_text_to_speech(batch_texts, batch_filenames)
                    batches_processed += 1
                    batch_texts = []
                    batch_filenames = []

                # Process any remaining items
                if batch_texts and i == total_lines:
                    # sorted_texts, sorted_filenames = sort_by_text_length(batch_texts, batch_filenames)
                    tts.batch_text_to_speech(batch_texts, batch_filenames)

    print("All sentences processed and saved as WAV files.")

if __name__ == "__main__":
    main()