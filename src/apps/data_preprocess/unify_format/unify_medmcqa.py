# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: unify_medmcqa.py
@Date: 2024/12/09
remarks: Uniform file format-medmcqa
"""

import json
from typing import List
from apps.data_preprocess.unify_format.unify_base import Test, Option
from apps.data_preprocess.unify_format.unify_base import UnifyBase


class UnifyMedMcqa(UnifyBase):
    def __init__(self, name, path_input):
        super().__init__(name, path_input)

    def create_test_list(self) -> List[Test]:
        l_test = []
        with open(self.path_input, encoding='utf-8') as f:
            for line in f.readlines():
                d_input = json.loads(line)
                idx = d_input["id"]
                q = d_input["question"]
                a = chr(ord('A')+d_input['cop']-1)
                c = d_input["exp"]
                l_op = [
                    Option(e[0], d_input[e[1]], '{}. {}'.format(e[0], d_input[e[1]]))
                    for e in [('A', 'opa'), ('B', 'opb'), ('C', 'opc'), ('D', 'opd')]
                ]
                test = Test(idx, q, a, c, l_op)
                l_test.append(test)

        return l_test
