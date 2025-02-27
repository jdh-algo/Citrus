# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: single_task_base.py
@Date: 2025/01/09
remarks: 
"""
import time
import traceback
from task.node.factory_node import get_node

class SingleTaskBase(object):
    def __init__(self, d_st_config, d_st_input, retry_num, verbose=0):
        self.d_st_config = d_st_config
        self.d_st_input = d_st_input
        self.retry_num = retry_num
        self.retry_num_really = 0
        self.stid = self.d_st_config['stid']
        self.line_id = self.d_st_input['line_id']
        self.verbose = verbose
        self.d_st_output = None
        self.out_msg = ''
        self.out_status = 1
        self.l_node = self.d_st_config.get('nodes', [])
        self.d_nid_node = {e['nid']: e for e in self.l_node}
    
    def cal(self):
        a = time.time()
        for n in range(self.retry_num):
            try:
                self.cal_inner()
                self.out_status = 0
                self.out_msg = 'ok'
                break
            except Exception as e:
                self.out_msg = traceback.format_exc()
                self.out_status = 1
        self.retry_num_really = n
        if self.verbose > 0:
            print("line_id:{}, retry_num:{}, status:{}, time_use:{}s, msg:{}".format(
                self.line_id, self.retry_num_really, self.out_status, 
                round(time.time()-a, 4), self.out_msg
            ))
    
    def cal_inner(self):
        d_node_output = self.run_node('node_base_1', {})
        self.d_st_output = d_node_output
    

    def run_node(self, nid, d_node_input: dict) -> dict:
        d_node_config = self.d_nid_node.get(nid)
        if d_node_config is None:
            raise ValueError("line_id:{}, stid: {}, nid: {} is invalid!".format(self.line_id, self.stid, nid))
        node = get_node(d_node_config, d_node_input, verbose=self.verbose)
        if node is None:
            raise ValueError("line_id:{}, stid: {}, nid: {} cannot get node, please check node config!".format(self.line_id, self.stid, nid))
        node.cal()
        if node.out_status != 0:
            raise ValueError("line_id:{}, stid: {}, nid: {} run error, msg: {}".format(self.line_id, self.stid, nid, node.out_msg))
        d_node_output = node.d_node_output
        return d_node_output

