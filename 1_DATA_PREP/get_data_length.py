import os
from mutagen import File
from tqdm import tqdm

def sum_audio_duration(folder_path, split):
    total_seconds = 0
    
    for filename in tqdm(os.listdir(folder_path), desc=f"getting time from {split}"):
        if filename.endswith(('.mp3', '.wav', '.flac', '.m4a')):
            file_path = os.path.join(folder_path, filename)
            audio = File(file_path)
            
            if audio is not None and hasattr(audio.info, 'length'):
                total_seconds += audio.info.length
    
    return total_seconds



folder_path_root = ''
splits = ['train', 'dev', 'dev2', 'test']
total_seconds = 0
for split in splits:
    folder_path = os.path.join(folder_path_root, split)
    split_seconds = sum_audio_duration(folder_path, split)
    total_seconds += split_seconds
    split_minutes, seconds = divmod(int(split_seconds), 60)
    hours, minutes = divmod(split_minutes, 60)
    print(f"{split} duration: {hours} hours and {minutes} minutes")
total_minutes, seconds = divmod(int(total_seconds), 60)
hours, minutes = divmod(total_minutes, 60)
print(f"Total duration: {hours} hours and {minutes} minutes")