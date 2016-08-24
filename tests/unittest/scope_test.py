#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

import sys
sys.path.append("/root/python/lalascan-devel/")

from lalascan.libs.core.scope import AuditScope, DummyScope
from lalascan.data.resource.domain import Domain


p = AuditScope()
audit_scope = DummyScope()
p.add_target("http://www.baidu.com/?id=1&p=3")
audit_scope = p
