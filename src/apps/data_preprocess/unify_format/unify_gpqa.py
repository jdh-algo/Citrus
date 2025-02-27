# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: unify_gpqa.py
@Date: 2025/02/23
remarks: Uniform file format-gpqa
"""
import json
from typing import List
from apps.data_preprocess.unify_format.unify_base import Test, Option
from apps.data_preprocess.unify_format.unify_base import UnifyBase


class UnifyGpqa(UnifyBase):
    def __init__(self, name, path_input):
        super().__init__(name, path_input)

    def create_test_list(self) -> List[Test]:
        l_test = []
        with open(self.path_input) as f:
            for line in f.readlines():
                d_input = json.loads(line)

                idx = d_input["id"]
                q = d_input["Q"]
                a = d_input["A"]

                l_op = [
                    Option(e["op_idx"], e["op_value"], e["op_text"])
                    for e in d_input["OPS"]
                ]

                test = Test(str(idx).zfill(5), q, a, None, l_op)
                l_test.append(test)

        return l_test