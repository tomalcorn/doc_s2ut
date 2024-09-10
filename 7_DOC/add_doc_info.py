import pandas as pd
import os
import argparse

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
    parts = file_id.split('_')
    doc_id = parts[0]
    start_time = parts[1]
    return doc_id, start_time

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", type=str, required=True)
    parser.add_argument("--data-root", type=str, required=True)
    parser.add_argument("--doc-context-size", type=int, default=1)
    
    args = parser.parse_args()
    
    split = args.split
    input_data_root = args.data_root
    input_file = f"{input_data_root}/{split}.tsv"
    doc_context_size = args.doc_context_size
    
    # Load the TSV file into a DataFrame, including the header
    df = pd.read_csv(input_file, sep='\t')    

    # Ensure that the 'id' column is present
    if 'id' not in df.columns:
        raise ValueError("The input file must contain an 'id' column.")

    # Extract `doc_id` and `numeric_part` from the 'id' column
    df[['doc_id', 'numeric_part']] = df.apply(lambda row: pd.Series(extract_info(row['id'])), axis=1)

    # Sort the DataFrame by doc_id and numeric part
    df = df.sort_values(by=['doc_id', 'numeric_part']).reset_index(drop=True)

    # Assign ordered index to doc_pos_idx within each doc_id group
    df['doc_pos_idx'] = df.groupby('doc_id').cumcount()

    df = df.drop(columns=['numeric_part'])

    # Change the number of source and target frames to concat of prev doc_context_size segments
    df[['src_n_frames', 'tgt_n_frames']] = df.apply(lambda row: pd.Series(change_src_tgt_frames(row, df, doc_context_size)), axis=1)

    # Overwrite the input file with the modified DataFrame
    df.to_csv(input_file, sep='\t', index=False)

    print(f"Processing completed. The input file {input_file} has been modified in place.")

if __name__ == "__main__":
    main()