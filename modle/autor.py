#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# @Time     : 2021/3/5 16:01
# @Author   : ordar
# @File     : autor.py
# @Project  : autoer
# @Python   : 3.7.5
from modle.auto_random import AUTO_RANDOM


class AUTOR:
    """
    统一管理所有插件，只需实例化这一个对象即可使用所有插件的所有方法
    """
    def __init__(self):
        self.random = AUTO_RANDOM()

