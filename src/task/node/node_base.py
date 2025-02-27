# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: base_node.py
@Date: 2025/01/09
remarks: single node - base class
"""

import traceback

class NodeBase(object):
    def __init__(self, d_node_config, d_node_input, verbose=0):
        self.nid = d_node_config['nid']
        self.d_node_config = d_node_config
        self.d_node_input = d_node_input
        self.d_node_output = None
        self.retry_num_config = d_node_config.get('retry_num', 1)
        self.retry_num_really = 0
        self.verbose = verbose
        self.out_msg = ''
        self.out_status = 1
    
    def cal(self):
        for _ in range(self.retry_num_config):
            self.retry_num_really += 1
            try:
                self.cal_inner()
                self.out_status = 0
                self.out_msg = 'ok'
            except Exception as e:
                self.out_msg = traceback.format_exc()
                self.out_status = 1
            
            if self.out_status == 0:
                break
            # if self.verbose == 1:
            #     print(self.out_msg)
    
    def cal_inner(self):
        self.d_node_output = {'prompt': self.d_node_config['prompt']}
        