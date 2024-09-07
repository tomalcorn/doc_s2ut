import os
import subprocess
from tqdm import tqdm
import argparse

def convert_and_downsample_audio_inplace(input_folder, sample_rate=16000):
    # Check if ffmpeg is available
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError:
        print("ffmpeg is not available. Please install ffmpeg and try again.")
        return

    # Loop through all files in the input folder
    for filename in tqdm(os.listdir(input_folder), desc="converting to wav..."):
        if filename.endswith(".mp3") or filename.endswith(".m4a") or filename.endswith(".wav"):
            # Define the full file paths
            input_path = os.path.join(input_folder, filename)
            temp_wav_filename = os.path.splitext(filename)[0] + "_temp.wav"
            temp_wav_path = os.path.join(input_folder, temp_wav_filename)
            
            try:
                # Convert audio to WAV format
                subprocess.run(
                    ["ffmpeg", "-i", input_path, temp_wav_path],
                    check=True,
                    capture_output=True,
                    text=True
                )
                
                # Downsample the WAV file to the specified sample rate
                final_wav_path = os.path.splitext(input_path)[0] + ".wav"
                subprocess.run(
                    ["ffmpeg", "-i", temp_wav_path, "-ar", str(sample_rate), final_wav_path],
                    check=True,
                    capture_output=True,
                    text=True
                )

                # Clean up temporary WAV file
                os.remove(temp_wav_path)

                # Remove the original file if it's not the final WAV
                if input_path != final_wav_path:
                    os.remove(input_path)

            except subprocess.CalledProcessError as e:
                print(f"Error processing {input_path}: {e.stderr}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str, required=True, help='Input directory path')
    args = parser.parse_args()

    # Set the input folder path
    input_folder = args.input_dir

    # Run the conversion and downsampling in place
    convert_and_downsample_audio_inplace(input_folder)

if __name__ == "__main__":
    main()