#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'


import sys
sys.path.append("/root/python/lalascan-devel/")

from lalascan.libs.core.report import TextReport
from lalascan.libs.core.globaldata import conf

conf.audit_scope.roots = ['www.baidu.com', 'bbs.baidu.com']
conf.audit_scope.domains = 'www.baidu.com'
conf.audit_scope.addresses = '192.168.0.1'
conf.audit_scope.web_pages = "http://www.baidu.com"

p = TextReport()
p.generate_report()
