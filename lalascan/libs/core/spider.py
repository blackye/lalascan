#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from lalascan.libs.core.plugin import PluginBase
from lalascan.libs.core.pluginregister import reg_instance_plugin
from lalascan.libs.core.globaldata import logger, conf

from lalascan.libs.net.web_utils import parse_url, argument_query, get_request
from lalascan.libs.net.web_mutants import payload_muntants

from lalascan.data.resource.url import URL, SpiderURL
from lalascan.utils.text_utils import to_utf8

from thirdparty_libs.wvs_spider.run import start_wvs_spider_dispatch

import json

def spider_task():
    cookie_param = None

    cookie_dict = conf.audit_config.cookie if conf.audit_config is not None and conf.audit_config.cookie is not None else None

    m_url = conf.target

    if cookie_dict != None:
        if hasattr(cookie_dict, "iteritems"):
                cookie_params = {
                    to_utf8(k): to_utf8(v) for k, v in cookie_dict.iteritems()
                }
                cookie_param = ';'.join(
                    '%s=%s' % (k ,v) for (k, v) in sorted(cookie_params.iteritems())
                )

    __ = start_wvs_spider_dispatch(m_url, cookie_param, logger)
    #__  = test_start_wvs_spider_dispatch('www.bbktel.com.cn_d2cc49d948a8589628d260faa6ba41a4')

    json_content = json.loads(__)

    for urls in json_content['info']:
        #print item
        logger.log_verbose("Web Spider:found url %s" % urls['fullurl'])
        m_resource = URL(url = urls['fullurl'])
        conf.targets.append(m_resource)
        for item_url in urls['content']:
            post_param = item_url['param_data']
            if "AcunetixBoundary_" in post_param:  #multipart/form-data
                method = 'FILE_UPLOAD'
            else:
                method = item_url['method']

            if method == "POST":
                post_param_dict = argument_query(item_url['param_data'])
                m_resource = URL(url = item_url['url'], method = "POST", post_params = post_param_dict, referer= urls['fullurl'])
            else:
                m_resource = URL(url = item_url['url'], method = method,  referer = urls['fullurl'])
            logger.log_verbose("Web Spider:found url %s" % item_url['url'])
            conf.targets.append(m_resource)