# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: single_task_data_labeling.py
@Date: 2025/01/09
remarks: 
"""
import re 
import copy
from task.single_task.single_task_base import SingleTaskBase


class SingleTaskDataLabeling(SingleTaskBase):
    def __init__(self, d_st_config, d_st_input, retry_num, verbose=0):
        super().__init__(d_st_config, d_st_input, retry_num, verbose=verbose)
    
    def cal_inner(self):
        # 改写成开放问题
        d_prompt_kv = {'Q': self.d_st_input['Q']}
        d_node_output_q_open = self.run_node('node_one_prompt_rewrite_q_open', {'d_prompt_kv': d_prompt_kv} )

        # 判断题目难度
        d_prompt_kv = {'question': self.d_st_input['Q'], 'options': '\n'.join([e['op_text'] for e in self.d_st_input['OP']])}
        d_node_output_strong_model = self.run_node('node_one_prompt_answer_exam_strong_model', {'d_prompt_kv': d_prompt_kv} )
        answer_strong_model = d_node_output_strong_model['prompt_res']

        d_node_output_weak_model = self.run_node('node_one_prompt_answer_exam_weak_model', {'d_prompt_kv': d_prompt_kv} )
        answer_weak_model = d_node_output_weak_model['prompt_res']
        complexity = self.get_comlexity_label(answer_strong_model,  answer_weak_model, self.d_st_input)

        # 拼答案
        self.d_st_output = copy.deepcopy(self.d_st_input)
        self.d_st_output['Q_open'] = d_node_output_q_open['prompt_res']
        self.d_st_output['complexity'] = complexity


    def get_comlexity_label(self, answer_strong_model,  answer_weak_model, d_st_input):
        gt_ops = d_st_input['A'] 
        strong_ops = SingleTaskDataLabeling.parse_question_result(answer_strong_model)['model_ops']
        weak_ops = SingleTaskDataLabeling.parse_question_result(answer_weak_model)['model_ops']
        comlexity_label = 'easy'
        
        if weak_ops!=gt_ops:
            comlexity_label = 'hard'
        elif strong_ops!=gt_ops and weak_ops==gt_ops:
            comlexity_label = 'unknown'
        else:
            comlexity_label = 'easy'
        return comlexity_label
    
    @staticmethod
    def parse_question_result(llm_res):
        thoughts = ""
        model_ops = 0
        pattern = r'<Thoughts>(.*)</Thoughts>'
        matches = re.findall(pattern, str(llm_res), re.DOTALL)
        if matches:
            thoughts = str(matches[-1]).strip()
        
        pattern = r'<Answer>(.*)</Answer>'
        matches = re.findall(pattern, str(llm_res), re.DOTALL)
        model_ops = []
        if matches:
            for ops in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H','-1']:
                if ops in matches[-1]:
                    model_ops.append(ops)
        model_ops = ";".join(sorted(model_ops))
        return dict(thoughts=thoughts, model_ops=model_ops) 
        

