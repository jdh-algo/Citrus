# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: task_process.py
@Date: 2024/12/09
remarks: 在task前后做一些路径处理，提供一种经典的处理方法，可以继承。适用于从data_name作为起始文件名的一些处理逻辑
"""

import os
import json
from task.task import Task

# an example of task card
'''
{
    "mode": "data_label",
    "task_name": "data label",
    "l_data": ["medqa_small", "medmcqa_small"],
    "path_input": "",
    "path_output": "",
    "stid": "single_task_data_labeling",
    "n_processor": 4,
    "n_save": 8,
    "n_retry": 3,
    "flag_force": true,
    "flag_ignore_fail": false,
    "extra_params": {}
}
'''

class TaskProcess(object):
    def __init__(self, d_task_card):
        self.d_task_card = d_task_card
        self.path_input_dir = self.d_task_card.get('path_input')
        self.path_output_dir = self.d_task_card.get('path_output')
        self.path_task_tmp_dir = None
        self.d_extra_params = self.d_task_card.get("extra_params", {})
    
    def init_path(self):
        if not os.path.exists(self.path_output_dir):
            os.mkdir(self.path_output_dir)

        self.path_task_tmp_dir = os.path.join(self.path_output_dir, '.task_tmp_dir')
        if not os.path.exists(self.path_task_tmp_dir):
            os.mkdir(self.path_task_tmp_dir)
    
    def get_path_input_output_file(self, data_name):
        path_input_file = os.path.join(self.path_input_dir, '{}.jsonl'.format(data_name))
        path_output_file = os.path.join(self.path_output_dir, '{}.jsonl'.format(data_name))
        return path_input_file, path_output_file


    def cal(self):
        self.init_path()
        for data_name in self.d_task_card['l_data']:
            self.single_data_process(data_name)
            
    
    def single_data_process(self, data_name):
        path_input_file, path_output_file = self.get_path_input_output_file(data_name)
        path_task_input = os.path.join(self.path_task_tmp_dir, '{}_input.jsonl'.format(data_name))
        path_task_output = os.path.join(self.path_task_tmp_dir, '{}_output.jsonl'.format(data_name))

        if not self.d_task_card.get('flag_force') and os.path.exists(path_output_file):
            return
        
        flag_error = False
        with open(path_input_file) as f, open(path_task_input, 'w') as fw:
            for line in f.readlines():
                d_tmp = json.loads(line)
                d_tmp['line_id'] = d_tmp['id']
                for k, v in self.d_extra_params.items():
                    if k in d_tmp:
                        print('[error] extra params key {} has already in input json, please check!')
                        flag_error = True
                        break
                    d_tmp[k] = v
                str_tmp = json.dumps(d_tmp, ensure_ascii=False)
                fw.write(str_tmp)
                fw.write('\n')
        if flag_error:
            return
        
        if self.d_task_card.get('flag_force') and os.path.exists(path_task_output):
            os.remove(path_task_output)

        d_task_card = {
            "task_name": '{} {}'.format(data_name, self.d_task_card.get("task_name", "")),
            "path_task_input": path_task_input,
            "path_task_output": path_task_output,
            "stid": self.d_task_card["stid"],
            "n_processor": self.d_task_card["n_processor"],
            "n_save": self.d_task_card["n_save"],
            "n_retry": self.d_task_card["n_retry"],
            "flag_force": self.d_task_card["flag_force"],
            "verbose": self.d_task_card.get("verbose")
        }

        task = Task(d_task_card)
        task.cal()

        n_fail = 0
        # with open(path_task_output) as f, open(path_origin_w_qopen_file, 'w') as fw:
        with open(path_task_output) as f:
            for line in f.readlines():
                d_tmp = json.loads(line)
                if d_tmp['line_status'] != 'success':
                    n_fail += 1
        if not self.d_task_card["flag_ignore_fail"] and n_fail > 0:
            print('[error] task {} has {} failed, please check!'.format(
                d_task_card["task_name"], n_fail
            ))
        else:
            with open(path_task_output) as f, open(path_output_file, 'w') as fw:
                for line in f.readlines():
                    d_tmp = json.loads(line)
                    del d_tmp['line_status']
                    del d_tmp['line_id']
                    for k, v in self.d_extra_params.items():
                        del d_tmp[k]
                    str_tmp = json.dumps(d_tmp, ensure_ascii=False)
                    fw.write(str_tmp)
                    fw.write('\n')



