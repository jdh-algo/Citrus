# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: unify_mmlu.py
@Date: 2024/12/09
remarks: Uniform file format-mmlu
"""

import pandas as pd
from typing import List
from apps.data_preprocess.unify_format.unify_base import Test, Option
from apps.data_preprocess.unify_format.unify_base import UnifyBase


class UnifyMmlu(UnifyBase):
    def __init__(self, name, path_input):
        super().__init__(name, path_input)

    def create_test_list(self) -> List[Test]:
        df = pd.read_csv(self.path_input, header=None, names=['q', 'A', 'B', 'C', 'D', 'answer'])
        l_test = []
        for idx, row in df.iterrows():
            q = row["q"]
            a = row["answer"]
            l_op = [
                Option(e, row[e], '{}. {}'.format(e, row[e]))
                for e in ['A', 'B', 'C', 'D']
            ]
            test = Test(str(idx).zfill(5), q, a, None, l_op)
            l_test.append(test)

        return l_test
