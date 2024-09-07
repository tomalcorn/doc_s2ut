import os

def list_files(folder):
    """Return a set of filenames in the given folder."""
    fileset =set()
    for filename in os.listdir(folder):
        if filename[-4:] == ".wav" and filename[-8:-4] == '.mp3':
            name = filename[:-8] + '.wav'
        else:
            name = filename
        fileset.add(name)
    return fileset

def compare_folders(folder1, folder2, results_file):
    """Compare filenames in two folders and write the results to a text file."""
    # Get the sets of filenames for each folder
    files_in_folder1 = list_files(folder1)
    files_in_folder2 = list_files(folder2)
    
    # Find the differences
    only_in_folder1 = files_in_folder1 - files_in_folder2
    only_in_folder2 = files_in_folder2 - files_in_folder1
    
    # Write the results to a file
    with open(results_file, 'w') as file:
        file.write(f"Files in {folder1} not in {folder2}:\n")
        for filename in sorted(only_in_folder1):
            file.write(filename + "\n")
        
        file.write(f"\nFiles in {folder2} not in {folder1}:\n")
        for filename in sorted(only_in_folder2):
            file.write(filename + "\n")
    
    print(f"Comparison complete. Results written to {results_file}")

# Set the folder paths and the results file path
folder1 = "data/cvss_c_es_en_v1.0/train"
folder2 = "data/es/train"
results_file = "./mismatch_train.txt"

# Run the comparison
compare_folders(folder1, folder2, results_file)
