#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'


import sys
sys.path.append("/root/python/lalascan-devel/")


from lalascan.libs.core.pluginmanager import PluginManager, PluginImporter
from lalascan.libs.core.common import readfile
from lalascan.libs.core.globaldata import register_plugins, conf, vulresult
from lalascan.libs.core.report import TextReport

from lalascan.data.resource.url import URL

from lalascan.libs.core.scope import AuditScope, DummyScope
from lalascan.data.resource.domain import Domain

from lalascan.libs.core.spider import spider_task
from lalascan.libs.core.threads import plugin_run_thread, execute_plugin, MyResourcePool, MyGeventPool

from thirdparty_libs.oset.pyoset import oset

conf.audit_config = None
conf.plugin = "reflect_xss"
conf.vulresult = oset()
print id(conf.vulresult)
#conf.plugin = "sqli,reflect_xss,any_file_read"
conf.targets = []

#output result
conf.audit_scope.roots = ['www.baidu.com', 'bbs.baidu.com']
conf.audit_scope.domains = 'www.baidu.com'
conf.audit_scope.addresses = '192.168.0.1'
conf.audit_scope.web_pages = "http://www.baidu.com"

report = TextReport()

#-------
m_resource = URL(url = "http://news.iciba.com/appv3/wwwroot/ds.php?action=search&search_word=1")
#m_resource = URL(url = "http://login.qidian.com/Login.php?appId=17&target=1&unionlogin=1&areaId=1&pm=1&popup=2&style=2&returnURL=http://avd.qidian.com/OALoginJump.aspx?returnURL=http://game.qidian.com/game/cqby/client/ServerList.aspx")

#conf.targets.append(m_resource)

#t = StringImporter()
#moduleName = 'reflect_xss'

#conf.target = 'http://demo.aisec.cn/demo/aisec/'

#爬虫
#spider_task()
conf.targets = [m_resource]

p = PluginManager()
p.set_plugin()
#print type(register_plugins)
#register_plugins['sqli'].run_plugin(m_resource)

proPool = MyResourcePool(4)


'''
def execute_plugin(m_resource):
    pluginPool = MyGeventPool(5)
    for key, plugin in register_plugins.iteritems():
        ##proPool.apply_async(plugin_run_thread, (key, plugin, m_resource))
        #pluginPool.spawn(plugin_run_thread, key, plugin, m_resource)

    #pluginPool.join()
'''

for m_resource in conf.targets:
    print '*' * 50
    proPool.apply_async(execute_plugin, (register_plugins, m_resource,))


proPool.close()
try:
    proPool.join()
except KeyboardInterrupt,e:
    print 'fuck!'

global vulresult
print vulresult
report.generate_report()


#PluginImporter.delModule('sqli')
#print register_plugins['sqli'].run('222')