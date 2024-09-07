import csv
import string

def filter_tsv(input_file_path, output_file_path, banned_words):
    banned_words_set = set(word.lower() for word in banned_words)
    punctuation_table = str.maketrans('', '', string.punctuation)
    
    def clean_word(word):
        return word.translate(punctuation_table).lower()
    
    with open(input_file_path, 'r', newline='') as infile, open(output_file_path, 'w', newline='') as outfile:
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')
        
        for row in reader:
            if len(row) < 3:
                # Skip lines that do not have at least 3 fields
                continue
            
            reference_translation = row[-1].strip()
            words = reference_translation.lower().split()
            
            if len(words) == 1:
                # Skip lines where the reference translation contains only one word
                continue
            
            cleaned_words = [clean_word(word) for word in words]
            
            if any(clean_word(word) in banned_words_set for field in row for word in field.split()):
                continue
            
            writer.writerow(row)


# Usage
input_file_path = '/Users/tomalcorn/Documents/University/pg/diss/5_EVALUATION/text_out/fisher_1.tsv'
output_file_path = '/Users/tomalcorn/Documents/University/pg/diss/5_EVALUATION/text_out/fisher_1_clean.tsv'
banned_words = ["hm",
                "hm",
                "hmmm",
                'm',
                'mm',
                'mmm',
                'mhm',
                'mhmm'
                'oh',
                'aha',
                'ah',
                'yea',
                'yeah',
                'Ok',
                'right',
                'uh',
                'um'
                ]  # Add your banned words here

filter_tsv(input_file_path, output_file_path, banned_words)
