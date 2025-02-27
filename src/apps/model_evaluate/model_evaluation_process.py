# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: model_evaluation_pipeline.py
@Date: 2024/12/09
remarks: Model inference + evaluation
"""

import os
import json
from task.task_process import TaskProcess
from config.config import data_configs

class ModelEvaluationProcess(TaskProcess):
    def __init__(self, d_task_card):
        super().__init__(d_task_card)
        self.model_eval = self.d_task_card["extra_params"]["model_eval"]
        self.path_input_dir = data_configs.path_origin_dir
        self.path_output_dir = os.path.join(data_configs.path_evaluation_dir, self.model_eval)
        self.path_summary = os.path.join(self.path_output_dir, 'summary.json')
    
    def cal(self):
        self.init_path()
        for data_name in self.d_task_card['l_data']:
            self.single_data_process(data_name)
        self.summary()
    
    def summary(self):
        d_summary = {}
        if os.path.exists(self.path_summary):
            with open(self.path_summary) as f:
                d_summary = json.load(f)

        for data_name in self.d_task_card['l_data']:
            _, path_output_file = self.get_path_input_output_file(data_name)

            n_true, n_false, n_no_answer = 0, 0, 0
            n_total = 0
            with open(path_output_file) as f:
                for line in f.readlines():
                    n_total += 1
                    d_tmp = json.loads(line)
                    if 'is_corrrect' in d_tmp:
                        if d_tmp['is_corrrect']:
                            n_true += 1
                        else:
                            n_false += 1
                    else:
                        n_no_answer += 1
            
            d_res = {
                "acc": round(n_true/n_total, 8),
                "valid_acc": round(n_true/(n_true + n_false), 8),
                "num": {
                    "true": n_true,
                    "false": n_false,
                    "no_answer": n_no_answer
                }
            }
            d_summary[data_name] = d_res
        
            with open(self.path_summary, 'w') as fw:
                json.dump(d_summary, fw, indent=2)



