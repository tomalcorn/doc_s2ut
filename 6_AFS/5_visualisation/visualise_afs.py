import numpy as np
import matplotlib.pyplot as plt
import wave
from pathlib import Path
from scipy.interpolate import interp1d
import scipy.signal
from tqdm import tqdm
import os

def visualize_waveform_and_spectrogram(audio_file, mask_file, output_file, plot_spectrogram):
    num_plots = 1
    if plot_spectrogram:
        num_plots = 2
    
    # Load the audio file
    with wave.open(audio_file, 'r') as spf:
        sample_rate = spf.getframerate()
        n_frames = spf.getnframes()
        signal = np.frombuffer(spf.readframes(n_frames), dtype=np.int16)
    
    # Calculate the length of the audio in seconds
    audio_length_seconds = n_frames / sample_rate
    
    # Load L0 mask and squeeze it to 1D
    l0_mask = np.load(mask_file).flatten()
    # print(f"Original l0_mask shape: {l0_mask.shape}")
    
    # Get lengths
    mask_length = len(l0_mask)
    # print(f"mask_length: {mask_length}")
    
    # Create an interpolation function to resample the mask
    x = np.linspace(0, mask_length - 1, mask_length)
    # print(f"x shape: {x.shape}")
    # print(f"l0_mask shape: {l0_mask.shape}")
    
    interpolator = interp1d(x, l0_mask, kind='linear', fill_value="extrapolate")
    
    # Create new x values for the audio length
    new_x = np.linspace(0, mask_length - 1, len(signal))
    scaled_mask = interpolator(new_x)
    
    # Create time array for the audio
    time = np.linspace(0, audio_length_seconds, num=len(signal))
    
    # Create the plot
    if plot_spectrogram:
        fig, (ax1, ax2) = plt.subplots(num_plots, 1, figsize=(15, 8), sharex=True)
    else:
        fig, ax1 = plt.subplots(num_plots, 1, figsize=(15, 6), sharex=True)
    # Plot waveform
    ax1.plot(time, signal, color='blue', alpha=0.5, label='Waveform')
    
    
    # Plot scaled mask
    mask_time = np.linspace(0, audio_length_seconds, num=len(scaled_mask))
    ax1.fill_between(mask_time, -np.max(signal), np.max(signal), where=scaled_mask > 0, color='red', alpha=0.7, label='Selected Features')
    # ax1.fill_between(mask_time, -np.max(signal), np.max(signal), where=(0.7 < scaled_mask) & (scaled_mask < 1), color='red', alpha=0.7, label='Partial Mask')
    # ax1.fill_between(mask_time, -np.max(signal), np.max(signal), where=(0.5 < scaled_mask) & (scaled_mask < 0.7), color='red', alpha=0.5, label='Partial Mask')
    # ax1.fill_between(mask_time, -np.max(signal), np.max(signal), where=(0.3 < scaled_mask) & (scaled_mask < 0.5), color='red', alpha=0.3, label='Partial Mask')
    # ax1.fill_between(mask_time, -np.max(signal), np.max(signal), where=(0.0 < scaled_mask) & (scaled_mask <= 0.5), color='red', alpha=0.1, label='Light Mask')
    
    # Set labels and title for the waveform
    ax1.set_ylabel('Amplitude (dB)')
    ax1.set_xlabel('Time (s)')
    ax1.set_title(f'Features selected by AFS with $\lambda$ = 0.8')
    ax1.legend(loc='upper right')
    
    if plot_spectrogram:
        ax2.specgram(signal, NFFT=1024, Fs=sample_rate, noverlap=900)
        ax2.fill_between(mask_time, -np.max(signal), np.max(signal), where=scaled_mask != 0, color='red', alpha=0.7, label='Selected features')
        ax2.fill_between(mask_time, -np.max(signal), np.max(signal), where=(0.7 < scaled_mask) & (scaled_mask < 1), color='red', alpha=0.7, label='Partial Mask')
        ax2.fill_between(mask_time, -np.max(signal), np.max(signal), where=(0.5 < scaled_mask) & (scaled_mask < 0.7), color='red', alpha=0.5, label='Partial Mask')
        ax2.fill_between(mask_time, -np.max(signal), np.max(signal), where=(0.3 < scaled_mask) & (scaled_mask < 0.5), color='red', alpha=0.3, label='Partial Mask')
        ax2.fill_between(mask_time, -np.max(signal), np.max(signal), where=(0.0 < scaled_mask) & (scaled_mask <= 0.5), color='red', alpha=0.1, label='Light Mask')
    # Save the plot
    fig.tight_layout(rect=[0,0.1,1,1]) 
    plt.savefig(output_file, dpi=300)
    plt.close()

def main():
    plot_spectrogram = False
    audio_dir = Path("/work/tc062/tc062/s2517781/SRC_AUDIO_EP/train")
    mask_dir = Path("/work/tc062/tc062/s2517781/7_AFS/5_visualisation/sent_integrated_test_0.8/l0_masks")
    output_dir = Path("/work/tc062/tc062/s2517781/7_AFS/5_visualisation/sent_integrated_test_0.8/graphs")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    total_lines = len(os.listdir(audio_dir))

    for audio_file in tqdm(audio_dir.glob('*.wav'), desc="visualising files", total=total_lines):
        mask_file = mask_dir / f"{audio_file.stem}.npy"
        if mask_file.exists():
            output_file = output_dir / f"{audio_file.stem}_visualization.png"
            visualize_waveform_and_spectrogram(str(audio_file), str(mask_file), str(output_file), plot_spectrogram)
            # print(f"Processed: {audio_file.name}")
        else:
            print(f"Mask file not found for: {audio_file.name}")

if __name__ == "__main__":
    main()