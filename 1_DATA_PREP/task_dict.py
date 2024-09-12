import os
import csv
from num2words import num2words
import re
from tqdm import tqdm

def preprocess(sent, task):
    task = 'es' if task == 'source_letter' else 'en'
    out_words = []
    # Remove all punctuation except apostrophes
    sent = re.sub(r'[^\w\s\']', '', sent)
    words = sent.split()
    for word in words:
        word = word.upper()
        if word.isalpha() or "'" in word:
            out_words.append(word)
        elif re.match(r'\d{4}$', word):
            num_word = num2words(int(word), to='year', lang=task).upper()
            num_word = num_word.replace('-', ' ')
            out_words.extend(num_word.split())
        elif word.isnumeric():
            num_word = num2words(int(word), lang=task).upper()
            # Remove hyphens from the number words
            num_word = num_word.replace('-', ' ')
            out_words.extend(num_word.split())
    return ' '.join(out_words)

def get_chars(sent, task):
    if task != 'decoder_target_ctc':
        output = [word for word in sent if word.isalpha()]
        output = [char.lower() for char in output]
        return ' '.join(output)
    return sent

import csv
import os
from tqdm import tqdm

def task_dic_maker(task, in_wavs, in_tsv, split, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(in_tsv, 'r', newline='', encoding='utf-8') as tsv_file, \
         open(f'{output_folder}/{split}.tsv', 'w', newline='', encoding='utf-8') as output_file:
        
        reader = csv.reader(tsv_file, delimiter="\t")
        writer = csv.writer(output_file, delimiter="\t")
        writer.writerow(['id', 'tgt_text'])

        # Count total lines
        total_lines = sum(1 for _ in tsv_file)
        tsv_file.seek(0)

        processed_lines = 0
        skipped_lines = 0
        empty_lines = 0
        
        for line_num, row in enumerate(tqdm(reader, desc=f"Processing {task}-{split}", total=total_lines), start=1):
            if not row:
                empty_lines += 1
                print(f"Empty line at line {line_num}")
                continue

            if len(row) != 2:
                print(f"Malformed line at line {line_num}: {row}")
                skipped_lines += 1
                continue

            filename, sentence = row
            file_path = os.path.join(in_wavs, filename)
            
            if not os.path.exists(file_path):
                print(f"Audio file not found: {file_path} (line {line_num})")
                skipped_lines += 1
                continue

            try:
                sentence = preprocess(sentence, task)
                if task in ['source_letter', 'target_letter', 'decoder_target_ctc']:
                    target = get_chars(sentence, task)
                    if filename.endswith(".wav"):
                        filename = filename[:-4]
                    writer.writerow([filename, target])
                    processed_lines += 1
            except Exception as e:
                print(f"Error processing line {line_num}: {e}")
                skipped_lines += 1

        print(f"Processed lines: {processed_lines}")
        print(f"Skipped lines: {skipped_lines}")

    return processed_lines, skipped_lines, empty_lines, total_lines
            
            