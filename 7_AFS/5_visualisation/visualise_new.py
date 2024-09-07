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

def visualize_waveform_and_spectrogram(audio_file, mask_files, text_grid_file, output_file, plot_spectrogram, fontsize_boost):
    num_plots = len(mask_files)
    
    # Load the audio file
    with wave.open(audio_file, 'r') as spf:
        sample_rate = spf.getframerate()
        n_frames = spf.getnframes()
        signal = np.frombuffer(spf.readframes(n_frames), dtype=np.int16)
    
    # Calculate the length of the audio in seconds
    audio_length_seconds = n_frames / sample_rate
    
    # Create time array for the audio
    time = np.linspace(0, audio_length_seconds, num=len(signal))
    
    # Create the plot
    fig, axes = plt.subplots(num_plots, 1, figsize=(16, 18), sharex=True)
    
    # Plot waveform
    axes[0].plot(time, signal, color='blue', alpha=0.5)
    axes[0].set_title("Features kept with $\lambda = 0.8$", fontsize=20 + fontsize_boost)
    axes[1].plot(time, signal, color='blue', alpha=0.5, label='Waveform')
    axes[1].set_title("Features kept with $\lambda = 0.3$", fontsize=20 + fontsize_boost)
    axes[2].plot(time, signal, color='blue', alpha=0.5)
    axes[2].set_title("Features kept with $\lambda = 0.1$", fontsize=20 + fontsize_boost)
    
    
    if plot_spectrogram:
        axes[0].specgram(signal, NFFT=1024, Fs=sample_rate, noverlap=900)
    
    axes[0].set_ylabel('Amplitude (dB)', fontsize=18 + fontsize_boost)
    axes[0].tick_params(axis='y', labelsize=16 + fontsize_boost)
    axes[0].set_ylim([-20000, 20000])
    axes[0].legend(loc='upper right', fontsize=16 + fontsize_boost)
    
    # Plot each mask
    for i, mask_file in enumerate(mask_files):
        l0_mask = np.load(mask_file).flatten()
        
        mask_length = len(l0_mask)
        x = np.linspace(0, mask_length - 1, mask_length)
        interpolator = interp1d(x, l0_mask, kind='linear', fill_value="extrapolate")
        
        new_x = np.linspace(0, mask_length - 1, len(signal))
        scaled_mask = interpolator(new_x)
        
        mask_time = np.linspace(0, audio_length_seconds, num=len(scaled_mask))
        
        ax_mask = axes[i]
        label = "Features kept" if i == 1 else ""
        ax_mask.fill_between(mask_time, -np.max(signal), np.max(signal), where=scaled_mask > 0, color='red', alpha=0.4, label=label)
        ax_mask.set_ylabel('Amplitude (dB)', fontsize=18 + fontsize_boost)
        ax_mask.tick_params(axis='y', labelsize=16 + fontsize_boost)
        ax_mask.set_ylim([-20000, 20000])
        ax_mask.legend(loc='upper right', fontsize=16 + fontsize_boost)
    
        # Parse the TextGrid data and plot the text annotations
        word_times = parse_textgrid(text_grid_file)
        for k in word_times.keys():
            shunt = 0.01
            start = word_times[k][0]
            end = word_times[k][1]
            word = k
            axes[i].annotate(word, (start + shunt, -18500), fontsize=12 + fontsize_boost)
            axes[i].axvline(start, color='gray', linestyle="dashed")
    
    # Set x-label only on the last subplot
    axes[-1].set_xlabel('Time (s)', fontsize=18 + fontsize_boost)
    axes[-1].tick_params(axis='x', labelsize=16 + fontsize_boost)
    
    # Save the plot
    fig.tight_layout()
    if output_file:
        plt.savefig(output_file, dpi=300)
        plt.close()
    else:
        plt.show()

def main():
    plot_spectrogram = False
    audio_dir = Path("/Users/tomalcorn/Documents/University/pg/diss/SRC_AUDIO_EP/train")
    mask_dir1 = Path("/Users/tomalcorn/Documents/University/pg/diss/7_AFS/5_visualisation/sent_integrated_test_0.8/l0_masks")
    mask_dir2 = Path("/Users/tomalcorn/Documents/University/pg/diss/7_AFS/5_visualisation/sent_integrated_test/l0_masks")
    mask_dir3 = Path("/Users/tomalcorn/Documents/University/pg/diss/7_AFS/5_visualisation/sent_integrated_test_0.1/l0_masks")
    text_grid_file = "/Users/tomalcorn/Documents/University/pg/diss/en_20101021_5_4-064_29_27_32_7.TextGrid"
    output_dir = Path("/Users/tomalcorn/Desktop")
    output_dir.mkdir(parents=True, exist_ok=True)

    audio_file_name = "en.20101021.5.4-064_29.27_32.7.wav"
    fontsize_boost = 5
    
    audio_file = audio_dir / audio_file_name
    mask_files = [
        mask_dir1 / f"{audio_file.stem}.npy",
        mask_dir2 / f"{audio_file.stem}.npy",
        mask_dir3 / f"{audio_file.stem}.npy"
    ]
    lambdas = ["0.8", "0.3", "0.1"]
    output_file = output_dir / f"three_masks.pdf"
    
    if all(mask_file.exists() for mask_file in mask_files):
        visualize_waveform_and_spectrogram(str(audio_file), [str(mask_file) for mask_file in mask_files], text_grid_file, str(output_file), plot_spectrogram, fontsize_boost)
    else:
        print(f"One or more mask files not found for: {audio_file.name}")

if __name__ == "__main__":
    main()