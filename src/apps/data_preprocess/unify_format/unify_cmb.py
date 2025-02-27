# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: unify_cmb.py
@Date: 2025/02/23
remarks: Uniform file format-cmb
"""
import json
from typing import List
from apps.data_preprocess.unify_format.unify_base import Test, Option
from apps.data_preprocess.unify_format.unify_base import UnifyBase


class UnifyCmb(UnifyBase):
    def __init__(self, name, path_input):
        super().__init__(name, path_input)

    def create_test_list(self) -> List[Test]:
        l_test = []
        with open(self.path_input, encoding='utf-8') as f:
            l_d_input = json.load(f)

        for idx, d_input in enumerate(l_d_input):
            q = d_input["question"]
            a = d_input["answer"]
            c = d_input["explanation"]
            l_op = [
                Option(e, d_input["option"][e], '{}. {}'.format(e, d_input["option"][e],))
                for e in ['A', 'B', 'C', 'D', 'E']
            ]
            test = Test(str(idx).zfill(5), q, a, c, l_op)
            l_test.append(test)

        return l_test
