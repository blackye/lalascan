#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from lalascan.libs.core.plugin import PluginBase
from lalascan.libs.core.globaldata import vulresult
from lalascan.utils.text_utils import to_utf8
from lalascan.data.resource import Resource

import multiprocessing
import multiprocessing.pool
from multiprocessing import Process
from multiprocessing import cpu_count
import gevent
from gevent.pool import Pool
#from gevent.threadpool import ThreadPool

from gevent import monkey

monkey.patch_socket()


class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)

class MyResourcePool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess
# ------------------------------

class MyGeventPool(gevent.pool.Pool):

    def _wait(self):
        gevent.wait()



def plugin_run_thread(plugin_name, pluginheader, info, method, **kwargs):
    #if issubclass(pluginheader, PluginBase):
    #print '1'
    p = pluginheader
    print type(p)
    p.run_plugin(info, resource_method = method , resource_param = kwargs)


def execute_plugin(register_plugins, m_resource):
    pluginPool = MyGeventPool(30)
    for key, plugin in register_plugins.iteritems():
        ##proPool.apply_async(plugin_run_thread, (key, plugin, m_resource))

        if isinstance(m_resource, Resource):
            if m_resource.has_url_params:
                param_dict = m_resource.url_params
                method = 'GET'
            if m_resource.has_post_params:
                param_dict = m_resource.post_params
                method = 'POST'

            for k, v in param_dict.iteritems():
                param_key   = to_utf8(k)
                param_value = to_utf8(v)
                pluginPool.spawn(plugin_run_thread, key, plugin, m_resource, method = method, param_key = param_key, param_value = param_value)

    pluginPool.join()