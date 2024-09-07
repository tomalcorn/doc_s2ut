def find_incomplete_lines(tsv_file_path):
    with open(tsv_file_path, 'r') as file:
        lines = file.readlines()
    
    incomplete_line_ids = []
    for line in lines:
        fields = line.strip().split('\t')
        if len(fields) != 3:
            incomplete_line_ids.append(fields[0] if fields else "Unknown ID")
    
    return incomplete_line_ids

# Usage
tsv_file_path = '/work/tc062/tc062/s2517781/5_EVALUATION/text_out/fisher_1.tsv'
incomplete_lines = find_incomplete_lines(tsv_file_path)
print("Lines with incomplete fields:", incomplete_lines)
