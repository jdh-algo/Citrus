# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 JD.com, Inc. All Rights Reserved
#
"""
@File: node_factory.py
@Date: 2025/01/09
remarks: node factory
"""
from typing import Optional
from task.node.node_base import NodeBase
from task.node.node_one_prompt import NodeOnePrompt

L_NODE_REGISTER = [
    NodeBase,
    NodeOnePrompt
]

D_NAME_NODE = {clazz.__name__: clazz for clazz in L_NODE_REGISTER}

def get_node(d_node_config, d_node_input, verbose=1) -> Optional[NodeBase]:
    clazz = D_NAME_NODE.get(d_node_config.get('node_class'))
    if clazz is None:
        return None
    node = clazz(d_node_config, d_node_input, verbose=verbose)
    return node
