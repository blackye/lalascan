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
conf.plugin = "sqli,reflect_xss,any_file_read" #逗号中间不能有空格
#conf.plugin = "sqli"
conf.targets = []

#output result
conf.audit_scope.roots = ['www.baidu.com', 'bbs.baidu.com']
conf.audit_scope.domains = 'www.baidu.com'
conf.audit_scope.addresses = '192.168.0.1'
conf.audit_scope.web_pages = "http://www.baidu.com"

report = TextReport()

#-------
#m_resource = URL(url = "http://weiyun.city.qq.com/dayueshop/wx.php?redirect_url=12&r=wegoApi%2Fcookie&_=1473047775677&token=ryhfgs1407576378&callbackparam=success_jsonpCallback")
#m_resource = URL(url = "http://demo.aisec.cn:80/demo/aisec/post_link.php?id=1")
m_resource_1 = URL(url = 'http://172.16.203.129/wooyun_test2/vul/sqlinject/search.php', post_params = {"keyword":"12"})
#m_resource = URL(url = "http://login.qidian.com/Login.php?appId=17&target=1&unionlogin=1&areaId=1&pm=1&popup=2&style=2&returnURL=http://avd.qidian.com/OALoginJump.aspx?returnURL=http://game.qidian.com/game/cqby/client/ServerList.aspx")

#conf.targets.append(m_resource)

#t = StringImporter()
#moduleName = 'reflect_xss'

#conf.target = 'http://demo.aisec.cn/demo/aisec/'
conf.target = 'http://172.16.203.129/wooyun_test2/'

#爬虫
#spider_task()
conf.targets = [m_resource_1]

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


report.generate_report()

#PluginImporter.delModule('sqli')
#print register_plugins['sqli'].run('222')