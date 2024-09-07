import csv

    
input_tsv = '/work/tc062/tc062/s2517781/DATA_ROOT/src_chars/test.tsv'
output_txt = '/work/tc062/tc062/s2517781/bad_chars.txt'

# Define the allowed characters (Spanish alphabet and numbers)
allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789áéíóúüñÁÉÍÓÚÜÑ ")

# Function to check if a sequence contains only allowed characters
def is_valid_sequence(sequence):
    return all(char in allowed_chars for char in sequence)

# Read the TSV file and process the data
filenames_with_invalid_chars = []

with open(input_tsv, 'r', encoding='utf-8') as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    for row in reader:
        filename, sequence = row
        if not is_valid_sequence(sequence):
            filenames_with_invalid_chars.append(filename)

# Write the results to a TXT file
with open(output_txt, 'a', encoding='utf-8') as txtfile:
    for filename in filenames_with_invalid_chars:
        txtfile.write(filename + '\n')

print("Process completed. Check 'output.txt' for the results.")