#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

import multiprocessing
import multiprocessing.pool
from multiprocessing import Process
from multiprocessing import cpu_count
from gevent import pool
from gevent import monkey

monkey.patch_socket()


class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)

class MyPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess
# ------------------------------