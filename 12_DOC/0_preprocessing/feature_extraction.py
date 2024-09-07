import os
import torch
import numpy as np
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import argparse
from typing import List
from fairseq.models.speech_to_text.s2t_transformer import AdaptiveFeatureSelection, S2TTransformerEncoder
from fairseq.models.speech_to_text.modules.afs_feature_extractor import AfsFeatureExtractor
from fairseq.data.audio.speech_to_speech_dataset import *
from fairseq import checkpoint_utils
from fairseq.data.audio.audio_utils import get_features_or_waveform

def collate_frames(
    frames: List[torch.Tensor], is_audio_input: bool = False
) -> torch.Tensor:
    """
    Convert a list of 2D frames into a padded 3D tensor
    Args:
    frames (list): list of 2D frames of size L[i]*f_dim. Where L[i] is
    length of i-th frame and f_dim is static dimension of features
    Returns:
    3D tensor of size len(frames)*len_max*f_dim where len_max is max of L[i]
    """
    max_len = max(frame.size(0) for frame in frames)
    if is_audio_input:
        out = frames[0].new_zeros((len(frames), max_len))
    else:
        out = frames[0].new_zeros((len(frames), max_len, frames[0].size(1)))
    for i, v in enumerate(frames):
        out[i, : v.size(0)] = v
    return out

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--feat_extractor_ckpt", type=str, required=True, help=".pt path to saved ASR-AFS model")
    parser.add_argument("--args_tsv", type=str, required=True, help="Path to tsv file with afs feat extractor args")
    parser.add_argument("--default_args_tsv", type=str, required=True, help="path to default args tsv")
    parser.add_argument("--audio_dir", type=str, required=True, help="path to audio dir")
    parser.add_argument('--output_dir', type=str, required=True, help="path to output dir for npy files")
    parser.add_argument('--input_tsv', type=str, required=True, help="path to input tsv file")
    parser.add_argument('--output_tsv', type=str, required=True, help="path to output tsv file")
    args = parser.parse_args()

    model = AfsFeatureExtractor(
        pretraining_path=args.feat_extractor_ckpt,
        args_tsv=args.args_tsv,
        default_args=args.default_args_tsv,
        need_l0_mask=True
    )

    # Directory containing audio files
    input_dir = Path(args.audio_dir)
    # Directory to save features
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    # Directory to save input lengths
    input_length_dir = output_dir.parent / f"{output_dir.name}_input_lengths"
    input_length_dir.mkdir(parents=True, exist_ok=True)
    # Directory to save l0_masks
    l0_mask_dir = output_dir.parent / f"{output_dir.name}_l0_masks"
    l0_mask_dir.mkdir(parents=True, exist_ok=True)

    # Read input TSV file
    df = pd.read_csv(args.input_tsv, sep='\t')

    # Process audio files individually
    # Process audio files individually
    for index, row in tqdm(df.iterrows(), total=len(df)):
        audio_file = Path(row['src_audio'])
        
        # Load audio
        source = torch.from_numpy(get_features_or_waveform(str(audio_file)))
        src_tokens = collate_frames([source], is_audio_input=False)
        src_lengths = torch.tensor([source.size(0)], dtype=torch.long)

        # Extract features
        with torch.no_grad():
            features, input_lengths, l0_masks = model.forward(src_tokens, src_lengths)

        
        features = features.squeeze(1)
        l0_masks = l0_masks.squeeze(1)
        
        # Save features and input lengths
        output_file = output_dir / f"{audio_file.stem}.npy"
        input_lengths_file = input_length_dir / f"{audio_file.stem}.npy"
        l0_masks_file = l0_mask_dir / f"{audio_file.stem}.npy"
        np.save(output_file, features.cpu().numpy())
        np.save(input_lengths_file, input_lengths.cpu().numpy())
        np.save(l0_masks_file, l0_masks.cpu().numpy())

        # Update TSV data
        df.at[index, 'src_audio'] = str(output_file)  # Update the audio path
        df.at[index, 'src_n_frames'] = features.size(0)  # Update src_n_frames to be the seq_length of extracted features

    # Save updated TSV
    df.to_csv(args.output_tsv, sep='\t', index=False)

if __name__ == '__main__':
    main()
    
    
