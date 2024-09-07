import pandas as pd
import matplotlib.pyplot as plt

def plot_loss(tsv_files, names, columns, box_x, box_y, save_path):
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for tsv_file, name in zip(tsv_files, names):
        # Read the TSV file into a DataFrame
        df = pd.read_csv(tsv_file, sep='\t')
        # Extract unique splits
        splits = df['split'].unique()
        
        # Plotting each split and column separately
        for split in splits:
            data = df[df['split'] == split]
            for column in columns.keys():
                if split in columns[column]:
                    line, =ax.plot(data['epoch'], data[column], label=f"{name}_{split}_{column}")
                    line_colour = line.get_color()
            # Mark the point with the lowest dev loss for each column
            if split == 'dev':
                for column in columns.keys():
                    if 'min' in columns[column]:
                        min_loss = data[column].min()
                        min_epoch = data.loc[data[column].idxmin(), 'epoch']
                        ax.axvline(x=min_epoch, color=line_colour, linestyle='--', linewidth=0.8)
                        
                        # Annotation box position
                        if 'box' in columns[column]:
                            xytext = (min_epoch + box_x, min_loss + box_y)
                            ax.annotate(f'Min Dev {name} {column}\n{min_loss:.2f}',
                                        xy=(min_epoch, min_loss), xytext=xytext,
                                        bbox=dict(boxstyle='round,pad=0.5', edgecolor='black', facecolor='white'))
    
    ax.set_xlabel('Epoch')
    ax.set_ylabel(', '.join(columns))
    ax.set_title(f'{", ".join(columns)} over Epochs for {", ".join(names)}')
    ax.legend(loc='upper right')
    ax.grid(True)
    
    plt.tight_layout()
    # Show plot
    if save_path:
        plt.savefig(save_path, dpi=500)
    else:
        plt.show()

if __name__ == "__main__":
    tsv_file_root = "/Users/tomalcorn/Documents/University/pg/diss/3_LOGGING/logs/doc_"
    
    # Define your parameters here
    variants = ['0.2_ctxt_2', '0.2_extended', '0.2', '1_extended', 'ep_base', 'ep_doc_full_0.005', 'ep_doc_integrated',]
    # column: [any of [{split}, 'box']]
    columns = {"loss": ['dev', 'min', 'box']}  # Add or remove columns as needed
    
    tsv_files = [f"{tsv_file_root}{name}_loss.tsv" for name in variants]
    box_x = -65
    box_y = 10

    save_path = ""

    # Ensure the number of names matches the number of TSV files
    if len(tsv_files) != len(variants):
        raise ValueError("The number of TSV files must match the number of names provided")
    
    # Call the plot function with the provided arguments
    plot_loss(tsv_files, variants, columns, box_x, box_y, save_path)