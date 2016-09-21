#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from lalascan.api.exception import LalascanNotImplementedError

from lalascan.libs.net.web_mutants import get_request
from lalascan.libs.core.globaldata import conf

from lalascan.data.resource import Data
from lalascan.data.resource.url import URL

from inspect import isclass
from time import sleep

class PluginBase(object):

    def __init__(self):
        pass

    def get_accepted_types(self):
        raise LalascanNotImplementedError()

    def run(self, info):
        raise LalascanNotImplementedError()

    def run_plugin(self, resource_input, resource_method , resource_param):

        #gevent pool run scan policy
        if isinstance(resource_input, Data):
            data = resource_input

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

                if isinstance(data, URL):
                    #test url whether access
                    if get_request(url = data, allow_redirects = False) is None:
                        return

                # Call the plugin.
                print resource_param
                result = self.run(data, method = resource_method, param = resource_param)
                sleep(0.05)
                return result

            except LalascanNotImplementedError:
                pass