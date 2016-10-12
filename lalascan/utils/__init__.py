#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

import base64

def _str2bs64(str):
    return base64.b64encode(str)
