# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: unify_pubmedqa.py
@Date: 2024/12/09
remarks: Uniform file format-pubmedqa
"""

import json
from typing import List
from apps.data_preprocess.unify_format.unify_base import Test, Option
from apps.data_preprocess.unify_format.unify_base import UnifyBase


class UnifyPubMedqa(UnifyBase):
    def __init__(self, name, path_input):
        super().__init__(name, path_input)

    def create_test_list(self) -> List[Test]:
        with open(self.path_input) as f:
            d_input = json.load(f)
        l_test = []
        l_op_str = [('A', 'yes'), ('B', 'no'), ('C', 'maybe')]

        for k, v in d_input.items():
            l_op = [
                Option(e[0], e[1], '{}. {}'.format(e[0], e[1]))
                for e in l_op_str
            ]
            answer_idx = None
            for e in l_op_str:
                if e[1] == v["final_decision"]:
                    answer_idx = e[0]
                    break
            
            if answer_idx is not None:
                test = Test(k, v["QUESTION"], answer_idx, v, l_op)
                l_test.append(test)
            else:
                print(k, 'no answer', v["final_decision"])
        return l_test
