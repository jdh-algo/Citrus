# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: node_one_prompt.py
@Date: 2025/01/09
remarks: single node - run noe prompt
"""

from task.node.node_base import NodeBase
from utils.model_inference import model_inference
from config.prompt import D_PROMPT_CONFIG


class NodeOnePrompt(NodeBase):
    def __init__(self, d_node_config, d_node_input, verbose=0):
        super().__init__(d_node_config, d_node_input, verbose=verbose)

    def cal_inner(self):
        prompt_fname = self.d_node_config['prompt']
        prompt_format = D_PROMPT_CONFIG[prompt_fname]
        
        model = self.d_node_config['model']
        d_prompt_kv = self.d_node_input['d_prompt_kv']
        if 'model' in self.d_node_input:
            model = self.d_node_input['model']
        prefix = self.d_node_config.get('prefix', '')

        prompt = prompt_format.format(**d_prompt_kv)
        prompt_res = model_inference(prompt, model, prefix=prefix)
        if prompt_res is None:
            raise ValueError('running model error: [model]: {}, [prompt]: {}'.format(model, prompt))

        self.d_node_output = {'prompt_res': prompt_res, 'prompt_format': prompt_format}