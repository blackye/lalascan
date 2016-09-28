#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'


CSRF_ENABLED = True
SECRET_KEY = 'b6068e9b337f8177d6e8d858cb2117a5'

MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = '3306'
MYSQL_USER = 'root'
MYSQL_PWD  = ''
MYSQL_DATABASE = 'luscan_spider'
SQLALCHEMY_DATABASE_URI = 'mysql://{0}@{1}:{2}/{3}?charset=utf8mb4'.format(MYSQL_USER, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE)