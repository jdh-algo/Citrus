# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: unify_medbullets.py
@Date: 2025/02/23
remarks: Uniform file format-medbullets
"""
import json
from typing import List
from apps.data_preprocess.unify_format.unify_base import Test, Option
from apps.data_preprocess.unify_format.unify_base import UnifyBase


class UnifyMedbullets(UnifyBase):
    def __init__(self, name, path_input):
        super().__init__(name, path_input)

    def create_test_list(self) -> List[Test]:
        l_test = []
        with open(self.path_input, encoding='utf-8') as f:
            d_input = json.load(f)
        for idx in range(len(d_input["question"])):
            id = str(idx).zfill(5)
            idx = str(idx)
            q = d_input["question"][idx]
            a = d_input["answer_idx"][idx]
            if self.path_input.replace(".json", "")[-1] == "4":
                l_op = [Option("A", d_input["opa"][idx], "A." + d_input["opa"][idx]),
                        Option("B", d_input["opb"][idx], "B." + d_input["opb"][idx]),
                        Option("C", d_input["opc"][idx], "C." + d_input["opc"][idx]),
                        Option("D", d_input["opd"][idx], "D." + d_input["opd"][idx]),]
            elif self.path_input.replace(".json", "")[-1] == "5":
              l_op = [Option("A", d_input["opa"][idx], "A." + d_input["opa"][idx]),
                      Option("B", d_input["opb"][idx], "B." + d_input["opb"][idx]),
                      Option("C", d_input["opc"][idx], "C." + d_input["opc"][idx]),
                      Option("D", d_input["opd"][idx], "D." + d_input["opd"][idx]),
                      Option("E", d_input["ope"][idx], "E." + d_input["ope"][idx]),]
            test = Test(str(idx).zfill(5), q, a, None, l_op)
            l_test.append(test)
        return l_test