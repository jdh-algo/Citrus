# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: model_inference_http.py
@Date: 2025/01/09
remarks: 模型调用-
"""
import json
import requests
import traceback
from typing import AnyStr
from config.config import model_api_configs

def get_model_inference_http(query, model, verbose=0, **kwargs):
    if model in ('gpt-4o', 'gpt-4o-mini'):
        return get_model_inference_openai_gpt(
            query, model, model_api_configs.open_ai.url, model_api_configs.open_ai.app_key, verbose=verbose
        )


def get_model_inference_openai_gpt(query: AnyStr, model: AnyStr, url: AnyStr, app_key: AnyStr, verbose=0) -> AnyStr:
    data = {
        "app_key": app_key,
        "messages": [
            {
                "role": "system",
                "content": "\nYou are ChatGPT, a large language model trained by OpenAI.\nKnowledge cutoff: 2024/06/05 11:09:20\nCurrent model: gpt-4-1106-preview\nCurrent time: {}"
            },
            {
                "role": "user",
                "content": query
            }
        ],
        "model": model,
        "stream": False
    }
    json_data = json.dumps(data)
    

    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Host': 'llm.jdh.com',
        'Connection': 'keep-alive',
        "Authorization": f"Bearer {app_key}",
    }

    try:
        resp = requests.post(url=url, data=json_data, headers=headers)
        if resp.status_code == 200:
            ret = resp.json()
            return ret['choices'][0]['message']['content']
        else:
            if verbose >= 1:
                print("[ERROR-1]: {}".format(resp.text))
    except Exception as err:
        if verbose >= 1:
            print("[ERROR-2]: {}".format(traceback.format_exc()))
