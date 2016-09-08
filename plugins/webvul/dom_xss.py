#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from lalascan.libs.core.plugin import PluginBase
from lalascan.libs.core.pluginregister import reg_instance_plugin
from lalascan.libs.core.globaldata import logger

from lalascan.libs.net.web_utils import parse_url, argument_query, get_request
from lalascan.libs.net.web_mutants import payload_muntants

from lalascan.data.resource.url import URL
from lalascan.utils.text_utils import to_utf8


import sys
import time
from bs4 import BeautifulSoup
import urlparse
import urllib
from termcolor import colored
from optparse import OptionParser


from PyQt4.QtCore import QUrl
from PyQt4.QtGui import QApplication
from PyQt4.QtWebKit import QWebPage
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest

try:
    import re2 as re
except ImportError:
    import re
else:
    re.set_fallback_notification(re.FALLBACK_WARNING)


try:
    import re2 as re
except ImportError:
    import re
else:
    re.set_fallback_notification(re.FALLBACK_WARNING)


class DomXssPlugin(PluginBase):

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


            return m_return


        if info.has_post_params:
            print 'POST'

        # Send the results
        return m_return

reg_instance_plugin(DomXssPlugin)