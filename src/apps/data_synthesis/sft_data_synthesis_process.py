# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: model_evaluation_pipeline.py
@Date: 2024/12/09
remarks: 模型推理+评测
"""

import os
import json
from task.task_process import TaskProcess
from config.config import data_configs

class SftDataSynthesisProcess(TaskProcess):
    def __init__(self, d_task_card):
        super().__init__(d_task_card)
        self.path_input_dir = data_configs.path_origin_w_data_label_dir
    
    def cal(self):
        self.init_path()
        for data_name in self.d_task_card['l_data']:
            self.single_data_process(data_name)



