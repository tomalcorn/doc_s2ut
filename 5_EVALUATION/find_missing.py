from natsort import natsorted
import re
import argparse

def find_missing(infile, tsv_file, outfile):
    pattern = r"D-(\d+)\t"
    
    # Read the contents of the file
    with open(infile, 'r') as file:
        lines = file.readlines()

    # Initialize an empty list to store numbers from lines starting with "D-"
    d_identifiers = []

    # Iterate through each line
    for line in lines:
        # Search for the pattern in the line
        match = re.search(pattern, line)
        if match:
            # Extract the identifier and convert it to an integer
            identifier = int(match.group(1))
            # Append the identifier to the list
            d_identifiers.append(identifier)

    # Sort the list of identifiers using natsorted
    sorted_identifiers = natsorted(d_identifiers)

    # Find the missing identifiers
    missing_identifiers = []
    for i in range(sorted_identifiers[0], sorted_identifiers[-1] + 1):
        if i not in sorted_identifiers:
            missing_identifiers.append(i)

    # Adjust missing identifiers for 1-based indexing
    missing_line_numbers = [identifier + 2 for identifier in missing_identifiers]

    # Read the TSV file and create a mapping from line numbers to ID tags
    id_tags = {}
    with open(tsv_file, 'r') as file:
        tsv_lines = file.readlines()
        for index, line in enumerate(tsv_lines, start=1):
            id_tag = line.split('\t')[0]
            id_tags[index] = id_tag

    # Look up the ID tags for the missing line numbers
    missing_id_tags = [id_tags[line_number] for line_number in missing_line_numbers if line_number in id_tags]

    # Write the missing ID tags to the output file
    with open(outfile, 'w') as out_file:
        for id_tag in missing_id_tags:
            out_file.write(f"{id_tag}\n")

# Usage example
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

infile = f"/work/tc062/tc062/s2517781/4_INFERENCE/{variant}/generate-test.txt"
tsv_file = f"/work/tc062/tc062/s2517781/{data_root}/test.tsv"
outfile = f"/work/tc062/tc062/s2517781/5_EVALUATION/missing_ids_{variant}.txt"

find_missing(infile, tsv_file, outfile)
