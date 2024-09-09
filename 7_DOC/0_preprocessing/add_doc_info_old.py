import pandas as pd

# Define file paths
split = "test"

input_file = f"/Users/tomalcorn/Documents/University/pg/diss/DATA_ROOT_DOC/{split}_pre_concat.tsv"
output_file = f"/Users/tomalcorn/Documents/University/pg/diss/DATA_ROOT_SENT/{split}.tsv"
prefix = 'common_voice_es_'
doc_context_size = 0

# Load the TSV file into a DataFrame, including the header
df = pd.read_csv(input_file, sep='\t')

def change_src_tgt_frames(row, df, doc_context_size):
    total_source_frames = row['src_n_frames']
    total_target_frames = row['tgt_n_frames']
    doc_id = row['doc_id']
    doc_pos_idx = row['doc_pos_idx']
    
    prev_doc_pos_idx = doc_pos_idx - 1
    contexts_catted = 0
    
    while contexts_catted < doc_context_size and prev_doc_pos_idx >= 0:
        prev_row = df[(df['doc_id'] == doc_id) & (df['doc_pos_idx'] == prev_doc_pos_idx)]
        
        if not prev_row.empty:
            total_source_frames += prev_row.iloc[0]['src_n_frames']
            total_target_frames += prev_row.iloc[0]['tgt_n_frames']
            contexts_catted += 1
        
        prev_doc_pos_idx -= 1
    
    return total_source_frames, total_target_frames

def extract_info(file_id):
    doc_id = file_id[len(prefix):len(prefix)+5]
    doc_pos_idx = int(file_id[len(prefix)+5:])
    return doc_id, doc_pos_idx

# Ensure that the 'id' column is present
if 'id' not in df.columns:
    raise ValueError("The input file must contain an 'id' column.")

# Extract `doc_id` (first 5 digits) and `doc_pos_idx` (remaining digits) from the 'id' column
df[['doc_id', 'numeric_part']] = df.apply(lambda row: pd.Series(extract_info(row['id'])), axis=1)

# Sort the DataFrame by doc_id and numeric part
df = df.sort_values(by=['doc_id', 'numeric_part']).reset_index(drop=True)

# Assign ordered index to doc_pos_idx within each doc_id group
df['doc_pos_idx'] = df.groupby('doc_id').cumcount()

df = df.drop(columns=['numeric_part'])

# Change the number of source and target frames to concat of prev doc_context_size segments
df[['src_n_frames', 'tgt_n_frames']] = df.apply(lambda row: pd.Series(change_src_tgt_frames(row, df, doc_context_size)), axis=1)

# Save the DataFrame with the new columns to a new TSV file
df.to_csv(output_file, sep='\t', index=False)

print(f"Processing completed. Output written to {output_file}")
