import csv

def override_columns(input_file, output_file):
    # Read the input file
    with open(input_file, 'r', newline='') as infile:
        input_reader = csv.reader(infile, delimiter='\t')
        input_rows = list(input_reader)  # Read all rows from input file
    
    # Read the output file
    with open(output_file, 'r', newline='') as outfile:
        output_reader = csv.reader(outfile, delimiter='\t')
        output_rows = list(output_reader)  # Read all rows from output file

    # Ensure the input and output files have the same number of rows
    if len(input_rows) != len(output_rows):
        print("Error: The number of rows in the input and output files do not match.")
        return
    
    # Override the first and third columns of the output file
    for i in range(len(output_rows)):
        output_rows[i][0] = input_rows[i][0]  # Override the first column
        output_rows[i][2] = input_rows[i][2]  # Override the third column

    # Write the updated rows back to the output file
    with open(output_file, 'w', newline='') as outfile:
        output_writer = csv.writer(outfile, delimiter='\t')
        output_writer.writerows(output_rows)

# Replace with your actual file paths
input_file = '/work/tc062/tc062/s2517781/5_EVALUATION/text_out/ep_base.tsv'
output_file = '/work/tc062/tc062/s2517781/5_EVALUATION/text_out/ep_sent_integrated.tsv'

override_columns(input_file, output_file)
