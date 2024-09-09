import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

def create_attention_heatmaps(attn_dir, source_mask_dir, target_mask_dir, output_dir):
    # Get all numpy files in the attention folder
    attn_files = [f for f in os.listdir(attn_dir) if f.endswith('.npy')]
    
    for np_file in tqdm(attn_files, desc="Creating heatmaps"):
        # Load attention scores
        attention_scores = np.load(os.path.join(attn_dir, np_file))
        
        # Load source and target masks
        source_mask = np.load(os.path.join(source_mask_dir, np_file.replace('attention_scores_', 'src_mask_')))
        target_mask = np.load(os.path.join(target_mask_dir, np_file.replace('attention_scores_', 'tgt_mask_')))
        
        # Remove padding from source mask
        last_non_zero_source = np.where(source_mask != 0)[0][-1]
        source_mask = source_mask[:last_non_zero_source + 1]
        
        
        # Adjust attention scores
        attention_scores = attention_scores[:last_non_zero_source + 1, :]
        
        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Create heatmap
        sns.heatmap(attention_scores.T, ax=ax, cmap='viridis')  # Transpose for correct orientation
        ax.invert_yaxis()
        
        # Find boundaries in the masks
        source_boundaries = np.where(np.diff(source_mask))[0]
        target_boundaries = np.where(np.diff(target_mask))[0]
        
        # Draw lines for source boundaries
        for boundary in source_boundaries:
            ax.axvline(x=boundary + 0.5, color='red', linestyle='--')
        
        # Draw lines for target boundaries
        for boundary in target_boundaries:
            ax.axhline(y=boundary + 0.5, color='blue', linestyle='--')
        
        # Set title and labels
        ax.set_title(f'Attention Heatmap - {np_file}')
        ax.set_ylabel('Target Tokens')
        ax.set_xlabel('Source Tokens')
        
        # Save the figure
        output_file = os.path.join(output_dir, f'{np_file[:-4]}_heatmap.png')
        plt.savefig(output_file)
        plt.close()

# Usage
root = "/Users/tomalcorn/Documents/University/pg/diss/12_DOC/3_attention/test"
attn_dir = os.path.join(root, "attn")
source_mask_dir = os.path.join(root, "src_segments")
target_mask_dir = os.path.join(root, "tgt_segments")
output_dir = os.path.join(root, "heatmaps")

for dir in [attn_dir, source_mask_dir, target_mask_dir, output_dir]:
    os.makedirs(dir, exist_ok=True)

create_attention_heatmaps(attn_dir, source_mask_dir, target_mask_dir, output_dir)