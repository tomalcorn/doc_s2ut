import csv
from collections import defaultdict
import argparse

def process_segments_tsv(input_tsv, output_tsv):
    # Dictionary to hold segments by speech_id
    segments = defaultdict(list)
    
    # Read the input TSV file
    with open(input_tsv, 'r') as infile:
        reader = csv.reader(infile, delimiter='\t')
        for row in reader:
            # Parse the ID to extract speech_id, start, and end
            segment_id = row[0]
            speech_id, start, end = segment_id.split('_')
            start_time = float(start)
            hypothesis = row[1]
            target_text = row[2]
            
            # Store the segments in the dictionary
            segments[speech_id].append((start_time, target_text, hypothesis))
    
    # Prepare to write the output TSV file
    with open(output_tsv, 'w', newline='') as outfile:
        writer = csv.writer(outfile, delimiter='\t')
        
        # Process each speech_id group
        for speech_id, segs in segments.items():
            # Sort segments by start time
            segs.sort(key=lambda x: x[0])
            
            # Concatenate the target_texts and hypotheses
            speech_target_text = ' '.join(seg[1] for seg in segs)
            speech_hypothesis = '. '.join(seg[2] for seg in segs)
            
            # Write the result to the output TSV file
            writer.writerow([speech_id, speech_hypothesis, speech_target_text])

# Example usage
parser = argparse.ArgumentParser()

parser.add_argument(
    "--variant",
    help= "basename for 4/INFERENCE dir"
)
parser.add_argument(
    "--data-root"
)

args = parser.parse_args()

variant = args.variant
data_root = args.data_root

input_tsv = f'{data_root}/../5_EVALUATION/text_out/{variant}.tsv'
output_tsv = f'{data_root}/..//5_EVALUATION/text_out/{variant}_speech.tsv'
process_segments_tsv(input_tsv, output_tsv)
