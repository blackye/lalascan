#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from lalascan.models.auditdb import AuditMysqlDB
from lalascan.utils.mytime import MyTime

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


def generate_vul_policy():
    with AuditMysqlDB() as auditdb:
        pass

def _sava_policy2db():
    with AuditMysqlDB() as auditdb:
        from scanpolicy.policy import ALL_LIST
        for _ in ALL_LIST:
           test_case_module = "from scanpolicy.policy import %s" % _
           exec test_case_module
           try:
               module = eval(_)
               for test_case in module:
                   test_case.pop('case_id')
                   new_test_case = {}
                   new_test_case['spt_id'] = 1
                   new_test_case['sli_id'] = 2
                   new_test_case['policy_name'] = _.replace('_detect_test_cases', '')
                   new_test_case['content'] = str(test_case)
                   new_test_case['insert_time'] = MyTime.get_current_datetime()
                   new_test_case['update_time'] = MyTime.get_current_datetime()

                   auditdb().insert_by_dict('scan_leak_policy', new_test_case)

           except Exception,e:
               print str(e)
               print 'error'