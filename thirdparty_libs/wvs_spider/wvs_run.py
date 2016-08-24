#!/usr/bin/env python
#-*- coding:utf-8 -*-


import sys
import optparse

#from thirdparty_libs.wvs_spider.wvs_console import WVSSpider
from wvs_console import WVSSpider


def do_wvs_crawl(target, keys, cookie):
	print 'start crawl %s, keys:%s' % (target, keys)
	WVSSpider(target, keys, cookie).start()


#def run_wvs_spider(target):
#	result = do_wvs_crawl(target)


def main():
	print len(sys.argv)
	if len(sys.argv) == 3:
		do_wvs_crawl(sys.argv[1], sys.argv[2], None)
	if len(sys.argv) == 4:
		do_wvs_crawl(sys.argv[1], sys.argv[2], sys.argv[3])


if __name__  == '__main__': main()