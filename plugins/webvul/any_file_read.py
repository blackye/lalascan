#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from lalascan.libs.core.plugin import PluginBase
from lalascan.libs.core.pluginregister import reg_instance_plugin
from lalascan.libs.core.globaldata import logger, vulresult
from lalascan.data.vuln.vulnerability import WebVulnerability

from lalascan.libs.net.web_utils import parse_url, argument_query, get_request
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

from scanpolicy.policy import any_file_read_detect_test_cases

try:
    import re2 as re
except ImportError:
    import re
else:
    re.set_fallback_notification(re.FALLBACK_WARNING)


class AnyFileReadPlugin(PluginBase):

    '''
    this plugin is a any file read plugin
    '''

    #--------------------------------------------------------------------------
    def get_accepted_types(self):
        return [URL]


    #--------------------------------------------------------------------------
    def run(self, info):
        #if not info.has_url_params and not info.has_post_params:
        #    return

        m_return = []

        if info.has_url_params:

            '''
            cookie_dict = Config.audit_config.cookie
            print cookie_dict
            if hasattr(cookie_dict, "iteritems"):
                    cookie_params = {
                        to_utf8(k): to_utf8(v) for k, v in cookie_dict.iteritems()
                    }
                    cookie_param = ';'.join(
                        '%s=%s' % (k ,v) for (k, v) in sorted(cookie_params.iteritems())
                    )

            print cookie_param
            print "GET"

            '''
            param_dict = info.url_params
            for k,v in param_dict.iteritems():

                key = to_utf8(k)
                value = to_utf8(v)

                for any_file_read_case in any_file_read_detect_test_cases:
                    p, payload_resource = payload_muntants(info, payload = {'k': key , 'pos': 1, 'payload':any_file_read_case['input'], 'type': 1}, bmethod = info.method)
                    if p is not None:
                        __ = re.search(any_file_read_case['target'], p.data)
                        if __ is not None:
                            vul = WebVulnerability(target = payload_resource, vulparam_point = key, method = 'GET', payload = any_file_read_case['input'], injection_type = "ANY_FILE_READ")
                            vulresult.put_nowait(vul)
                            logger.log_success('[!+>>>] found %s reflect xss vulnerable!' % payload_resource.url)

                            return m_return


        if info.has_post_params:
            param_dict = info.post_params
            for k,v in param_dict.iteritems():
                key = to_utf8(k)
                value = to_utf8(v)

                for any_file_read_case in any_file_read_detect_test_cases:
                    p , payload_resource = payload_muntants(info, payload = {'k': key , 'pos': 1, 'payload':any_file_read_case['input'], 'type': 1}, bmethod = info.method)
                    if p is not None:
                        __ = re.search(any_file_read_case['target'], p.data)

                        if __ is not None:
                            vul = WebVulnerability(target = payload_resource, vulparam_point = key, method = 'POST', payload = any_file_read_case['input'], injection_type = "ANY_FILE_READ")
                            vulresult.put_nowait(vul)
                            logger.log_success('[!+>>>] found %s reflect xss vulnerable!' % payload_resource.url)
                            return m_return

        # Send the results
        return m_return

reg_instance_plugin(AnyFileReadPlugin)