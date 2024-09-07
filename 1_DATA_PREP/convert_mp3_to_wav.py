import os
import subprocess

def convert_and_downsample_mp3_to_wav(input_folder, output_folder, sample_rate=16000):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".mp3"):
            # Define the full file paths
            mp3_path = os.path.join(input_folder, filename)
            wav_filename = os.path.splitext(filename)[0] + ".wav"
            wav_path = os.path.join(output_folder, wav_filename)
            
            try:
                # Convert MP3 to WAV
                convert_result = subprocess.run(
                    ["ffmpeg", "-i", mp3_path, wav_path],
                    check=True,
                    capture_output=True,
                    text=True
                )
                print(f"Converted {mp3_path} to {wav_path}")
                
                # Downsample the WAV file to 16000 Hz
                downsampled_wav_path = os.path.join(output_folder, "downsampled_" + wav_filename)
                downsample_result = subprocess.run(
                    ["ffmpeg", "-i", wav_path, "-ar", str(sample_rate), downsampled_wav_path],
                    check=True,
                    capture_output=True,
                    text=True
                )
                print(f"Downsampled {wav_path} to {downsampled_wav_path} with {sample_rate} Hz")

                # Replace original WAV file with downsampled version
                os.remove(wav_path)
                os.rename(downsampled_wav_path, wav_path)
            except subprocess.CalledProcessError as e:
                print(f"Error processing {mp3_path}: {e.stderr}")

# Set the input and output folder paths
input_folder = "mine/data/es/clips"
output_folder = "mine/data/es/clips16"

# Run the conversion and downsampling
convert_and_downsample_mp3_to_wav(input_folder, output_folder)
