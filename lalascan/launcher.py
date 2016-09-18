#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from lalascan.libs.core.pluginmanager import PluginManager, PluginImporter
from lalascan.libs.core.common import readfile, post_query
from lalascan.libs.core.globaldata import register_plugins, conf, vulresult
from lalascan.libs.core.report import TextReport

from lalascan.data.resource.url import URL

from lalascan.libs.core.scope import AuditScope, DummyScope
from lalascan.data.resource.domain import Domain

from lalascan.libs.core.spider import spider_task
from lalascan.libs.core.threads import plugin_run_thread, execute_plugin, MyResourcePool, MyGeventPool


def init():
    get_multiple_target()
    http_req_initoption()

def run():
    report = TextReport()

    pluginmanager = PluginManager()
    pluginmanager.set_plugin()

    proPool = MyResourcePool(4)
    for m_resource in conf.targets:
        print '*' * 50
        proPool.apply_async(execute_plugin, (register_plugins, m_resource,))

    proPool.close()
    try:
        proPool.join()
    except KeyboardInterrupt,e:
        print 'fuck!'

    report.generate_report()

def get_multiple_target():
    #infocollect
    if conf.bspider:
        spider_task()

    else:
        if conf.post_data is not None:
            m_resource = URL(url = conf.url , post_params = post_query(conf.post_data), method = 'POST')
        else:
            m_resource = URL(url = conf.url, method = 'GET')
        conf.targets.append(m_resource)

    conf.audit_scope.roots = ['www.baidu.com', 'bbs.baidu.com']
    conf.audit_scope.domains = 'www.baidu.com'
    conf.audit_scope.addresses = '192.168.0.1'
    conf.audit_scope.web_pages = "http://www.baidu.com"

def init_report():
    report = TextReport()
    report.generate_report()

def http_req_initoption():
    _set_http_useragnet()


def _set_http_useragnet():
    pass

def _set_http_referer():
    pass

def _set_http_proxy():
    pass

def _set_http_timeout():
    pass
