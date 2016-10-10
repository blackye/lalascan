#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from lalascan.libs.core.pluginmanager import PluginManager, PluginImporter
from lalascan.libs.core.common import readfile, post_query, cookie_query
from lalascan.libs.core.globaldata import register_plugins, conf, db_audit, vulresult, source_result
from lalascan.libs.core.report import TextReport
from lalascan.libs.core.scope import AuditScope, DummyScope
from lalascan.libs.core.spider import spider_task
from lalascan.libs.core.threads import plugin_run_thread, execute_plugin, MyResourcePool, MyGeventPool

from lalascan.data.resource.url import URL
from lalascan.data.resource.domain import Domain

from lalascan.models.scan_task import ScanTask

from lalascan.utils.mytime import MyTime


def init():

    source_result.start_time = MyTime.get_current_datetime()

    http_req_initoption()
    get_multiple_target()

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

    source_result.end_time = MyTime.get_current_datetime()
    report.generate_report()

def get_multiple_target():
    #infocollect

    if conf.bspider:
        spider_task(conf.audit_name)

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

    #scan_task_model = ScanTask(audit_name = conf.audit_name, scan_url = conf.url, starttime = MyTime.get_current_datetime(), finishtime = MyTime.get_current_datetime())
    #db_audit.session.add(scan_task_model)
    #db_audit.session.commit()

def init_report():
    report = TextReport()
    report.generate_report()

def http_req_initoption():
    _set_http_useragnet()
    _set_http_cookie()


def _set_http_useragnet():
    pass

def _set_http_cookie():
    conf.cookie = cookie_query(conf.cookie)

def _set_http_referer():
    pass

def _set_http_proxy():
    pass

def _set_http_timeout():
    pass
