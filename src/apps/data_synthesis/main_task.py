# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: main_task.py
@Date: 2025/02/09
remarks: 数据合成-主函数入口
"""

from apps.data_synthesis.xpo_sample_process import XpoSampleProcess
from apps.data_synthesis.sft_data_synthesis_process import SftDataSynthesisProcess


def main_data_synthesis(mode, d_task_card):
    if mode == 'xpo_sample':
        xsp = XpoSampleProcess(d_task_card)
        xsp.cal()
    if mode == 'sft_data_synthesis':
        sdsp = SftDataSynthesisProcess(d_task_card)
        sdsp.cal()
    