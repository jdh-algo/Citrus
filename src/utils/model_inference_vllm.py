# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: model_inference_vllm.py
@Date: 2025/01/09
remarks: 模型调用-本地vllm
"""


import re
import json
import time
import random
import datetime
import requests
import traceback
from time import sleep
from openai import OpenAI
from config.config import model_api_configs


def model_inference_vllm(prompt, prefix='', urls=['127.0.0.1:8080'], inference_type='test', model_name='citrus'):
    # API_URL = f"http://{url}/generate"
    API_ENDPOINTS = [f"http://{url}/v1" for url in urls]
    API_URL = random.choice(API_ENDPOINTS)
    client = OpenAI(
            api_key="EMPTY",
            base_url=API_URL,
    )
    messages = [{"role": "system", "content": prefix},
                {"role": "user", "content": prompt}]
        
    if inference_type == 'test':
        n_para = 1
    elif inference_type == 'sample':
        n_para = 20

    try:
        # 发送请求，设置超时
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model_name,
            temperature=0.7,
            stream=False,
            max_tokens=4096
        )   
        valid_response = chat_completion.choices[0].message.content        
        return valid_response, 1
    except requests.exceptions.Timeout:
        return [], 1
