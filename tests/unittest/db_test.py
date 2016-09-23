#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

import sys
sys.path.append("/root/python/lalascan-devel/")

from lalascan.utils.mymath import LalaMath

def main():
    #with AuditMysqlDB() as auditdb:
    #    print auditdb.get_alldata(audit_table = "webvul_leak_info", risk_level = 4)

    s = [2.3, 4.1, 6.2, 8.7]
    stdev = LalaMath.stdev(s)
    print stdev
    average = LalaMath.average(s)
    print average - 7 * stdev

if __name__ == '__main__': main()