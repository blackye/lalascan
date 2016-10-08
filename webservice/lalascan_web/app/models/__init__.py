#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'


from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(use_native_unicode = 'utf8')