from pydub import AudioSegment
import os

def downsample_audio(input_folder, output_folder, sample_rate=16000):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".mp3") or filename.endswith(".wav"):
            # Define the full file paths
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            
            # Load the audio file
            audio = AudioSegment.from_file(input_path)
            
            # Downsample the audio file
            audio = audio.set_frame_rate(sample_rate)
            
            # Export the downsampled audio file
            audio.export(output_path, format="wav")
            print(f"Downsampled {input_path} to {output_path} at {sample_rate} Hz")

# Set the input and output folder paths
input_folder = "data/es/train"
output_folder = "data/es/train16"

# Run the downsampling
downsample_audio(input_folder, output_folder)
