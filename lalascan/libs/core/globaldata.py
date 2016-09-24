#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

'''
global var data
'''

from lalascan.libs.core.logger import ScanLog
from lalascan.data.datatype import AttribDict
from multiprocessing import Queue

# logger
logger = ScanLog()

# object to share within function and classes command
# line options and settings
conf = AttribDict()
conf.audit_scope = AttribDict()

#global multiprocessing result var
vulresult = Queue()

# Dictionary storing
# (1)targets, (2)registeredPocs, (3) bruteMode
# (4)results, (5)pocFiles
# (6)multiThreadMode \ threadContinue \ threadException
#kb = AttribDict()

cmdLineOptions = AttribDict()

register_plugins = AttribDict()
#registeredPocs = {}


#defaults = AttribDict(defaults)

