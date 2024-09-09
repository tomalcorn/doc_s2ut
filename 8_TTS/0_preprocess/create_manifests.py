import csv
import os
from tqdm import tqdm

def create_manifest_speeches(speeches_list, speeches_en, split, out_folder):
    outfile_name = f"speeches_{split}.tsv"
    outfile = os.path.join(out_folder, outfile_name)
    with open(speeches_list, 'r') as files, open(speeches_en, 'r') as txts, open(outfile, 'w') as f:
        f.write("id\ttext\n")
        for file_id, line in tqdm(zip(files, txts), desc=f'Making speeches manifest for {split}', total=sum(1 for _ in open(speeches_list))):
            f.write(f"{file_id.strip()}\t{line.strip()}\n")

def create_manifest_segments(segments_list, segments_en, split, out_folder):
    outfile_name = f"segments_{split}.tsv"
    outfile = os.path.join(out_folder, outfile_name)
    with open(segments_list, 'r') as files, open(segments_en, 'r') as txts, open(outfile, 'w') as f:
        reader = csv.reader(files, delimiter=' ')
        f.write("id\tstart\tfinish\ttext\n")
        for row, line in tqdm(zip(reader, txts), desc=f"Making segments manifest for {split}", total=sum(1 for _ in open(segments_list))):
            f.write(f"{row[0]}\t{row[1]}\t{row[2]}\t{line.strip()}\n")

def main():
    root = "/work/tc062/tc062/s2517781/v1.1/es/en"
    splits = ['train', 'dev', 'test']
    output_manifest_folder = "/work/tc062/tc062/s2517781/v1.1/es/manifests"
    
    if not os.path.exists(output_manifest_folder):
        os.makedirs(output_manifest_folder, exist_ok=True)
    
    # Iterate over splits for speeches
    for split in splits:
        split_path = os.path.join(root, split)
        
        speeches_list = os.path.join(split_path, 'speeches.lst')
        speeches_en = os.path.join(split_path, 'speeches.en')
        create_manifest_speeches(speeches_list, speeches_en, split, out_folder=output_manifest_folder)
        
    # Iterate over splits for segments
    for split in splits:
        split_path = os.path.join(root, split)
        
        segments_list = os.path.join(split_path, 'segments.lst')
        segments_en = os.path.join(split_path, 'segments.en')
        create_manifest_segments(segments_list, segments_en, split, out_folder=output_manifest_folder)

if __name__ == "__main__":
    main()
