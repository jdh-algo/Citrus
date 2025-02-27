# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: unify_medqa.py
@Date: 2024/12/09
remarks: Uniform file format-medqa
"""

import json
from typing import List
from apps.data_preprocess.unify_format.unify_base import Test, Option
from apps.data_preprocess.unify_format.unify_base import UnifyBase


class UnifyMedqa(UnifyBase):
    def __init__(self, name, path_input):
        super().__init__(name, path_input)

    def create_test_list(self) -> List[Test]:
        l_test = []
        with open(self.path_input, encoding='utf-8') as f:
            for idx, line in enumerate(f.readlines()):
                d_input = json.loads(line)
                q = d_input["question"]
                a = d_input["answer_idx"]
                if len(d_input["options"]) != 4:
                    continue
                l_op = [
                    Option(e, d_input["options"][e], '{}. {}'.format(e, d_input["options"][e]))
                    for e in ['A', 'B', 'C', 'D']
                ]
                test = Test(str(idx).zfill(5), q, a, None, l_op)
                l_test.append(test)

        return l_test
