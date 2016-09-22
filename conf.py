#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

import os
import sys

import sys


dirname_path_func = os.path.dirname
abspath_path_func = os.path.abspath
join_path_func    = os.path.join

BASEDIR = os.path.dirname(__file__)

LIBDIR = BASEDIR + '/lib'
PLUGINDIR = BASEDIR + '/plugins'
CACHEDIR = BASEDIR + '/cache'

# system path
if BASEDIR not in sys.path:
	sys.path.append(BASEDIR)
if LIBDIR not in sys.path:
	sys.path.append(LIBDIR)
if PLUGINDIR not in sys.path:
	sys.path.append(PLUGINDIR)

#mysql config
DB_MYSQL_HOST = '172.16.203.129'
DB_MYSQL_USER = 'root'
DB_MYSQL_PWD = 'root'
DB_MYSQL_PORT = 3306
DB_MYSQL_DATABASE = 'lalascan'

#webvul leakinfo
LEAK_JSON_FILE = 'leakinfo.json'