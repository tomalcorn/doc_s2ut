import os
from collections import defaultdict

def extract_dict_entries(file_path, all_entries, task):
    with open(file_path, 'r', encoding='utf-8') as f:
        first_line = True
        for line in f:
            if first_line:
                first_line = False
                continue
            if '\t' in line:
                _, tgt_text = line.strip().split('\t')
                if task == "decoder_target_ctc":
                    
                    for word in tgt_text.split():
                        all_entries[word] += 1
                else:
                    for char in tgt_text.replace(' ', ''):
                        all_entries[char] += 1
    return all_entries

def write_dictionary(output_dir, characters):
    sorted_chars = sorted(characters.items(), key=lambda x: x[1], reverse=True)
    dict_file = os.path.join(output_dir, 'dict_tmp.txt')
    with open(dict_file, 'w', encoding='utf-8') as f:
        for idx, (char, freq) in enumerate(sorted_chars, start=4):
            f.write(f"{char} {freq}\n")

def main(task, data_root):
    data_root = os.path.join(data_root, task)
    output_dir = data_root

    os.makedirs(output_dir, exist_ok=True)

    file1 = os.path.join(data_root, "train.tsv")
    file2 = os.path.join(data_root, "dev.tsv")
    file3 = os.path.join(data_root, "test.tsv")

    all_characters = defaultdict(int)

    all_characters = extract_dict_entries(file1, all_characters, task)
    all_characters = extract_dict_entries(file2, all_characters, task)
    all_characters = extract_dict_entries(file3, all_characters, task)

    write_dictionary(output_dir, all_characters)

    return os.path.join(output_dir, 'dict_tmp.txt')

if __name__ == "__main__":
    main()
