# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: create_question_file_process.py
@Date: 2024/12/09
remarks: Construct question data in a uniform format
"""

import os
import json
from config.config import data_configs


class CreateQuestionFileProcess(object):
    def __init__(self):
        pass

    def cal(self):
        for fname in os.listdir(data_configs.path_origin_dir):
            if not fname.endswith(".jsonl"):
                continue

            print("create question file {}".format(fname))
            with open(os.path.join(data_configs.path_origin_dir, fname), encoding='utf-8') as f:
                with open(os.path.join(data_configs.path_question_dir, fname), 'w', encoding='utf-8') as fw:
                    for line in f.readlines():
                        d_tmp = json.loads(line)
                        d_ques = {
                            e: d_tmp[e] for e in ["exam_name", "id", "Q", "OP"]
                        }
                        str_ques = json.dumps(d_ques, ensure_ascii=False)
                        fw.write(str_ques)
                        fw.write("\n")