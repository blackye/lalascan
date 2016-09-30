#!/usr/bin/env/python
#-*- coding:utf-8 -*-

"""
封装常用的时间函数
"""

__author__ = 'BlackYe.'

import time

class MyTime(object):

    format_datetime = "%Y-%m-%d %H:%M:%S"

    @classmethod
    def get_current_datetime(cls):
        return time.strftime(cls.format_datetime, time.localtime(time.time()))
