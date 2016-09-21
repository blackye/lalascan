#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

import sys
sys.path.append("/root/python/lalascan-devel/")

from lalascan.models.auditdb import AuditMysqlDB

def main():
    with AuditMysqlDB() as auditdb:
        print auditdb.get_alldata(audit_table = "webvul_leak_info", risk_level = 4)


if __name__ == '__main__': main()