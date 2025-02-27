# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: unify_mmlu_pro.py
@Date: 2024/12/09
remarks: Uniform file format-mmlu-pro
"""

import json
from typing import List
from apps.data_preprocess.unify_format.unify_base import Test, Option
from apps.data_preprocess.unify_format.unify_base import UnifyBase


class UnifyMmluPro(UnifyBase):
    def __init__(self, name, path_input):
        super().__init__(name, path_input)

    def create_test_list(self) -> List[Test]:
        l_test = []
        with open(self.path_input, encoding='utf-8') as f:
            for idx, line in enumerate(f.readlines()):
                d_input = json.loads(line)
                q = d_input["question"]
                a = d_input["answer"]
                l_op = [Option(chr(int(op_idx) + 65), op, chr(int(op_idx) + 65) + "." + op)
                        for op_idx, op in enumerate(d_input["options"])]
                test = Test(str(idx).zfill(5), q, a, None, l_op)
                l_test.append(test)

        return l_test
