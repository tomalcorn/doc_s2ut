import csv

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
tsv_file = "/work/tc062/tc062/s2517781/DATA_ROOT_FISHER/test.tsv"
missing_ids_file = "/work/tc062/tc062/s2517781/5_EVALUATION/missing_ids.txt"
output_file = "/work/tc062/tc062/s2517781/5_EVALUATION/test_cleaned.tsv"

filter_tsv_by_missing_ids(tsv_file, missing_ids_file, output_file)
