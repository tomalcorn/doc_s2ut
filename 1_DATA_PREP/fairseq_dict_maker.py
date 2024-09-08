import multitask_dict_maker
import task_dict
from fairseq.data import dictionary as dic
import os
import argparse

def main():
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--data-root", type=str)
    parser.add_argument("--manifest-dir", type=str)
    parser.add_argument("--task-dict", type=str)
    parser.add_argument("--splits", type=str)
    
    args = parser.parse_args()
    
    data_root = args.data_root
    tasks = eval(args.task_dict)
    splits = args.splits.split(',')
    manifest_dir = args.manifest_dir


    for task in tasks:
        for split in splits:
            location = tasks[task][:3].lower()
            # print(location)
            in_wavs = "./" + tasks[task] + split
            in_tsv = f'{manifest_dir}{location}_{split}.tsv'
            output_folder = f'{data_root}{task}/'
            task_dict.task_dic_maker(task, in_wavs, in_tsv, split, output_folder)

    for task in tasks:
        root = f'{data_root}/{task}/'
        save_file = root + 'dict.txt'
        input_file = multitask_dict_maker.main(task, data_root)
        task_dic = dic.Dictionary()
        loaded_dict = task_dic.load(input_file)
        loaded_dict.save(save_file)
        # Remove any existing dict_tmp.txt file
        dict_tmp_file = os.path.join(root, 'dict_tmp.txt')
        if os.path.exists(dict_tmp_file):
            os.remove(dict_tmp_file)
        
        

if __name__ == "__main__":
    main()        
