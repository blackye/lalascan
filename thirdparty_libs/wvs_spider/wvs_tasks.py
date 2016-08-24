#!/usr/bin/env python
#-*- coding:utf-8 -*-


from celery import Celery
import subprocess

'''
celery -A wvs_tasks worker --loglevel=info -Q add
'''

app = Celery()
app.config_from_object('wvs_celery_config')

@app.task
def wvs_spider_dispatch(url, keys, cookie):

	if cookie != None:
		cmdline = 'python wvs_run.py %s %s %s' % (url, keys, cookie)
	else:
		cmdline = 'python wvs_run.py %s %s' % (url, keys)

	print cmdline
	spider_proc = subprocess.Popen(cmdline, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	process_output = spider_proc.stdout.readlines()
	print 'wvs subprocess exit!'
	return process_output
    