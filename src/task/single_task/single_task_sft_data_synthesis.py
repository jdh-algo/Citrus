# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: single_task_sft_data_synthesis.py
@Date: 2025/01/09
remarks: 
"""
import re 
import copy
from task.single_task.single_task_base import SingleTaskBase


class SingleTaskSftDataSynthesis(SingleTaskBase):
    def __init__(self, d_st_config, d_st_input, retry_num, verbose=0):
        super().__init__(d_st_config, d_st_input, retry_num, verbose=verbose)
    
    def cal_inner(self):
        self.previous_thought = ""
        self.reasoning_step = ""
        self.early_stop_cache = []
        self.generate_GT()
        for _ in range(self.d_st_config["num_loop"]):
            # stage p1
            stage_p1_node_input = self.get_stage_p1_node_input()
            stage_p1_node_output = self.run_node('node_one_prompt_sft_data_synthesis_stage_p1', stage_p1_node_input)['prompt_res']

            # stage p2
            stage_p2_node_input = self.get_stage_p2_node_input(stage_p1_node_output)
            stage_p2_node_output = self.run_node('node_one_prompt_sft_data_synthesis_stage_p2', stage_p2_node_input)['prompt_res']

            # stage p3
            stage_p3_node_input = self.get_stage_p3_node_input(stage_p2_node_output)
            stage_p3_node_output = self.run_node('node_one_prompt_sft_data_synthesis_stage_p3', stage_p3_node_input)['prompt_res']

            # 判断
            flag_stage_p3_node_output_judgement = self.get_stage_p3_node_output_judgement(stage_p3_node_output)
            self.early_stop_cache.append(flag_stage_p3_node_output_judgement)
            if sum(self.early_stop_cache)>2:
                break

        # stage p4
        stage_p4_node_input = self.get_stage_p4_node_input(stage_p3_node_output)
        stage_p4_node_output = self.run_node('node_one_prompt_sft_data_synthesis_stage_p4', stage_p4_node_input)['prompt_res']

        
        # 拼结果
        self.d_st_output = copy.deepcopy(self.d_st_input)
        self.d_st_output['sft_data_synthesis_result'] = stage_p4_node_output
    
    def generate_GT(self):
        GT = ""
        for gt_ops in self.d_st_input['OP']:
            if gt_ops['op_idx'] == self.d_st_input['A']:
                GT = gt_ops['op_value']
                break
        self.GT = GT

    def get_stage_p1_node_input(self):
        d_prompt_kv = {'Q': self.d_st_input['Q_open']}
        return {'d_prompt_kv': d_prompt_kv} 
    
    def get_stage_p2_node_input(self, stage_p1_node_output):
        pattern = r'<Reasoning>(.*)</Reasoning>'
        matches = re.findall(pattern, stage_p1_node_output, re.DOTALL)
        if matches:
            res = matches[-1]        
        else:
            res = res.replace('<Reasoning>','').replace('</Reasoning>','')
        res =res.strip()
        
        d_prompt_kv = {
            'Q': self.d_st_input['Q_open'],
            'GT': self.GT,
            'previous_thought':self.previous_thought,
            'reasoning_step':res,
        } 
        self.reasoning_step = res
        stage_p2_node_input = {'d_prompt_kv': d_prompt_kv} 
        return stage_p2_node_input
    
    def get_stage_p3_node_input(self, stage_p2_node_output):
        d_prompt_kv = {}  
        pattern = r'<Rating>.*(0|1).*</Rating>'
        rating = 0
        matches = re.findall(pattern, stage_p2_node_output, re.DOTALL)
        if matches:
            rating = int(matches[-1])
        
        pattern_feedback = r"<Feedback>(.*)</Feedback>"
        feedback = ""
        matches_feedback = re.findall(pattern_feedback, stage_p2_node_output, re.DOTALL)
        if matches_feedback:
            feedback = matches_feedback[-1]
        else:
            feedback = stage_p2_node_output.replace('<Feedback>','').replace('</Feedback>','').replace('<Rating>','').replace('</Rating>','').replace('\n','')
        feedback = feedback.strip()
        if rating:
            self.previous_thought  = "{}\n{}\n{}\n".format(self.previous_thought, self.reasoning_step, feedback)

        d_prompt_kv['previous_thought'] = self.previous_thought
        stage_p3_node_input = {'d_prompt_kv': d_prompt_kv} 
        return stage_p3_node_input
    
    def get_stage_p3_node_output_judgement(self, stage_p3_node_output):
        pattern = r'<Rating>.*(0|1).*</Rating>'
        score = 0
        matches = re.findall(pattern, stage_p3_node_output, re.DOTALL)
        if matches:
            score = int(matches[-1])
        return score
    
    def get_stage_p4_node_input(self, stage_p3_node_output):
        d_prompt_kv = {
            'GT': self.GT,
            'raw_answer':self.previous_thought
        }
        stage_p4_node_input = {'d_prompt_kv': d_prompt_kv} 
        return stage_p4_node_input