#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from .globaldata import register_plugins

def reg_instance_plugin(plugin_class):
    module = plugin_class.__module__.split('.')[-1]
    if module in register_plugins:
        return

    register_plugins[module] = plugin_class()
