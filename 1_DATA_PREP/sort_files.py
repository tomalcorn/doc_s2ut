import os

def sort_files(directory, sort_by='name'):
    # Get a list of all files in the directory
    files = os.listdir(directory)
    
    # Filter out directories, only keep files
    files = [f for f in files if os.path.isfile(os.path.join(directory, f))]
    
    if sort_by == 'name':
        # Sort files by name
        sorted_files = sorted(files)
    elif sort_by == 'mtime':
        # Sort files by modification time
        sorted_files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(directory, x)))
    elif sort_by == 'size':
        # Sort files by size
        sorted_files = sorted(files, key=lambda x: os.path.getsize(os.path.join(directory, x)))
    else:
        raise ValueError("Invalid sort_by value. Choose from 'name', 'mtime', 'size'.")
    
    return sorted_files

# Set the directory path
directory = 'TGT_AUDIO/train'

# Sort files by name, modification time (mtime), or size
sorted_files_by_name = sort_files(directory, sort_by='name')
sorted_files_by_mtime = sort_files(directory, sort_by='mtime')
sorted_files_by_size = sort_files(directory, sort_by='size')

# Print sorted file lists
print("Files sorted by name:")
for f in sorted_files_by_name:
    print(f)

print("\nFiles sorted by modification time:")
for f in sorted_files_by_mtime:
    print(f)

print("\nFiles sorted by size:")
for f in sorted_files_by_size:
    print(f)
