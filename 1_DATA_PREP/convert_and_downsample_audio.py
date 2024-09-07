import os
import subprocess
from tqdm import tqdm
import argparse

def convert_and_downsample_audio(input_folder, output_folder, sample_rate=16000):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

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
            wav_filename = os.path.splitext(filename)[0] + ".wav"
            wav_path = os.path.join(output_folder, wav_filename)
            
            try:
                # Convert audio to WAV
                convert_result = subprocess.run(
                    ["ffmpeg", "-i", input_path, wav_path],
                    check=True,
                    capture_output=True,
                    text=True
                )
                
                # Downsample the WAV file to the specified sample rate
                downsampled_wav_path = os.path.join(output_folder, "downsampled_" + wav_filename)
                downsample_result = subprocess.run(
                    ["ffmpeg", "-i", wav_path, "-ar", str(sample_rate), downsampled_wav_path],
                    check=True,
                    capture_output=True,
                    text=True
                )

                # Replace original WAV file with downsampled version
                os.remove(wav_path)
                os.rename(downsampled_wav_path, wav_path)
            except subprocess.CalledProcessError as e:
                print(f"Error processing {input_path}: {e.stderr}")


def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str, required=True, help='input dir')
    parser.add_argument('--output_dir', type=str, required=True, help='output dir path')
    
    args = parser.parse_args()
    
    # Set the input and output folder paths
    input_folder = args.input_dir
    output_folder = args.output_dir

    # Run the conversion and downsampling
    convert_and_downsample_audio(input_folder, output_folder)


if __name__ == "__main__":
    main()