# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: xpo_sample_process.py
@Date: 2024/12/09
remarks: 
"""

import os
import json
from task.task_process import TaskProcess
from config.config import data_configs 
from apps.data_synthesis.utils import XpoDataCheck

class XpoSampleProcess(TaskProcess):
    def __init__(self, d_task_card):
        super().__init__(d_task_card)
        self.path_input_dir = data_configs.path_origin_w_data_label_dir
    
    def cal(self):
        self.init_path()
        for data_name in self.d_task_card['l_data']:
            self.single_data_process(data_name) 
            self.singl_data_postprcocess(data_name) 
    
    def singl_data_postprcocess(self, data_name):
        path_training_data_output = os.path.join(self.path_output_dir, '{}_training_data_output.jsonl'.format(data_name)) 
        path_task_output = os.path.join(self.path_task_tmp_dir, '{}_output.jsonl'.format(data_name))
        print(f'path_training_data_output: {path_training_data_output}')


        if not os.path.exists(path_task_output):
            print(f"[error] Output file for {data_name} does not exist.")
            return 
        
        processed_data = []
        with open(path_task_output, 'r', encoding='utf-8') as f:
            for line in f:
                d_tmp = json.loads(line) 
                processed_data.extend(XpoSampleProcess.format_xpo_data(d_tmp)) 
        

        with open(path_training_data_output, 'w', encoding='utf-8') as fw:
            for item in processed_data:
                str_tmp = json.dumps(item, ensure_ascii=False)
                fw.write(str_tmp + '\n')

    @staticmethod
    def sort_xpo_data_pair(item):
        """
        此方法用于针对构造的dpo_pair做排序, 按照优先选项不同、低分优先的原则排序
        """
        sft_ops = item['d2']['sft_ops']
        score = item['d2']['pairtwise_eval_score']
        return (sft_ops, score)

    @staticmethod
    def format_xpo_data(item):
        """
        此方法用于构造最终用于dpo训练的数据
        """
        if item.get("l_xpo_sample_result"):
            l_xpo_sample_result = sorted(item["l_xpo_sample_result"], key=lambda x:XpoSampleProcess.sort_xpo_data_pair(x)) 
        else:
            return [] 
        
        l_xpo_sample_result = l_xpo_sample_result[:3] 
        results = [] 
        for d in l_xpo_sample_result:
            question = d['d1']['sft_input'] 
            target_1 = d['d1']['sft_target'] 
            target_2 = d['d2']['sft_target'] 

            d_res = {"chosen": [{"role": "user", "content": question},{"role": "assistant", "content": target_1}], 
                "rejected": [{"role": "user", "content": question},{"role": "assistant", "content": target_2}]} 
            d_fillted = XpoSampleProcess.filter_invalid_xpo_item(d_res) 
            
            d_res = {"chosen": [{"role": "user", "content": question},{"role": "assistant", "content": target_1}], 
                "rejected": [{"role": "user", "content": question},{"role": "assistant", "content": target_2}],
                "valid_status": d_fillted["valid_status"],
                "msg": d_fillted["msg"]}
            
            results.append(d_res)
        
        return results 
    
    @staticmethod
    def filter_invalid_xpo_item(item):
        SDC = XpoDataCheck() 
        data_res, valid_status, msg = SDC.process(item) 
        valid_status = 1 if valid_status else 0
        item = data_res if data_res else item

        return dict(item=item, valid_status=valid_status, msg=msg )