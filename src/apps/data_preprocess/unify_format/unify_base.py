# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: unify_format_base.py
@Date: 2024/12/09
remarks: Uniform file format-base class
"""

import os
import json
from typing import List
from collections import namedtuple
from config.config import data_configs

Test = namedtuple("Test", "id Q A C OP")
Option = namedtuple("Option", "op_idx op_value op_text")

class UnifyBase(object):
    def __init__(self, name, path_input):
        self.name = name
        self.path_input = path_input
        self.path_output = os.path.join(
            data_configs.path_origin_dir,
            '{}.jsonl'.format(name)
        )

    def cal(self):
        print("unify file {}".format(self.name))
        l_test = self.create_test_list()
        self.create_origin_file(l_test)

    def create_test_list(self) -> List[Test]:
        return []

    def create_origin_file(self, l_test: List[Test]):
        with open(self.path_output, 'w', encoding='utf-8') as fw:
            for test in l_test:
                d_op = None
                if type(test.OP) is list:
                    d_op = [{"op_idx": e.op_idx, "op_value": e.op_value, "op_text": e.op_text} for e in test.OP]

                d_tmp = {
                    "exam_name": self.name, "id": test.id,
                    "Q": test.Q, "A": test.A, "C": test.C,
                    "OP": d_op
                }
                str_tmp = json.dumps(d_tmp, ensure_ascii=False)
                fw.write(str_tmp)
                fw.write("\n")
