# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: unify_cmmlu.py
@Date: 2025/02/23
remarks: Uniform file format-cmmlu
"""
import json
from typing import List
from apps.data_preprocess.unify_format.unify_base import Test, Option
from apps.data_preprocess.unify_format.unify_base import UnifyBase


class UnifyCmmlu(UnifyBase):
    def __init__(self, name, path_input):
        super().__init__(name, path_input)

    def create_test_list(self) -> List[Test]:
        l_test = []
        with open(self.path_input, encoding='utf-8') as f:
            for idx, line in enumerate(f.readlines()):
                d_input = json.loads(line)
                q = d_input["Question"]
                a = d_input["Answer"]
                l_op = [Option("A", d_input["A"], "A." + d_input["A"]),
                        Option("B", d_input["D"], "B." + d_input["B"]),
                        Option("C", d_input["C"], "C." + d_input["C"]),
                        Option("D", d_input["D"], "D." + d_input["D"])]
                test = Test(str(idx).zfill(5), q, a, None, l_op)
                l_test.append(test)

        return l_test