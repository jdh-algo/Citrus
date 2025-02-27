# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: single_task_factory.py
@Date: 2025/01/09
remarks: 
"""
from typing import Optional
from config.single_task import D_SINGLE_TASK_CONFIG
from task.single_task.single_task_base import SingleTaskBase
from task.single_task.single_task_data_labeling import SingleTaskDataLabeling
from task.single_task.single_task_evaluation import SingleTaskEvaluation
from task.single_task.single_task_xpo_sample import SingleTaskXpoSample
from task.single_task.single_task_sft_data_synthesis import SingleTaskSftDataSynthesis

L_ST_REGISTER = [
    SingleTaskBase,
    SingleTaskDataLabeling,
    SingleTaskEvaluation,
    SingleTaskXpoSample,
    SingleTaskSftDataSynthesis
]

D_ST = {e.__name__: e for e in L_ST_REGISTER}


def get_single_task(stid, d_st_input, retry_num, verbose=1) -> Optional[SingleTaskBase]:
    if stid not in D_SINGLE_TASK_CONFIG:
        return None
    d_st_config = D_SINGLE_TASK_CONFIG[stid]
    st_class = d_st_config['single_task_class']
    if st_class not in D_ST:
        return None
    single_task = D_ST[st_class](d_st_config, d_st_input, retry_num, verbose=verbose)
    return single_task

def run_single_task(stid, d_st_input, retry_num=1, verbose=1) -> Optional[SingleTaskBase]:
    single_task = get_single_task(stid, d_st_input, retry_num, verbose=verbose)
    if single_task is None:
        return None
    single_task.cal()
    return single_task


