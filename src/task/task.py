# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: task.py
@Date: 2025/01/09
remarks: 任务
"""
import os
import json
import time
from typing import List
from concurrent.futures import ThreadPoolExecutor
# from concurrent.futures import ProcessPoolExecutor
from task.single_task.single_task_base import SingleTaskBase
from task.single_task.factory_single_task import run_single_task

class Task(object):
    def __init__(self, d_task_card):
        self.d_task_card = d_task_card
        self.verbose = d_task_card.get('verbose', 0)
        self.path_task_input = self.d_task_card['path_task_input']
        self.path_task_output = self.d_task_card['path_task_output']
        self.stid = self.d_task_card['stid']
        self.n_processor = self.d_task_card['n_processor']
        self.n_save = self.d_task_card['n_save']
        self.n_retry= self.d_task_card['n_retry']
        self.flag_force = self.d_task_card['flag_force']
        self.d_output = {}
        self.l_input = []
    
    def cal(self):
        print('#'*10, 'task {} start'.format(self.d_task_card.get('task_name', '')), '#'*10)
        print('path_task_input', self.path_task_input)
        print('path_task_output', self.path_task_output)
        print('stid', self.stid)
        print('n_processor ', self.n_processor )
        print('n_save', self.n_save)
        print('n_retry', self.n_retry)
        self.get_input()
        self.get_output()

        print('total line: {}, success line: {}, need to run: {}'.format(
            len(self.l_input), len(self.d_output),
            len(self.l_input) - len(self.d_output)
        ))

        while True:
            a = time.time()
            l_once_input = self.get_once_input()
            if len(l_once_input) == 0:
                break
            l_single_task = self.get_single_task_result(l_once_input)
            self.update_output(l_single_task)
            self.save_result()

            print('total line: {}, success line: {}, fail line: {} need to run: {}, time use: {}s, speed: {}s/item'.format(
                len(self.l_input), 
                len([e for e in self.d_output.values() if e['line_status']=='success']),
                len([e for e in self.d_output.values() if e['line_status']=='fail']),
                len(self.l_input) - len(self.d_output),
                round(time.time()-a, 4),
                round((time.time()-a) / len(l_once_input), 4),
            ))
        self.save_result()

        print('#'*10, 'task {} end'.format(self.d_task_card.get('task_name', '')), '#'*10)

    def get_input(self):
        with open(self.path_task_input) as f:
            for line in f.readlines():
                d_tmp = json.loads(line)
                line_id = d_tmp['line_id']
                self.l_input.append((line_id, d_tmp))
    
    def get_output(self):
        if self.flag_force:
            return
        if not os.path.exists(self.path_task_output):
            return
        with open(self.path_task_output) as f:
            for line in f.readlines():
                d_tmp = json.loads(line)
                line_id = d_tmp['line_id']
                line_status = d_tmp['line_status']
                if line_status != 'success':
                    continue
                self.d_output[line_id] = d_tmp
    
    def get_once_input(self):
        l_once_input = []
        for line_id, d_tmp in self.l_input:
            if len(l_once_input) >= self.n_save:
                break
            if line_id in self.d_output:
                continue
            l_once_input.append((line_id, d_tmp))
        return l_once_input
    
    def get_single_task_result(self, l_once_input):
        if self.n_processor == 1:
            return self.get_single_task_result_singleton(l_once_input)
        with ThreadPoolExecutor(max_workers=self.n_processor) as executor:
            l_task = []
            for line_id, d_tmp in l_once_input:
                l_task.append(
                    executor.submit(run_single_task, self.stid, d_tmp, self.n_retry, self.verbose)
                )

            l_task_reslut = []
            for task in l_task:
                l_task_reslut.append(task.result())
        return l_task_reslut
    
    def get_single_task_result_singleton(self, l_once_input):
        l_task_result = []
        for line_id, d_tmp in l_once_input:
            result = run_single_task(self.stid, d_tmp, self.n_retry, self.verbose)
            l_task_result.append(result)

        return l_task_result

    def update_output(self, l_single_task: List[SingleTaskBase]):
        for st in l_single_task:
            if st.out_status != 0:
                self.d_output[st.line_id] = {'line_id': st.line_id, 'line_status': 'fail'}
            else:
                d_st_output = st.d_st_output
                d_st_output['line_id'] = st.line_id
                d_st_output['line_status'] = 'success'
                self.d_output[st.line_id] = d_st_output
    
    def save_result(self):
        with open(self.path_task_output, 'w') as fw:
            for line_id, _ in self.l_input:
                d_tmp = {'line_id': line_id, 'line_status': 'fail'}
                if line_id in self.d_output:
                    d_tmp = self.d_output[line_id]
                str_tmp = json.dumps(d_tmp, ensure_ascii=False)
                fw.write(str_tmp)
                fw.write('\n')


