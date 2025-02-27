# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: create_origin_file_process.py
@Date: 2024/12/09
remarks: Construct raw data in a uniform format
"""

import os
from apps.data_preprocess.unify_format.unify_mmlu import UnifyMmlu
from apps.data_preprocess.unify_format.unify_medqa import UnifyMedqa
from apps.data_preprocess.unify_format.unify_pubmedqa import UnifyPubMedqa
from apps.data_preprocess.unify_format.unify_jmed import UnifyJmed
from apps.data_preprocess.unify_format.unify_care_qa import UnifyCareQA
from apps.data_preprocess.unify_format.unify_medbullets import UnifyMedbullets
from apps.data_preprocess.unify_format.unify_mmlu_pro import UnifyMmluPro
from config.config import data_configs

# Data set registration
L_CLAZZ_DATA = [
    (UnifyMedqa, ['medqa', 'medqa_train_small']),
    (UnifyPubMedqa, ['pubmedqa']),
    (UnifyMmlu, ['mmlu-anatomy', 'mmlu-clinical_knowledge', 'mmlu-college_biology', 'mmlu-college_medicine', 'mmlu-medical_genetics', 'mmlu-professional_medicine',]),
    (UnifyJmed, ['jmed']),
    (UnifyCareQA, ["care_qa"]),
    (UnifyMedbullets, ["medbullets_op4", "medbullets_op5"]),
    (UnifyMmluPro, ["mmlu-pro_health", "mmlu-pro_biology"])
]

D_DATA_CLAZZ = {}
for clazz, l_data in L_CLAZZ_DATA:
    for data_name in l_data:
        D_DATA_CLAZZ[data_name] = clazz


class CreateOriginFileProcess(object):
    def __init__(self, d_task_card):
        self.d_task_card = d_task_card

    def cal(self):
        for d_tmp in data_configs.datasets:
            data_name, path_data = d_tmp['name'], d_tmp['download_file']
            if data_name not in self.d_task_card['l_data']:
                continue
            clazz = D_DATA_CLAZZ[data_name]
            path_data = os.path.join(
                data_configs.path_download_dir,
                path_data
            )
            c = clazz(data_name, path_data)
            c.cal()
