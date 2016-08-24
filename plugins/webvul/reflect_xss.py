#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from lalascan.libs.core.plugin import PluginBase
from lalascan.libs.core.pluginregister import reg_instance_plugin
from lalascan.libs.core.globaldata import logger

from lalascan.libs.net.web_utils import download, parse_url, argument_query, download, get_request
from lalascan.libs.net.web_mutants import payload_muntants

from lalascan.data.resource.url import URL
from lalascan.utils.text_utils import to_utf8


#from golismero.api.data.vulnerability.injection.xss import XSS

from scanpolicy.policy import xss_reflection_detect_test_cases
from random import randint
from bs4 import BeautifulSoup
from types import NoneType as NT

try:
    import re2 as re
except ImportError:
    import re
else:
    re.set_fallback_notification(re.FALLBACK_WARNING)

class ReflectXSSPlugin(PluginBase):

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

        #TODO 30X redirect


        #TODO Content-Type
        p = get_request(url = info, allow_redirects=False)
        if (p.status == '301' or p.status == '302') and not p.headers.get('Location'):

            return m_return

        if p.content_type is not None and re.search('(application\/json)|(application\/javascript)|(text\/json)|(text\/javascript)|'
                       '(application\/x-javascript)|(application\/octet-stream)|(text\/xml)|(application\/xml)', p.content_type) is not None:

            return m_return

        m_url = info

        if info.has_url_params:

            for k,v in m_url.url_params.iteritems():
                key = to_utf8(k)
                value = to_utf8(v)

                if self.xss_detect(m_url, method = 'GET', k = key, v = value):

                    url = URL(url = m_url.url,
                          method = 'GET',
                          post_params = None,
                          referer = m_url.referer)

                    print '[+] found reflected xss!'
                    #vul = XSS(url, vulnerable_params = {"injection":"xxxxxx"}, injection_point = XSS.INJECTION_POINT_URL, injection_type = "XSS")

                    #vul.description += "fuck"

                    #m_return.append()
                    break

                #return m_return

        if info.has_post_params:
            print 'POST'

        # Send the results
        return m_return

    def xss_detect(self, url, method = 'GET',  **kwargs):

        if not isinstance(url, URL):
            raise TypeError("Expected url type, type:%s" % type(url))

        k = kwargs.get("k", None)
        if k is None or not isinstance(k, str):
            raise ValueError("Except param has not key!")

        v = kwargs.get("v", None)

        for xss_test_case_dict in xss_reflection_detect_test_cases:
            #xss_test_case_dict = xss_reflection_detect_test_cases[12]

            rand_num = 900000000 + randint(1, 9999999)
            xss_payload = xss_test_case_dict['input'].replace('rndstr', str(rand_num))
            xss_resp = payload_muntants(url, payload = {'k': k , 'pos': 1, 'payload':xss_payload, 'type': 1}, bmethod = method)

            if xss_resp is None or xss_resp.data is None:
                return False

            tags_list , flags_list, targets_list = self._get_tags_flags(xss_test_case_dict['tag'], xss_test_case_dict['flag'], xss_test_case_dict['target'])
            flag_type = xss_test_case_dict['flag_type']
            compare   = xss_test_case_dict['compare']

            for tag in tags_list:

                result = []

                for flag in flags_list:

                    #TODO BUG targets_list must be one
                    try:
                        assert len(targets_list) == 1
                        target = targets_list[0].replace('rndstr', str(rand_num))

                        #print tag , flag , flag_type , target, compare
                        ret_without_quote, txt_without_quote = self._search_in_html(page = xss_resp.data, tag = tag, flag = flag, flag_type = flag_type, target = target, compare = compare)

                        single_quote_closed = False
                        double_quote_closed = False
                        big_brace_closed    = False
                        mid_brace_closed    = False

                        if 'rndstr' in targets_list[0]:
                            single_quote_closed, double_quote_closed, big_brace_closed, mid_brace_closed = self._check_whether_quote_closed(txt_without_quote, str(rand_num), xss_test_case_dict['input'])
                        else:
                            single_quote_closed, double_quote_closed, big_brace_closed, mid_brace_closed = self._check_whether_quote_closed(txt_without_quote, targets_list[0], xss_test_case_dict['input'])


                        if txt_without_quote is not None:
                            if compare == 'match':
                                rgx = 'lt;\s*%s\s*&gt;' % tag
                                if re.search(rgx, txt_without_quote) is not None or single_quote_closed == False or double_quote_closed == False:
                                    ret_without_quote = 0

                        if ret_without_quote > 0:
                            result.append(flag)

                    except AssertionError:
                        logger.log_verbose("targets list length must bu one!")
                        return False

                if len(result) > 0:
                    logger.log_verbose('[+] found reflect xss vulnerable!')
                    return True

        return False


    def _get_tags_flags(self, tags, flags, targets):
        return tags.split('|'), flags.split('|'), targets.split('|')


    def _check_whether_quote_closed(self, txt, target, input):

        single_quote_closed = False
        double_quote_closed = False
        big_brace_closed = False
        mid_brace_closed = False

        single_quote_cnt = 0
        double_quote_cnt = 0
        big_brace_left_cnt = 0
        big_brace_right_cnt = 0
        mid_brace_left_cnt = 0
        mid_brace_right_cnt = 0

        if not txt or target not in txt:
            return single_quote_closed, double_quote_closed, big_brace_closed, mid_brace_closed

        start_index = txt.index(target)
        for i, char in enumerate(txt[:start_index]):
            if i == 0:
                pre_char = ''
            else:
                pre_char = txt[i - 1]

            aft_char = txt[i + 1]

            if pre_char != '\\':
                if char == '\'':
                    if pre_char == '"' and aft_char == '"':
                        pass
                    else:
                        single_quote_cnt = single_quote_cnt + 1
                elif char == '"':
                    if pre_char == '\'' and aft_char == '\'':
                        pass
                    else:
                        double_quote_cnt = double_quote_cnt + 1

                elif char == '{':
                    big_brace_left_cnt = big_brace_left_cnt + 1
                elif char == '}':
                    big_brace_right_cnt = big_brace_right_cnt + 1
                elif char == '[':
                    mid_brace_left_cnt = mid_brace_left_cnt + 1
                elif char == ']':
                    mid_brace_right_cnt = mid_brace_right_cnt + 1

        if single_quote_cnt % 2 == 0:
            single_quote_closed = True
        if double_quote_cnt % 2 == 0:
            double_quote_closed = True

        if big_brace_left_cnt <=  big_brace_right_cnt:
            big_brace_closed = True

        if mid_brace_left_cnt <= mid_brace_right_cnt:
            mid_brace_closed = True

        return single_quote_closed, double_quote_closed, big_brace_closed, mid_brace_closed



    def _search_in_html(self, **kwargs):

        page = kwargs.get("page", None)
        if page is None or not isinstance(page, str):
            raise ValueError("Except param has not page_resp!")

        tag = kwargs.get("tag", None)
        if tag is None or not isinstance(tag, str):
            raise ValueError("Except param has not tag!")

        flag = kwargs.get("flag", None)
        if page is None or not isinstance(flag, str):
            raise ValueError("Except param has not flag!")

        flag_type = kwargs.get("flag_type", None)
        if flag_type is None or not isinstance(flag_type, str):
            raise ValueError("Except param has not flag_type!")

        target = kwargs.get("target", None)
        if target is None or not isinstance(target, str):
            raise ValueError("Except param has not compare!")

        compare = kwargs.get("compare", None)
        if compare is None or not isinstance(compare, str):
            raise ValueError("Except param has not compare!")

        html_soup = BeautifulSoup(page, 'html.parser', from_encoding = 'utf8')

        tag_nodes = []
        if tag == '*':
            for child in html_soup.descendants:
                if child.name != None:
                    #print child.name
                    tag_nodes.append(child)
        else:
            tag_nodes = html_soup.find_all(tag)

        if flag_type == "attr":
            for tag_item_node in tag_nodes:
                if isinstance(tag_item_node.attrs, dict):
                    if tag_item_node.attrs.has_key(flag):
                        attr_val = tag_item_node.attrs[flag]
                        if target in attr_val:
                        #    print '11111'
                            return 1, attr_val

        elif flag_type == "node":
            pass

        elif flag_type == "txt":
            for tag_item_node in tag_nodes:
                node_text = tag_item_node.text
                if target in node_text:
                    return 1, node_text

        return 0, None

reg_instance_plugin(ReflectXSSPlugin)