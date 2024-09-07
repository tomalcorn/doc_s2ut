import os
import shutil

def move_files_from_txt(input_folder1, input_folder2, output_folder1, output_folder2, txt_file):
    # Read the filenames from the text file
    with open(txt_file, 'r') as file:
        filenames = [line.strip() for line in file.readlines()]
    
    # Create the output folders if they don't exist
    os.makedirs(output_folder1, exist_ok=True)
    os.makedirs(output_folder2, exist_ok=True)
    
    # Loop through the filenames and move matching files
    for filename in filenames:
        input_file_path1 = os.path.join(input_folder1, filename)
        input_file_path2 = os.path.join(input_folder2, filename)
        
        if os.path.exists(input_file_path1) and os.path.exists(input_file_path2):
            shutil.move(input_file_path1, output_folder1)
            shutil.move(input_file_path2, output_folder2)
            print(f"{filename} moved.")
        else:
            print(f"File {filename} does not exist in one or both input folders and was skipped.")

# Set the input and output folder paths and the path to the text file
input_folder1 = "/work/tc062/tc062/s2517781/mine/data/es/clipsslim"
input_folder2 = "/work/tc062/tc062/s2517781/mine/data/en/clipsslim"
output_folder1 = "/work/tc062/tc062/s2517781/SRC_AUDIO/test"
output_folder2 = "/work/tc062/tc062/s2517781/TGT_AUDIO/test"
txt_file = "/work/tc062/tc062/s2517781/mine/data/en/testing.txt"

# Run the file moving function
move_files_from_txt(input_folder1, input_folder2, output_folder1, output_folder2, txt_file)
