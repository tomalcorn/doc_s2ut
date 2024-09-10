import os
import soundfile as sf
from tqdm import tqdm
import argparse

def get_audio_duration_in_frames(file_path):
    with sf.SoundFile(file_path) as audio_file:
        frames = len(audio_file)
    return frames

def create_manifest(root_directory, manifest_path, split):
    with open(manifest_path, 'w') as manifest_file:
        manifest_file.write(f"{root_directory}\n")

        # Collect all audio file paths
        audio_files = []
        for subdir, _, files in os.walk(root_directory):
            for file in files:
                if file.endswith(".wav"):  # Adjust the extension if needed (e.g., .mp3)
                    file_path = os.path.join(subdir, file)
                    relative_path = os.path.relpath(file_path, root_directory)
                    audio_files.append(relative_path)

        # Sort the audio file paths
        audio_files.sort()

        # Write the sorted audio files to the manifest
        for relative_path in tqdm(audio_files, desc=f"writing manifest for {split}"):
            file_path = os.path.join(root_directory, relative_path)
            frames = get_audio_duration_in_frames(file_path)
            manifest_file.write(f"{relative_path}\t{frames}\n")


def main():
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--manifest-dir", type=str, help="path to output manifest directory")
    parser.add_argument("--audio-dir", type=str, help="path to audio dir split")
    parser.add_argument("--lang-code", type=str, help="short language code for source or target language")
    parser.add_argument("--split", type=str, help="split name: train, dev etc.")
    
    args = parser.parse_args()
    
    # Set the root directory containing audio files and the path to the manifest file
    manifest_directory = args.manifest_dir

    # check exists
    os.makedirs(manifest_directory, exist_ok=True)

    root_directory = args.audio_dir
    lang = args.lang_code
    folder = args.split
    manifest_path = f"{manifest_directory}/{lang}_{folder}.tsv"

    # Create the manifest file
    create_manifest(root_directory, manifest_path, split=folder)


if __name__ == "__main__":
    main()