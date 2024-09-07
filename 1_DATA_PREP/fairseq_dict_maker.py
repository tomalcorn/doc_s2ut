import multitask_dict_maker
import task_dict
from fairseq.data import dictionary as dic
import os

global_root = '/Users/tomalcorn/Documents/University/pg/diss/'
data_root = global_root + 'DATA_ROOT_EP/'
tasks = {'decoder_target_ctc':'TGT_AUDIO_EP/', 'source_letter':'SRC_AUDIO_EP/', 'target_letter':'TGT_AUDIO_EP/'}
splits = ['train', 'dev', 'test']


for task in tasks:
    for split in splits:
        location = tasks[task][:3].lower()
        # print(location)
        in_wavs = global_root + tasks[task] + split
        in_tsv = f'{data_root}{location}_{split}.tsv'
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
    
    

    
