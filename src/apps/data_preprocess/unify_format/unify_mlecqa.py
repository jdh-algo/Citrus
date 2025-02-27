# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: unify_mlec_qa.py
@Date: 2024/12/09
remarks: Uniform file format-mlec-qa
"""

import json
import pandas as pd
from typing import List
from apps.data_preprocess.unify_format.unify_base import Test, Option
from apps.data_preprocess.unify_format.unify_base import UnifyBase


class UnifyMlecqa(UnifyBase):
    def __init__(self, name, path_input):
        super().__init__(name, path_input)

    def create_test_list(self) -> List[Test]:
        l_test = []
        with open(self.path_input) as f:
            l = json.load(f)
        
        for de in l:
            idx = de['qid']
            q = de["qtext"].replace('\u3000', '')
            a = de["answer"]
            l_op = [
                Option(e, de["options"][e], '{}. {}'.format(e, de["options"][e],))
                for e in ['A', 'B', 'C', 'D', 'E', 'F']
                if e in de["options"]
            ]

            test = Test(idx, q, a, None, l_op)
            l_test.append(test)

        return l_test
