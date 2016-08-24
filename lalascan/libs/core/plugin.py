#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from lalascan.api.exception import LalascanNotImplementedError
from lalascan.data.resource import Data

from inspect import isclass

class PluginBase(object):

    def __init__(self):
        pass

    def get_accepted_types(self):
        raise LalascanNotImplementedError()

    def run(self, info):
        raise LalascanNotImplementedError()

    def run_plugin(self, plugin_input):

        #gevent pool run scan policy
        print plugin_input
        if isinstance(plugin_input, Data):
            data = plugin_input

            try:
                accepted_info = self.get_accepted_types()
                if isclass(accepted_info):
                    found = data.is_instance(accepted_info)
                else:
                    found = False
                    for clazz in accepted_info:
                        if data.is_instance(clazz):
                            found = True
                            break

                if not found:
                    msg = "Plugin %s cannot process data of type %s"
                    raise TypeError(msg % ('sqli', type(data)))

                # Call the plugin.
                result = self.run(data)

            except LalascanNotImplementedError:
                pass