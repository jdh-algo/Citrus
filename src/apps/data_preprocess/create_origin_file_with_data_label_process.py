# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: create_origin_file_with_data_label_process.py
@Date: 2024/12/09
remarks: Add data labels to raw data in a uniform format
"""

from task.task_process import TaskProcess
from config.config import data_configs

class CreateOriginFileWithDataLabelProcess(TaskProcess):
    def __init__(self, d_task_card):
        super().__init__(d_task_card)
        self.path_input_dir = data_configs.path_origin_dir
        self.path_output_dir = data_configs.path_origin_w_data_label_dir
