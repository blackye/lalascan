#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'


import sys
sys.path.append("/root/python/lalascan-devel/")


from lalascan.libs.core.pluginmanager import PluginManager, PluginImporter
from lalascan.libs.core.common import readfile
from lalascan.libs.core.globaldata import register_plugins, conf
from lalascan.data.resource.url import URL

from lalascan.libs.core.scope import AuditScope, DummyScope
from lalascan.data.resource.domain import Domain

from lalascan.libs.core.spider import spider_task

conf.audit_config = None
#m_resource = URL(url = "http://eduyun.nwnu.edu.cn/tpd/index.php?g=Help&menuid=36")
m_resource = URL(url = "http://xsg.swjtu.edu.cn/ArticleList.aspx?ClassID=42&Type=0&page=1")


#t = StringImporter()
moduleName = 'sqli'
#moduleName = 'reflect_xss'
'''
plugin_content = readfile("/root/python/lalascan-devel/plugins/webvul/sqli.py")

try:
    from sqli import SqliPlugin
except:
    print 'not register!'


try:
    importer = StringImporter(moduleName, plugin_content)
    importer.load_module(moduleName)
    #print sys.modules

except ImportError, ex:
    errMsg = "%s register failed \"%s\"" % (moduleName, str(ex))
    print errMsg

print register_plugins
'''

conf.target = 'http://demo.aisec.cn/demo/aisec/'

spider_task()

#p = PluginManager()
#p.set_plugin()
#print register_plugins

#print register_plugins['sqli'].run_plugin(m_resource)

#PluginImporter.delModule('sqli')
#print register_plugins['sqli'].run('222')