import os
import subprocess
from tqdm import tqdm
import argparse
import wave
import librosa
import soundfile as sf

def get_wav_info(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        return wav_file.getframerate()

def convert_and_downsample_audio_inplace(input_folder, sample_rate=16000):
    # Check if ffmpeg is available
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError:
        print("ffmpeg is not available. Please install ffmpeg and try again.")
        return

    # Loop through all files in the input folder
    for filename in tqdm(os.listdir(input_folder), desc="Processing audio files..."):
        if filename.endswith((".mp3", ".m4a", ".wav")):
            # Define the full file paths
            input_path = os.path.join(input_folder, filename)
            final_wav_path = os.path.splitext(input_path)[0] + ".wav"

            try:
                if filename.endswith((".mp3", ".m4a")):
                    # Convert non-WAV audio to WAV format using ffmpeg
                    temp_wav_path = os.path.splitext(input_path)[0] + "_temp.wav"
                    subprocess.run(
                        ["ffmpeg", "-i", input_path, "-acodec", "pcm_s16le", "-ar", str(sample_rate), temp_wav_path],
                        check=True, capture_output=True, text=True
                    )
                    os.replace(temp_wav_path, final_wav_path)
                    os.remove(input_path)
                else:  # WAV files
                    # Load the audio file
                    y, sr = librosa.load(input_path, sr=None)
                    
                    # Resample if necessary
                    if sr != sample_rate:
                        y = librosa.resample(y, orig_sr=sr, target_sr=sample_rate)
                    
                    # Save the processed audio
                    sf.write(final_wav_path, y, sample_rate)
                    
                    # Remove the original file if it's not the same as the final WAV
                    if input_path != final_wav_path:
                        os.remove(input_path)

            except subprocess.CalledProcessError as e:
                print(f"Error processing {input_path}: {e.stderr}")
            except Exception as e:
                print(f"Unexpected error processing {input_path}: {str(e)}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', type=str, required=True, help='Input directory path')
    args = parser.parse_args()

    # Set the input folder path
    input_folder = args.input_dir

    # Run the conversion and downsampling in place
    convert_and_downsample_audio_inplace(input_folder)

if __name__ == "__main__":
    main()