import os
import shutil
import pandas as pd

def process_split_tsv_files(tsv_files, src_audio_dir, tgt_audio_dir):
    """
    Processes each TSV file to move corresponding .wav files from SRC_AUDIO and TGT_AUDIO
    into split-specific directories.

    Args:
        tsv_files (list of str): List of paths to TSV files (one per split).
        src_audio_dir (str): Path to the source audio directory (SRC_AUDIO).
        tgt_audio_dir (str): Path to the target audio directory (TGT_AUDIO).
    """

    # Process each TSV file
    for tsv_file in tsv_files:
        # Extract the split name from the TSV file name (e.g., "train", "test", "dev")
        split_name = os.path.basename(tsv_file).split("_")[1][:-4]

        # Create a directory for the split inside the output directory
        split_dir_src = os.path.join(src_audio_dir, split_name)
        split_dir_tgt = os.path.join(tgt_audio_dir, split_name)
        os.makedirs(split_dir_src, exist_ok=True)
        os.makedirs(split_dir_tgt, exist_ok=True)

        # Read the TSV file using pandas
        try:
            tsv_data = pd.read_csv(tsv_file, sep='\t', header=None, names=['id', 'text'])
        except Exception as e:
            print(f"Error reading {tsv_file}: {e}")
            continue

        # Iterate over each row in the TSV file
        for index, row in tsv_data.iterrows():
            file_id = row['id']

            # Define the source and target file paths
            src_wav_path = os.path.join(src_audio_dir, f"{file_id}.wav")
            tgt_wav_path = os.path.join(tgt_audio_dir, f"{file_id}.wav")

            # Define the destination paths in the split directory
            dest_src_wav_path = os.path.join(split_dir_src, f"{file_id}.wav")
            dest_tgt_wav_path = os.path.join(split_dir_tgt, f"{file_id}.wav")

            # Move the SRC audio file if it exists
            if os.path.exists(src_wav_path) and os.path.exists(tgt_wav_path):
                try:
                    shutil.move(src_wav_path, dest_src_wav_path)
                    print(f"Moved {src_wav_path} to {dest_src_wav_path}")
                except Exception as e:
                    print(f"Error moving {src_wav_path}: {e}")
            
            # Move the TGT audio file if it exists
            if os.path.exists(tgt_wav_path):
                try:
                    shutil.move(tgt_wav_path, dest_tgt_wav_path)
                    print(f"Moved {tgt_wav_path} to {dest_tgt_wav_path}")
                except Exception as e:
                    print(f"Error moving {tgt_wav_path}: {e}")

# Example usage:
data_root = "./DATA_ROOT"
tsv_files = [os.path.join(data_root, f) for f in os.listdir(data_root)]
src_audio_dir = "./SRC_AUDIO"
tgt_audio_dir = "./TGT_AUDIO"

process_split_tsv_files(tsv_files, src_audio_dir, tgt_audio_dir)