import os
import csv
import argparse

def filter_tsv_by_missing_ids(tsv_file, missing_ids_file, output_file):
    # Read the missing IDs from the file and store them in a set
    with open(missing_ids_file, 'r') as f:
        missing_ids = set(line.strip() for line in f)

    # Read the TSV file, filter lines, and write the results to the output file
    with open(tsv_file, 'r') as tsv, open(output_file, 'w', newline='') as out:
        reader = csv.reader(tsv, delimiter='\t')
        writer = csv.writer(out, delimiter='\t')

        for line in reader:
            id_field = line[0]
            if id_field not in missing_ids:
                writer.writerow(line)

# Example usage
parser = argparse.ArgumentParser()
    
parser.add_argument(
    "--variant",
    type=str,
    help = "base name of directory in 4_INFERENCE"
)
parser.add_argument(
    "--data-root",
    type=str,
    help = "DATA_ROOT basename"
)

args = parser.parse_args()

variant = args.variant
data_root = args.data_root

tsv_file = f"{data_root}/test.tsv"


missing_ids_dir = f"{data_root}/../5_EVALUATION/missing_ids"
cleaned_dir = f"{data_root}/../5_EVALUATION/cleaned"
os.makedirs(missing_ids_dir, exist_ok=True)
os.makedirs(cleaned_dir, exist_ok=True)

missing_ids_file = f"{missing_ids_dir}/{variant}.txt"
output_file = f"{cleaned_dir}/{variant}.tsv"

filter_tsv_by_missing_ids(tsv_file, missing_ids_file, output_file)
