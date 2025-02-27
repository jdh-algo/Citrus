# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: unify_care_qa.py
@Date: 2025/02/23
remarks: Uniform file format-care_qa
"""

import pandas as pd
import json
from typing import List
from apps.data_preprocess.unify_format.unify_base import Test, Option
from apps.data_preprocess.unify_format.unify_base import UnifyBase

class UnifyCareQA(UnifyBase):
    def __init__(self, name, path_input):
        super().__init__(name, path_input)

    def create_test_list(self) -> List[Test]:
        l_test = []
        with open(self.path_input, encoding='utf-8') as f:
            for idx, line in enumerate(f.readlines()):
                d_input = json.loads(line)
                q = d_input["question"]
                # a = chr(int(d_input["cop"]) + 64)
                if d_input["cop"] == 1.0:
                    a = "A"
                elif d_input["cop"] == 2.0:
                    a = "B"
                elif d_input["cop"] == 3.0:
                    a = "C"
                elif d_input["cop"] == 4.0:
                    a = "D"
                l_op = [Option("A", d_input["op1"], "A." + str(d_input["op1"])),
                        Option("B", d_input["op2"], "A." + str(d_input["op2"])),
                        Option("C", d_input["op3"], "A." + str(d_input["op3"])),
                        Option("D", d_input["op4"], "A." + str(d_input["op4"]))]
                test = Test(str(idx).zfill(5), q, a, None, l_op)
                l_test.append(test)
        return l_test