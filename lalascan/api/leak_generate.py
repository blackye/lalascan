#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from lalascan.models.auditdb import AuditMysqlDB

from conf import CACHEDIR, LEAK_JSON_FILE, join_path_func
import json
import copy

def generate_leak_info():
    with AuditMysqlDB() as auditdb:
        leak_json = {}
        all_leak_data = auditdb.get_alldata(audit_table = "webvul_leak_info")
        for _ in all_leak_data:
            s = copy.copy(_).pop('leak_name')
            leak_json[s] = _
        with open(join_path_func(CACHEDIR, LEAK_JSON_FILE), 'w') as f:
            f.write(json.dumps(leak_json))
