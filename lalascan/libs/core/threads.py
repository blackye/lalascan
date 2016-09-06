#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from lalascan.libs.core.plugin import PluginBase

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



def plugin_run_thread(plugin_name, pluginheader, info):
    #if issubclass(pluginheader, PluginBase):
    #print '1'
    p = pluginheader
    print type(p)
    p.run_plugin(info)


def execute_plugin(register_plugins, m_resource):
    pluginPool = MyGeventPool(10)
    for key, plugin in register_plugins.iteritems():
        ##proPool.apply_async(plugin_run_thread, (key, plugin, m_resource))
        print m_resource
        pluginPool.spawn(plugin_run_thread, key, plugin, m_resource)

    pluginPool.join()