#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

'''
global var data
'''

from lalascan.libs.core.logger import _ScanLog
from lalascan.data.datatype import AttribDict
from lalascan.models import _DBConfig
from multiprocessing import Queue

# object to share within function and classes command
# line options and settings
conf = AttribDict()

source_result = AttribDict()
conf.audit_scope = AttribDict()

# logger
class L(object):
    logger = None

    @classmethod
    def set_logfilepath(cls, audit_name):
        L.logger = _ScanLog(audit_name)

db_audit = _DBConfig()

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

