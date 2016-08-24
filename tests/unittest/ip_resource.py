#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'


import os, sys

sys.path.append("/root/python/lalascan-devel/")

from lalascan.data.resource.ip import IP

try:
    print IP("192.168.0.1").address
except Exception:
    print 'fuck'