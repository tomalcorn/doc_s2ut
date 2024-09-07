import numpy as np
import matplotlib.pyplot as plt
import wave
from pathlib import Path
from scipy.interpolate import interp1d
import os
from tqdm import tqdm

def parse_textgrid(text_grid_file):
    word_times = {}
    with open(text_grid_file, 'r') as f:
        lines = f.readlines()
    
    # Parse the TextGrid format
    for line in lines:
        line = line.strip()
        if line.startswith("xmin"):
            xmin = float(line.split(' = ')[1])
        elif line.startswith('xmax'):
            xmax = float(line.split(' = ')[1])
        elif line.startswith('text'):
            text = line.split(' = ')[1][1:-1]
            word_times[text] = [xmin, xmax]
    
    return word_times

def visualize_waveform_and_spectrogram(audio_file, mask_file, text_grid_file, output_file, plot_spectrogram):
    num_plots = 3
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
        fig, (ax1, ax2, ax3) = plt.subplots(num_plots, 1, figsize=(16, 6), sharex=True)
    # Plot waveform
    ax1.plot(time, signal, color='blue', alpha=0.5, label='Waveform')
    
    
    # Plot scaled mask
    mask_time = np.linspace(0, audio_length_seconds, num=len(scaled_mask))
    ax1.fill_between(mask_time, -np.max(signal), np.max(signal), where=scaled_mask > 0, color='red', alpha=0.4, label='Selected Features')
    # ax1.fill_between(mask_time, -np.max(signal), np.max(signal), where=(0.7 < scaled_mask) & (scaled_mask < 1), color='red', alpha=0.7, label='Partial Mask')
    # ax1.fill_between(mask_time, -np.max(signal), np.max(signal), where=(0.5 < scaled_mask) & (scaled_mask < 0.7), color='red', alpha=0.5, label='Partial Mask')
    # ax1.fill_between(mask_time, -np.max(signal), np.max(signal), where=(0.3 < scaled_mask) & (scaled_mask < 0.5), color='red', alpha=0.3, label='Partial Mask')
    # ax1.fill_between(mask_time, -np.max(signal), np.max(signal), where=(0.0 < scaled_mask) & (scaled_mask <= 0.5), color='red', alpha=0.1, label='Light Mask')
    
    # Set labels and title for the waveform
    ax1.set_ylabel('Amplitude (dB)', fontsize=20)
    ax1.set_xlabel('Time (s)', fontsize=20)
    ax1.tick_params(axis='y', labelsize=18)
    ax1.tick_params(axis='x', labelsize=18)
    ax1.set_ylim([-18000, 18000])
    plt.title(f'Features selected by AFS with $\lambda$ = 0.8', fontsize=22)
    ax1.legend(loc='upper right', fontsize=18)
    
    if plot_spectrogram:
        ax1.specgram(signal, NFFT=1024, Fs=sample_rate, noverlap=900)
    
    
    # Parse the TextGrid data
    word_times = parse_textgrid(text_grid_file)
    # Plot the text grid at the bottom of the figure
    for k in word_times.keys():
        shunt = 0.01
        start = word_times[k][0]
        end = word_times[k][1]
        word = k
        ax1.annotate(word, (start + shunt, -17000), fontsize=16)
        plt.axvline(start, color='gray', linestyle="dashed")
        
    
    # Save the plot
    fig.tight_layout() 
    plt.savefig(output_file, dpi=300)
    plt.close()

def main():
    plot_spectrogram = False
    audio_dir = Path("/Users/tomalcorn/Documents/University/pg/diss/SRC_AUDIO_EP/train")
    mask_dir = Path("/Users/tomalcorn/Documents/University/pg/diss/7_AFS/5_visualisation/sent_integrated_test_0.8/l0_masks")
    text_grid_file = "/Users/tomalcorn/Documents/University/pg/diss/en_20101021_5_4-064_29_27_32_7.TextGrid"
    output_dir = Path("/Users/tomalcorn/Desktop")
    output_dir.mkdir(parents=True, exist_ok=True)

    audio_file_name = "en.20101021.5.4-064_29.27_32.7.wav"
    
    audio_file = audio_dir / audio_file_name
    mask_file = mask_dir / f"{audio_file.stem}.npy"
    output_file = output_dir / f"0.8_lambda.pdf"
    
    if mask_file.exists():
        visualize_waveform_and_spectrogram(str(audio_file), str(mask_file), text_grid_file, str(output_file), plot_spectrogram)
    else:
        print(f"Mask file not found for: {audio_file.name}")

if __name__ == "__main__":
    main()
