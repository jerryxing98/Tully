#!/usr/bin/env python
#coding=utf-8
'''
Created on 2012-1-20

@author: Chine
'''

import os
import os.path
import collections

root_path = os.path.dirname(__file__)

def get_path(s):
    if isinstance(s, str):
        return os.path.join(root_path, s)
    elif isinstance(s, collections.Iterable):
        return os.path.join(root_path, os.sep.join(s))   