# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: main.py
@Date: 2025/02/09
remarks: main entry
"""
import json
import argparse
from apps.data_preprocess.main_task import main_data_preprocess
from apps.model_evaluate.main_task import main_evaluation
from apps.data_synthesis.main_task import main_data_synthesis



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='citrus pro training')
    parser.add_argument('-a', '--app', type=str, help='choose running app: data_preprocess, data_synthesis, model_evaluate') 
    parser.add_argument('-tc', '--task_card', type=str, help='detail task parameters for each mode') 
    args = parser.parse_args()


    with open(args.task_card) as f:
        d_task_card = json.load(f)    
    mode = d_task_card['mode']
    
    if args.app not in ('data_preprocess', 'data_synthesis', 'evaluation'):
        print('app must in: data_preprocess, data_synthesis, model_evaluate')
    
    if args.app == 'data_preprocess':
        main_data_preprocess(mode, d_task_card)
    if args.app == 'data_synthesis':
        main_data_synthesis(mode, d_task_card)
    if args.app == 'evaluation':
        main_evaluation(mode, d_task_card)