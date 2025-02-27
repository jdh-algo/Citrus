# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: unify_cmexam.py
@Date: 2024/12/09
remarks: Uniform file format-cm-exam
"""

import pandas as pd
from typing import List
from apps.data_preprocess.unify_format.unify_base import Test, Option
from apps.data_preprocess.unify_format.unify_base import UnifyBase


class UnifyCmExam(UnifyBase):
    def __init__(self, name, path_input):
        super().__init__(name, path_input)

    def create_test_list(self) -> List[Test]:
        l_test = []
        df = pd.read_csv(self.path_input, encoding='gb18030')
        for idx, row in df.iterrows():
            q = row["Question"]
            a = row["Answer"]
            c = row["Explanation"]

            l_op_str = [(e[0], e[1:].strip()) for e in row["Options"].split('\r\n')]
            l_op = [
                Option(e1, e2, '{}. {}'.format(e1, e2))
                for e1, e2 in l_op_str
            ]

            test = Test(str(idx).zfill(5), q, a, c, l_op)
            l_test.append(test)

        return l_test
