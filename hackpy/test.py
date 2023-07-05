#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
使用requests请求隧道服务器
请求http和https网页均适用
"""
import os
import random
with open(os.getcwd()+'/user-agents.txt') as f:
                agent = f.readlines()
                print(type(random.choice(agent)))