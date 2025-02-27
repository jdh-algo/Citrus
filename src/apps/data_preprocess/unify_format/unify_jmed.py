# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: unify_jdh_inquiry.py
@Date: 2024/12/09
remarks: Uniform file format-jdh_inquiry
"""

import pandas as pd
from typing import List
from apps.data_preprocess.unify_format.unify_base import Test, Option
from apps.data_preprocess.unify_format.unify_base import UnifyBase

STR_Q_DIAGNOSIS = '''
患者年龄：{}
患者性别：{}
患者病情摘要：{}

根据上述患者的情况，请问最有可能的诊断是什么？
'''

class UnifyJmed(UnifyBase):
    def __init__(self, name, path_input):
        super().__init__(name, path_input)

    def create_test_list(self) -> List[Test]:
        l_test = []
        df = pd.read_excel(self.path_input)
        for _, row in df.iterrows():
            # 诊断题目
            idx = '{}-{}-diagnose-option'.format(
                int(row['diagId']), _
            )
            q = STR_Q_DIAGNOSIS.format(
                row['patient_age'], row['patient_sex'],
                row['final_question']
            )
            
            d_op = eval(row['final_options'])
            l_op = [
                Option(e, d_op[e], '{}. {}'.format(e, d_op[e]))
                for e in ['A', 'B', 'C', 'D', 'E', 'F']
                if e in d_op
            ]

            a = ','.join(eval(row['final_correct_answer']))

            c = None
            if 'glm_search_result' in row:
                c = row['glm_search_result']

            test = Test(idx, q, a, c, l_op)
            l_test.append(test)

        return l_test
