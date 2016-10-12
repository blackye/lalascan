#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'



def f():

    s = ['']
    def g():
        s[0] = 'eeff'

    print s
    g()
    print 'fuck!'
    print s, type(s)

f()