# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: main_task.py
@Date: 2025/02/09
remarks: Model evaluation - Main function entry
"""

from apps.model_evaluate.model_evaluation_process import ModelEvaluationProcess


def main_evaluation(mode, d_task_card):
    if mode == 'single_model_evaluation':
        mep = ModelEvaluationProcess(d_task_card)
        mep.cal()