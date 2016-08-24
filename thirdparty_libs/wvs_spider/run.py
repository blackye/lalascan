#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'


__all__ = []


#------------------------------------------------------------------------------
# Fix the module load path.

import os, sys
from os import path
import redis

here = path.split(path.abspath(__file__))[0]
if not here:  # if it fails use cwd instead
	here = path.abspath(os.getcwd())
if not here in sys.path:
	sys.path.insert(0, here)
# add parent path
parent = path.abspath(path.join(here, '../../../'))
if not parent in sys.path:
	sys.path.insert(0, parent)


from celery import Celery, platforms
import sys, time, datetime, random, hashlib, urllib, requests
from lib.config import REDIS_SERVER, REDIS_PWD

def start_wvs_spider_dispatch(target, cookie, Logger):
	app = Celery()
	app.config_from_object('wvs_celery_config')
	domain = get_crawl_domain(target)
	keys = get_save_crawl_folder_name(domain)
	Logger.log_verbose("Web Spider: Crawl Domain:%s, keys:%s"  % (domain, keys))
	Logger.log_verbose("Web Spider: Spider is Running!")
	app.send_task('wvs_tasks.wvs_spider_dispatch', args=[target, keys, cookie])
	platforms.C_FORCE_ROOT = True
	Logger.log_verbose('Waiting spider return content..........')
	return wait_parse_result(keys)

def test_start_wvs_spider_dispatch(keys):
	return wait_parse_result(keys)

def get_save_crawl_folder_name(domain):

	if isinstance(domain, str):
		cur_time =  str(int(time.mktime(datetime.datetime.now().timetuple())))
		seed =  ''.join(random.sample('abcdefghijklmnopqrstuvwxyz!@#$%^&*', 5))
		__ = hashlib.md5()
		__.update(cur_time + seed)
		return '{0}_{1}'.format(domain, __.hexdigest())

def get_crawl_domain(url):
	if isinstance(url, str):
		protocol, __ = urllib.splittype(url)
		host = urllib.splitnport(urllib.splithost(__)[0])
		return host[0]

def wait_parse_result_by_redis(keys):
	s = requests.session()
	s.keep_alive = False
	redis_url = 'http://172.16.203.129:7379/GET/'
	spider_json_content = None
	while True:
		spider_json = requests.get(url = redis_url + keys).json()
		if spider_json['GET'] is not None:
			spider_json_content = spider_json['GET']
			break
		time.sleep(1)
	return spider_json_content 

def wait_parse_result(keys):
    pool = redis.ConnectionPool(host = REDIS_SERVER , port = 6379, db = 0, password = REDIS_PWD)
    r = redis.Redis(connection_pool = pool)
    spider_json_content = None
    while True:
        #TODO timeout is need
        try:
            _ = r.get(keys)
            if _ is not None:
                spider_content = eval(_)
                if isinstance(spider_content, dict) and spider_content.haskey('GET') and spider_content['GET'] is not None:
                    spider_json_content = spider_content['GET']
                    break
        except Exception:
            time.sleep(1)

    return spider_json_content

if __name__ == '__main__':
	if len(sys.argv) == 3:
		start_wvs_spider_dispatch(sys.argv[1], sys.argv[2], sys.argv[3])  #url, cookie
