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
# CACHEDIR = BASEDIR + '/cache'

# system path
if BASEDIR not in sys.path:
	sys.path.append(BASEDIR)
if LIBDIR not in sys.path:
	sys.path.append(LIBDIR)
if PLUGINDIR not in sys.path:
	sys.path.append(PLUGINDIR)