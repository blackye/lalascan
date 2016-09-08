#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

import multiprocessing
import multiprocessing.pool
from multiprocessing import Process
from multiprocessing import cpu_count
from multiprocessing import Queue
from gevent import pool
from gevent import monkey
import time
import requests

monkey.patch_socket()


result = Queue(100)


# ----------------------------------------------------------------------------------------------------
class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)

# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.
class MyPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess
# ------------------------------


def procFunc(url):
    #print url
    global result
    try:
        req = requests.get(url = url, timeout = 10)
        if req.status_code == 200:
            print '%s header:%s' % (url, req.headers)
            result.put(url)
    except Exception,e:
        print str(e)
        #return False

    #time.sleep(0.5)

def process_url(url_list):
    g = pool.Pool(5)
    #print 'fuck!!!'
    #for url in url_list:
    #    g.spawn(procFunc, url)
    g.map(procFunc, url_list)
    g.join()


def main():
    start = time.clock()
    proPool = MyPool(cpu_count())
    url_list = []
    for i in range(1, 100):
        url = "http://www.freebuf.com/news/%s.html" % i
        url_list.append(url)
        if i % 50 == 0:
            #print url_list
            proPool.apply_async(process_url,(url_list,))
            url_list = []

    proPool.close()
    try:
        proPool.join()
    except KeyboardInterrupt,e:
        print ('Caught KeyboardInterrupt, terminating workers')

    end = time.clock()
    print "scan time:%f s" % (end - start)

if __name__  == '__main__':
    main()
    print result.qsize()
    #start = time.clock()
    #process_url([ 'http://www.freebuf.com/news/%s.html'  % i for i in range(1, 1200)])
    #end = time.clock()
    #print "scan time:%f s" % (end - start)