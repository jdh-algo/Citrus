# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: model_inference.py
@Date: 2025/01/09
remarks: 模型调用
"""

from utils.model_inference_http import get_model_inference_http
from utils.model_inference_vllm import model_inference_vllm


def model_inference(query, model, urls=[], prefix="", verbose=0):
    if 'citrus' in model:
        res, status = model_inference_vllm(query, prefix=prefix)
    else:
        res = get_model_inference_http(query, model, verbose=verbose)
    return res

