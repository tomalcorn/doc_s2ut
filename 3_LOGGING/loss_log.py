import os

# Input log file
task = "doc"
variants = ['afs_slurm', 'cv_afs', 'cv_feats', 'cv_feats_2']
variants = ['0.2_ctxt_2', '0.2_extended', '0.2', '1_extended', 'ep_base', 'ep_doc_0.001', 'ep_doc_full_0.005', 'ep_doc_integrated', 'ep_doc_wav_test', 'ep_doc_wav_test_curr']

for variant in variants:
    input_log_file = f"/Users/tomalcorn/Documents/University/pg/diss/{task}/{variant}.txt"


    log_dir = '/Users/tomalcorn/Documents/University/pg/diss/3_LOGGING/logs'
    # Create logs directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)

    # Output TSV file
    output_tsv_file = log_dir + f"/{task}_{variant}_loss.tsv"

    # TSV header

    if 'afs' in task:
        header = "Datetime\tsplit\tepoch\tloss\tnll_loss\tl0_reg\tppl\twps\tups\twpb\tbsz\tnum_updates\tlr\tgnorm\tclip\tloss_scale\ttrain_wall\tgb_free\twall\tnum_updates\tbest_loss"
    else:
        header = "Datetime\tsplit\tepoch\tloss\tnll_loss\tmultitask_source_letter_loss\tmultitask_target_letter_loss\tmultitask_decoder_target_ctc_loss\tppl\twps\tups\twpb\tbsz\tnum_updates\tmultitask_source_letter_loss_weight\tmultitask_target_letter_loss_weight\tmultitask_decoder_target_ctc_loss_weight\tlr\tgnorm\tclip\tloss_scale\ttrain_wall\tgb_free\twall\tnum_updates\tbest_loss"
    # afs finetune header

    # Function to process a line and convert it to the TSV format
    def process_line(line):
        parts = line.strip().split(" | ")
        if len(parts) >= 6:
            # Remove the second column (INFO)
            processed_parts = [parts[0]] + parts[2:]
            
            # Check if it's a dev line
            if "| INFO | dev |" in line or "| INFO | dev2 |" in line:
                # Remove the 5th column and handle 'best loss'
                processed_parts = processed_parts[:3] + processed_parts[4:]
            
            # Replace header text in column entries if present
            for i, word in enumerate(header.split("\t")):
                if i < 2:
                    pass
                elif i < len(processed_parts) and word in processed_parts[i]:
                    processed_parts[i] = processed_parts[i].replace(f"{word} ", "")
                else:
                    processed_parts.insert(i, 'NA')
            
            # Join parts with tab
            return "\t".join(processed_parts)
        return None

    # Read the input log file and write to the output TSV file
    with open(input_log_file, "r") as infile, open(output_tsv_file, "w") as outfile:
        # Write the TSV header
        outfile.write(header + "\n")
        
        # Process lines and write them to the TSV file
        for line in infile:
            if "| INFO | train |" in line or "| INFO | dev |" in line or "| INFO | dev2 |" in line:
                processed_line = process_line(line)
                if processed_line:
                    outfile.write(processed_line + "\n")

    print(f"Lines containing '| INFO | train |' and '| INFO | dev |'  and maybe '| INFO | dev2 |' have been written to {output_tsv_file}")
