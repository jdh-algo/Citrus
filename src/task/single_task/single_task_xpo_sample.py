# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: single_task_xpo_sample.py
@Date: 2025/01/09
remarks: 
"""
import re 
import copy
from task.single_task.single_task_base import SingleTaskBase


class SingleTaskXpoSample(SingleTaskBase):
    def __init__(self, d_st_config, d_st_input, retry_num, verbose=0):
        super().__init__(d_st_config, d_st_input, retry_num, verbose=verbose) 
        self.init_variables() 

    def init_variables(self):
        # 初始化options 
        self.options = "、".join([d['op_text'] for d in self.d_st_input['OP']]) 
        self.gt_ops = self.d_st_input['A'] 
        self.ref_answer = "[参考选项]:"+self.options+ "[答案选项]:"+self.gt_ops
        self.prefix = "Your response should be in the same language as the original question"
    
    def parse_score_num(self, data, mode):
        pattern = f'<{mode}>.*?(\d+).*?</{mode}>'
        matches = re.findall(pattern, data, re.DOTALL)
        if matches:
            num = matches[-1].replace(f"<{mode}>", "").replace(f"</{mode}>", "").strip()
        else:
            num = -1

        try:
            num = int(float(num))
        except:
            num = -1

        return num

    def cal_inner(self):
        l_xpo_sample_result = []
        for _ in range(self.d_st_config["sample_num_stage_d1"]):
            
            # stage d1: 
            stage_d1_node_input = self.get_stage_d1_node_input()
            stage_d1_node_output = self.run_node('node_one_prompt_xpo_sample_stage_d1', stage_d1_node_input) 
            self.sft_input = stage_d1_node_output["prompt_format"] 
            stage_d1_node_output = stage_d1_node_output["prompt_res"]
            if self.verbose > 1 :
                print(f'stage_d1_node_output: {stage_d1_node_output}')
            
            # stage d2: 
            stage_d2_node_input = self.get_stage_d2_node_input(stage_d1_node_output)
            stage_d2_node_output = self.run_node('node_one_prompt_xpo_sample_stage_d2', stage_d2_node_input)['prompt_res']
            if self.verbose > 1 :
                print(f'stage_d2_node_output: {stage_d2_node_output}')

            # stage d3: 
            stage_d3_node_output = self.get_stage_d3_node_output(stage_d2_node_output)
            if self.verbose > 1 :
                print(f'stage_d3_node_output: {stage_d3_node_output}')
            
            # stage d4: 
            stage_d4_node_input = self.get_stage_d4_node_input(stage_d1_node_input, stage_d3_node_output)
            stage_d4_node_output = self.run_node('node_one_prompt_xpo_sample_stage_d4', stage_d4_node_input)['prompt_res']
            stage_d4_node_output = {"pointwise_eval_score":self.parse_score_num(stage_d4_node_output, "score"), 
                                    "pointwise_eval_result":stage_d4_node_output} 
            if self.verbose > 1 :
                print(f'stage_d4_node_output: {stage_d4_node_output}')

            l_xpo_sample_result.append({
            "stage_d1_output": stage_d1_node_output,
            "stage_d2_output": stage_d2_node_output,
            "stage_d3_output": stage_d3_node_output,
            "stage_d4_output": stage_d4_node_output}) 
        
        # stage d5: 
        l_xpo_sample_result = sorted(l_xpo_sample_result, key=lambda x: x["stage_d4_output"]["pointwise_eval_score"], reverse=True) 
        l_xpo_sample_result = [d for d in l_xpo_sample_result if d["stage_d4_output"]["pointwise_eval_score"]>=0]  
        if self.verbose > 1 :
                print(f'l_xpo_sample_result_cnt-v1: {l_xpo_sample_result}')

        stage_d5_node_output = [] 
        self.d_st_output = copy.deepcopy(self.d_st_input) 
        
        if len(l_xpo_sample_result)<2:
            if self.verbose > 1 :
                print(f'l_xpo_sample_result_cnt-v1: {l_xpo_sample_result}')
            self.d_st_output['l_xpo_sample_result'] = stage_d5_node_output 
            return 

        best_answer = l_xpo_sample_result[0] 
        bad_answers = [d for d in l_xpo_sample_result[-5:] if d["stage_d4_output"]["pointwise_eval_score"]<60 and d!=best_answer]
        if self.verbose > 1 :
            print('='*100) 
            print(f'len(best_answer): {len(best_answer)} || len(bad_answers): {len(bad_answers)}')
            print(f'best_answer: {best_answer} || bad_answers: {bad_answers}')
            print('='*100) 

        if (not bad_answers) or best_answer['stage_d4_output']['pointwise_eval_score']<60:
            self.d_st_output['l_xpo_sample_result'] = stage_d5_node_output 
            return 

        for bad_answer in bad_answers:
            stage_d5_node_input = self.get_stage_d5_node_input(best_answer, bad_answer) 
            single_d5_node_output = self.run_node('node_one_prompt_xpo_sample_stage_d5', stage_d5_node_input)['prompt_res']

            pairtwise_eval_item = self.parse_score_num(single_d5_node_output, "better_item") 
            pairtwise_eval_score_1 = self.parse_score_num(single_d5_node_output, "score_1")
            pairtwise_eval_score_2 = self.parse_score_num(single_d5_node_output, "score_2") 
            
            sft_input = self.sft_input 
            ground_truth = self.ref_answer 
            
            d1_sft_target = best_answer['stage_d1_output']
            d2_sft_target = bad_answer['stage_d1_output']

            d1_sft_ops = best_answer['stage_d3_output']['sft_ops']
            d2_sft_ops = bad_answer['stage_d3_output']['sft_ops']

            d1_correctness = best_answer['stage_d3_output']['correctness']
            d2_correctness = bad_answer['stage_d3_output']['correctness']

            d1_pointwise_eval_score = best_answer['stage_d4_output']['pointwise_eval_score']
            d2_pointwise_eval_score = bad_answer['stage_d4_output']['pointwise_eval_score']
            
            valid_status = 1 if pairtwise_eval_item==1 and pairtwise_eval_score_1 > pairtwise_eval_score_2 and d1_pointwise_eval_score > d2_pointwise_eval_score else 0 
            if self.verbose > 1 :
                print(f'pairtwise_eval_item: {pairtwise_eval_item} || pairtwise_eval_score_1:{pairtwise_eval_score_1} || pairtwise_eval_score_2: {pairtwise_eval_score_2} || valid_status: {valid_status}')
            
            d1 = {"sft_input":sft_input,
                  "ground_truth":ground_truth,
                  "sft_target": d1_sft_target,
                  "sft_ops": d1_sft_ops,
                  "correctness": d1_correctness,
                  "pointwise_eval_score":d1_pointwise_eval_score,
                  "pairtwise_eval_score": pairtwise_eval_score_1
                  }
            
            d2 = {"sft_input":sft_input,
                  "ground_truth":ground_truth,
                  "sft_target": d2_sft_target,
                  "sft_ops": d2_sft_ops,
                  "correctness": d2_correctness,
                  "pointwise_eval_score":d2_pointwise_eval_score,
                  "pairtwise_eval_score": pairtwise_eval_score_2
                  }
            pair_wise_data = {"d1": d1, 
                              "d2": d2, 
                              "pairtwise_eval_details": single_d5_node_output,
                              "pairtwise_eval_item": pairtwise_eval_item,
                              "valid_status":valid_status
                              } 
            
            if self.verbose > 1 :
                print(f'pair_wise_data: {pair_wise_data}')

            stage_d5_node_output.append(pair_wise_data) 

        if self.verbose > 1 :
            print("*"*100)
            print(f'stage_d5_node_output: {stage_d5_node_output}') 
            print("*"*100)

        self.d_st_output = copy.deepcopy(self.d_st_input)
        self.d_st_output['l_xpo_sample_result'] = stage_d5_node_output

    def get_stage_d1_node_input(self):
        d_prompt_kv = {'Q': self.d_st_input['Q_open']}
        return {'d_prompt_kv': d_prompt_kv} 
    
    def get_stage_d2_node_input(self, stage_d1_node_output):
        d_prompt_kv = {"OPS": self.options, "answer_raw": stage_d1_node_output} 
        stage_d2_node_input = {'d_prompt_kv': d_prompt_kv} 

        return stage_d2_node_input
    
    
    def get_stage_d3_node_output(self, stage_d2_node_output):
        pattern = r'<Answer>.*(A|B|C|D|E).*</Answer>'
        matches = re.findall(pattern, stage_d2_node_output, re.DOTALL)

        sft_ops = '-1'
        if matches:
            sft_ops = matches[-1]
        else:
            sft_ops = stage_d2_node_output.replace('<Answer>', '').replace('</Answer>', '')

        correctness = 1 if sft_ops==self.gt_ops else 0

        stage_d3_node_output = {"sft_ops": sft_ops, 
                                "correctness": correctness} 

        return stage_d3_node_output
    
    def get_stage_d4_node_input(self, stage_d2_node_output, stage_d3_node_output):
        target = stage_d2_node_output 
        correctness = stage_d3_node_output["correctness"] 

        d_prompt_kv = {"input": self.sft_input,
                       "target": target,
                       "ref_answer": self.ref_answer,
                       "correctness": correctness}  
        stage_d4_node_input = {'d_prompt_kv': d_prompt_kv} 
        
        return stage_d4_node_input
    
    def get_stage_d5_node_input(self, best_answer, bad_answer):
        target_1 = best_answer["stage_d1_output"]
        target_2 = bad_answer["stage_d1_output"]

        correctness_1 = best_answer['stage_d3_output']['correctness']
        correctness_2 = bad_answer['stage_d3_output']['correctness']
        
        if correctness_1==0:
            correctness_1 = "错误"
        elif correctness_1==1:
            correctness_1 = "正确"
        else:
            correctness_1 = "未知"
        
        if correctness_2==0:
            correctness_2 = "错误"
        elif correctness_2==1:
            correctness_2 = "正确"
        else:
            correctness_2 = "未知"
        
        d_prompt_kv = dict(input=self.sft_input,
                            ref_answer=self.ref_answer,
                            target_1=target_1,
                            correctness_1=correctness_1,
                            target_2=target_2,
                            correctness_2=correctness_2)  
        stage_d5_node_input = {'d_prompt_kv': d_prompt_kv} 

        return stage_d5_node_input 