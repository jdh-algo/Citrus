# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: main_task.py
@Date: 2025/02/09
remarks: Data Preprocessing - Main function entry
"""

from apps.data_preprocess.create_origin_file_process import CreateOriginFileProcess
from apps.data_preprocess.create_question_file_process import CreateQuestionFileProcess
from apps.data_preprocess.create_origin_file_with_data_label_process import CreateOriginFileWithDataLabelProcess


def main_data_preprocess(mode, d_task_card):
    if mode == 'data_label':
        cwqp = CreateOriginFileWithDataLabelProcess(d_task_card)
        cwqp.cal()

    if mode == 'create_origin_file':
        cep = CreateOriginFileProcess(d_task_card)
        cep.cal()


    # cqp = CreateQuestionFileProcess()
    # cqp.cal()