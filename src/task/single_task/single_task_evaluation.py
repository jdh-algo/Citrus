# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: single_task_evaluation.py
@Date: 2025/01/09
remarks: 
"""
import re 
import copy
from task.single_task.single_task_base import SingleTaskBase


class SingleTaskEvaluation(SingleTaskBase):
    def __init__(self, d_st_config, d_st_input, retry_num, verbose=0):
        super().__init__(d_st_config, d_st_input, retry_num, verbose=verbose)
    
    def cal_inner(self):
        d_prompt_kv = {'Q': self.d_st_input['Q'], 'OPS': '\n'.join([e['op_text'] for e in self.d_st_input['OP']])}
        model = self.d_st_input['model_eval']

        if 'citrus' in model:
            d_node_output_citrus = self.run_node('node_one_prompt_citrus_pro', {'d_prompt_kv': d_prompt_kv, 'model': model} )
            rawA = d_node_output_citrus['prompt_res']

        else:
            d_node_output_other_model = self.run_node('node_one_prompt_llm_model', {'d_prompt_kv': d_prompt_kv, 'model': model} )
            rawA = d_node_output_other_model['prompt_res']
        
        answer = SingleTaskEvaluation.extract_answer(rawA)
        
        if len(answer) > 3:
            d_prompt_kv_answer_check = {'rawA': answer, 'ops': '\n'.join([e['op_text'] for e in self.d_st_input['OP']])}
            d_node_output_answer_check = self.run_node('node_one_prompt_answer_check', {'d_prompt_kv': d_prompt_kv_answer_check} )
            answer = d_node_output_answer_check['prompt_res']
        
        # 拼答案
        self.d_st_output = copy.deepcopy(self.d_st_input)
        self.d_st_output['raw_answer'] = rawA
        self.d_st_output['final_answer'] = answer
        self.d_st_output['is_corrrect'] = answer == self.d_st_input['A']

    
    @staticmethod
    def extract_answer(raw_answer):
        pattern = r'<answer>(.*?)</answer>'
        try:
            match = re.findall(pattern, raw_answer, re.DOTALL)[-1]
        except:
            match = raw_answer
        return match.strip()