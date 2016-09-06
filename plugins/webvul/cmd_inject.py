#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from lalascan.libs.core.plugin import PluginBase
from lalascan.libs.core.pluginregister import reg_instance_plugin
from lalascan.libs.core.globaldata import logger

from lalascan.libs.net.web_utils import parse_url, argument_query , get_request
from lalascan.libs.net.web_mutants import payload_muntants

from lalascan.data.resource.url import URL
from lalascan.utils.text_utils import to_utf8

from scanpolicy.policy import cmd_inject_detect_test_cases

try:
    import re2 as re
except ImportError:
    import re
else:
    re.set_fallback_notification(re.FALLBACK_WARNING)

class CmdInjectPlugin(PluginBase):

    '''
    this plugin is a any file read plugin
    '''

    #--------------------------------------------------------------------------
    def get_accepted_types(self):
        return [URL]


    #--------------------------------------------------------------------------
    def run(self, info):

        m_return = []

        if info.has_url_params:
            #param_dict = info.url_params
            for k,v in info.url_params.iteritems():
                key = to_utf8(k)
                value = to_utf8(v)

                for cmd_inject_case in cmd_inject_detect_test_cases:
                    p = payload_muntants(info, payload = {'k': k , 'pos': 1, 'payload':cmd_inject_case['input'], 'type': 0}, bmethod = info.method, timeout = 15.0)

                    if cmd_inject_case['target'] is not None:
                        if p is not None:
                            __ = re.search(cmd_inject_case['target'], p.data)
                            if __ is not None:
                                logger.log_verbose( '[+] found cmd inject!' )
                                return m_return



        if info.has_post_params:
            #param_dict = info.post_params
            for k,v in info.post_params.iteritems():
                key = to_utf8(k)
                value = to_utf8(v)

                for cmd_inject_case in cmd_inject_detect_test_cases:
                    p = payload_muntants(info, payload = {'k': k , 'pos': 1, 'payload':cmd_inject_case['input'], 'type': 0}, bmethod = info.method, timeout = 15.0)

                    if cmd_inject_case['target'] is not None:
                        if p is not None:
                            __ = re.search(cmd_inject_case['target'], p.data)
                            if __ is not None:
                                logger.log_verbose( '[+] found cmd inject!' )
                                return m_return

        # Send the results
        return m_return





