#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from random import randint, shuffle
import time

from lalascan.api.exception import LalascanNetworkException, LalascanAttributeError
from lalascan.api.exception import LalascanValueError
from lalascan.libs.core.plugin import PluginBase
from lalascan.libs.core.pluginregister import reg_instance_plugin
from lalascan.libs.core.globaldata import logger, vulresult
from lalascan.libs.net.web_utils import get_request
from lalascan.libs.net.web_mutants import payload_muntants, request_muntants
from lalascan.utils.mymath import LalaMath
from lalascan.data.resource.url import URL
from lalascan.data.vuln.vulnerability import WebVulnerability
from scanpolicy.policy import sql_inject_detect_err_msg_test_cases
from scanpolicy.policy import sql_inject_detect_boolean_test_cases
from scanpolicy.policy import sql_inject_detect_timing_test_cases
from thirdparty_libs.bind_sql_inject.fuzzy_string_cmp import relative_distance_boolean
from thirdparty_libs.bind_sql_inject.diff import diff
import math

try:
    import re2 as re
except ImportError:
    import re
else:
    re.set_fallback_notification(re.FALLBACK_WARNING)

TEST_SQL_TYPE = ['ERR_MSG_DETECT', "ORDER_BY_DETECT", "UNION_BY_DETECT"] #, "BOOLEAN_DETECT", "TIMING_DETECT"
#TEST_SQL_TYPE = ['BOOLEAN_DETECT']

RSP_SHORT_DURATION = 2

# 25% more/less than the original wait time
DELTA_PERCENT = 1.25

#time base seconds
DELAY_SECONDS = [3, 4, 6, 2]

#Minimum time response set needed for time-comparison based on standard deviation
MIN_TIME_RESPONSES = 30

# Coefficient used for a time-based query delay checking (must be >= 7)
# 99.9999999997440% of all non time-based SQL injection affected
# response times should be inside +-7*stdev([normal response times])
TIME_STDEV_COEFF = 7

###每个用例间隔时间系数
DURATION_VAR_RATIO = 0.85

##实际返回时间波动比例方差
MAX_RSP_DELAY_RATIO = 2

#order by check sign
ORDER_BY_SIGN = 'md5(95278)'

#order by md5 value
ORDER_BY_MD5_VAL = '59b874e05f47d8f295c63e0ed2578125'


class SqliPlugin(PluginBase):


    def __init__(self):
        self.response_times = []
        self.normal_rsp_time_stdev = 0
        self.normal_rsp_time_average = 0


    def get_accepted_types(self):
        return [URL]


    #--------------------------------------------------------------------------
    def run(self, info, **kwargs):

        m_url = info.url

        # If file is a javascript, css or image, do not run

        if info.parsed_url.extension[1:] in ('css', 'js', 'jpeg', 'jpg', 'png', 'gif', 'svg', 'txt') or ( not info.has_url_params and not info.has_post_params):
            logger.log_verbose("Skipping URL: %s" % m_url)
            return

        m_return = []

        b_continue = True
        m_source_url = []
        target = None

        '''
        if info.has_url_params:
            #param_dict = info.url_params

            for test_type in TEST_SQL_TYPE:
            #self.deal_param_payload(test_type, info.url, param_dict, method = info.method, referer = info.referer)
                if self.deal_param_payload(test_type, info, method = 'GET', param = kwargs['param']):
                    return m_return

        if info.has_post_params:
            print info.post_params
            #print info.url, info.post_params
            #param_dict = info.post_params

            for test_type in TEST_SQL_TYPE:
                #self.deal_param_payload(test_type, info.url, param_dict, method = info.method, referer = info.referer)
                if self.deal_param_payload(test_type, info, method = 'POST', param = kwargs['param']):
                    return m_return
        '''
        method = kwargs.get('method', None)
        if method is None or not isinstance(method, str):
            raise LalascanValueError("run plugin param has not method!")

        param = kwargs.get('param', None)
        if param is None or not isinstance(param, dict):
            raise LalascanValueError("run plugin param has not param!")

        for test_type in TEST_SQL_TYPE:
            if self.deal_param_payload(test_type, info, method = method , param = kwargs['param']):
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

        #if method == 'GET':
        #    param_dict = url.url_params
        #elif method == 'POST':
        #    param_dict = url.post_params

        param_dict = kwargs['param']

        is_timing_stable = True
        short_duration = 1

        def __check_if_rsp_stable_on_orig_input():
            p = request_muntants(url = url, allow_redirects=False)
            if p.status != '200':
                is_timing_stable = False

            orig_first_time       = p.elapsed
            orig_first_resp_body  = p.data

            time.sleep(2)

            p = request_muntants(url = url, allow_redirects=False)
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

        '''
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

        '''
        if sql_detect_type == "ERR_MSG_DETECT":
            for test_case_dict in sql_inject_detect_err_msg_test_cases:
                p, payload_resource = payload_muntants(url, payload = {'k': param_dict['param_key'] , 'pos': 1, 'payload':test_case_dict['input'], 'type': 0}, bmethod = method)
                if self._err_msg_sql_detect(p, test_case_dict['target']):
                    #print '[+] found sql inject in url:{0}, payload:{1}'.format(req_uri, payload_param_dict)
                    vulresult.put_nowait(WebVulnerability(target = payload_resource, vulparam_point = param_dict['param_key'] , method = method, payload = test_case_dict['input'], injection_type = "SQLI"))

                    logger.log_success('[!+>>>] found %s err_msg sql inject vulnerable!' % payload_resource.url)
                    return True

        elif sql_detect_type == "ORDER_BY_DETECT":
            if self._orderby_sql_detect(k = param_dict['param_key'], v = param_dict['param_value'] , url = url, method = method):
                return True

        elif sql_detect_type == "UNION_BY_DETECT":
            if self._union_sql_detect(k = param_dict['param_key'], v = param_dict['param_value'] , url = url, method = method):
                return True

        elif sql_detect_type == "ECHO_DETECT":
            self._echo_sql_detect()

        elif sql_detect_type == "BOOLEAN_DETECT":
            print '----------- BOOLEAN_DETECT -----------------------'

            if self._boolean_sql_detect(k = param_dict['param_key'], v = param_dict['param_value'] , url = url, method = method):
               return True

        elif sql_detect_type == "TIMING_DETECT":
            print '-----------TIMING_DETECT -----------------------'

            if self._timing_sql_detect(k = param_dict['param_key'], v = param_dict['param_value'], url = url, method = method, short_duration = short_duration):
                #print '[+] found time_based sql inject!'
                return True


    def _err_msg_sql_detect(self, response_mutants, sql_err_re):
        '''
        sql报错注入
        :return:
        '''

        if response_mutants is not None:
            self.add_normal_rsp_time(response_mutants.elapsed)
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

        for keyword in ['or', 'and']:
            max_order_column_payload = ' {0} 1=2 order by {1}--'.format( keyword, max_bound )
            min_order_column_payload = ' {0} 1=2 order by {1}--'.format( keyword, min_bound )

            p = request_muntants(url = url, allow_redirects = False)

            if p is None or p.status != '200':
                return False

            orig_resp_body  = p.data

            max_order_column_payload_rsp, _ = payload_muntants(url_info = url, payload = {'k': k , 'pos': 1, 'payload':max_order_column_payload, 'type': 0}, bmethod = method)
            min_order_column_payload_rsp, _ = payload_muntants(url_info = url, payload = {'k': k , 'pos': 1, 'payload':min_order_column_payload, 'type': 0}, bmethod = method)

            if max_order_column_payload_rsp is not None and min_order_column_payload_rsp is not None:
                self.add_normal_rsp_time(max_order_column_payload_rsp.elapsed)
            else:
                return False

            if max_order_column_payload_rsp.data != None and min_order_column_payload_rsp.data != None and (orig_resp_body != max_order_column_payload_rsp.data) and (orig_resp_body == min_order_column_payload_rsp.data):
                #maybe exist sql_inject

                while lower_index <= high_index:
                    #二分法
                    col = int(math.ceil( (lower_index + high_index) / 2))
                    column_payload = ' order by {0}--'.format(col)
                    print column_payload
                    column_payload_rsp = None
                    column_payload_rsp, _ = payload_muntants(url_info = url, payload = {'k': k , 'pos': 1, 'payload':column_payload, 'type': 0}, bmethod = method, use_cache = False)

                    if column_payload_rsp != None and column_payload_rsp.data != orig_resp_body:
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
                    union_payload = ' {0} 1=2 union select {1}'.format(keyword, ','.join(map(str,union_list)))
                    union_payload_rsp = None
                    try:
                        union_payload_rsp, payload_resource = payload_muntants(url_info = url, payload = {'k': k , 'pos': 1, 'payload':union_payload, 'type': 0}, bmethod = method, use_cache = False)

                        if union_payload_rsp is not None and ORDER_BY_MD5_VAL in union_payload_rsp.data:
                            vulresult.put_nowait(WebVulnerability(target = payload_resource, vulparam_point = k, method = method, payload = union_payload, injection_type = "SQLI"))
                            logger.log_success('[!+>>>] found %s order_by sql inject vulnerable!' % payload_resource.url)
                            return True

                    except LalascanAttributeError:
                        return False

        return False


    def _union_sql_detect(self, **kwargs):
        '''
        union 注入
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

        max_column = 20
        orig_rsp = request_muntants(url = url, allow_redirects = False)

        if orig_rsp is None or orig_rsp.status != '200':
            return False

        union_payload = None
        table_columns = 0
        first_union_payload_rsp_data = None

        for index in range(1, max_column):
            if index == 1:
                union_payload = " union select 1"
            else:
                union_payload = "{0},{1}".format(union_payload, index)
            print union_payload

            union_payload_rsp, payload_resource = payload_muntants(url_info = url, payload = {'k': k , 'pos': 1, 'payload':union_payload, 'type': 0}, bmethod = method)

            if union_payload_rsp is not None:
                if index == 1:
                    first_union_payload_rsp_data = union_payload_rsp.data

                else:
                    if (union_payload_rsp.data != first_union_payload_rsp_data) and (union_payload_rsp.data != orig_rsp.data):
                        #TODO Maybe WAF, union_payload_rsp.data != orig_rsp.data
                        if index == 2:
                            table_columns = [1,2]
                        else:
                            table_columns = index
                        break
            else:
                break

        if table_columns != 0 and isinstance(table_columns, str):
            for inject_index in range(table_columns):
                union_list = [x+1 for x in range(table_columns)]
                union_list[inject_index] = ORDER_BY_SIGN
                union_payload = ' union select {0}'.format(','.join(map(str,union_list)))
                union_payload_rsp = None
                try:
                    union_payload_rsp, payload_resource = payload_muntants(url_info = url, payload = {'k': k , 'pos': 1, 'payload':union_payload, 'type': 0}, bmethod = method, use_cache = False)

                    if union_payload_rsp is not None and ORDER_BY_MD5_VAL in union_payload_rsp.data:
                        vulresult.put_nowait(WebVulnerability(target = payload_resource, vulparam_point = k, method = method, payload = union_payload, injection_type = "SQLI"))
                        logger.log_success('[!+>>>] found %s union_by sql inject vulnerable!' % payload_resource.url)
                        return True

                except LalascanAttributeError:
                    return False
        elif isinstance(table_columns, list):
            union_payload_list = [' union select {0}'.format(ORDER_BY_SIGN), ' union select {0},2'.format(ORDER_BY_SIGN), ' union select 1, {0}'.format(ORDER_BY_SIGN)]
            for union_payload in union_payload_list:
                try:
                    union_payload_rsp, payload_resource = payload_muntants(url_info = url, payload = {'k': k , 'pos': 1, 'payload':union_payload, 'type': 0}, bmethod = method, use_cache = False)

                    if union_payload_rsp is not None and ORDER_BY_MD5_VAL in union_payload_rsp.data:
                        vulresult.put_nowait(WebVulnerability(target = payload_resource, vulparam_point = k, method = method, payload = union_payload, injection_type = "SQLI"))
                        logger.log_success('[!+>>>] found %s union_by sql inject vulnerable!' % payload_resource.url)
                        return True

                except LalascanAttributeError:
                    continue
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

            body_true_response = ""
            body_false_response = ""
            try:
                body_true_resp,  payload_resource  = payload_muntants(url_info = url, payload = {'k': k , 'pos': 1, 'payload':true_case, 'type': 1}, bmethod = method)
                if body_true_resp is not None:
                    body_true_response = body_true_resp.data

                body_false_resp, _  = payload_muntants(url_info = url, payload = {'k': k , 'pos': 1, 'payload':false_case, 'type': 1}, bmethod = method)
                if body_false_resp is not None:
                    body_false_response = body_false_resp.data

                self.add_normal_rsp_time(body_true_resp.elapsed)
            except AttributeError:
                continue

            if body_true_response == body_false_response:
                continue

            compare_diff = False
            #print 'Comparing body_true_response and body_false_response.'
            if self.__equal_with_limit(body_true_response, body_false_response,
                                 compare_diff):

                compare_diff = True

            body_confirm_true_response  = ""
            body_confirm_false_response = ""
            try:
                body_confirm_true_resp ,  _ = payload_muntants(url_info = url, payload = {'k': k , 'pos': 1, 'payload':confirm_true_case, 'type': 1}, bmethod = method)
                body_confirm_true_response = body_confirm_true_resp.data if body_confirm_true_resp is not None else None

                body_confirm_false_resp,  _ = payload_muntants(url_info = url, payload = {'k': k , 'pos': 1, 'payload':confirm_false_case, 'type': 1}, bmethod = method)
                body_confirm_false_response = body_confirm_false_resp.data if body_confirm_false_resp is not None else None
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

        while len(self.response_times) < MIN_TIME_RESPONSES:
            p = request_muntants(url = url, allow_redirects=False)
            if p is not None:
                self.add_normal_rsp_time(p.elapsed)

        self.normal_rsp_time_average = LalaMath.average(self.response_times)
        self.normal_rsp_time_stdev = LalaMath.stdev(self.response_times)

        rand_str = str(randint(90000, 99999))

        for timing_test_case_dict in sql_inject_detect_timing_test_cases:
        #if timing_test_case_dict is not None:

            payload_resource = None
            time_payload = ''
            def delay_for(original_wait_time, delay):
                time_payload = timing_test_case_dict['input'].replace("rndstr", rand_str).replace('duration', str(delay)).replace('val', v)

                delta = original_wait_time * DELTA_PERCENT
                upper_bound = (delay * 2) + original_wait_time + delta + 1
                lower_bound = original_wait_time + delay - delta

                try:
                    time_sleep_rsp , payload_resource = payload_muntants(url_info = url, payload = {'k': k , 'pos': 1, 'payload':time_payload, 'type': 1}, bmethod = method, use_cache = False, timeout = 30.0)
                    current_response_wait_time = time_sleep_rsp.elapsed
                    rsp_delay = int(math.ceil(current_response_wait_time))
                    lower_bound = delay + self.normal_rsp_time_average - TIME_STDEV_COEFF * self.normal_rsp_time_stdev  #正态分布
                    rsp_delay_ratio = rsp_delay / delay
                    return rsp_delay >= lower_bound, rsp_delay, rsp_delay_ratio, payload_resource

                    #if upper_bound > current_response_wait_time > lower_bound:
                    #    return True
                except Exception,e:
                    return False, 0, 0

            def get_original_time():
                try:
                    p = get_request(url = url, allow_redirects= False)
                    return p.elapsed if p is not None else None
                except LalascanNetworkException:
                    return None

            bvul = True
            all_rsp_delay = {}
            all_rsp_delay_ratio = []

            shuffle(DELAY_SECONDS)
            for delay in DELAY_SECONDS:
                #if not delay_for(get_original_time(), delay):
                #    bvul = False
                _ , rsp_delay, rsp_delay_ratio, payload_resource = delay_for(get_original_time(), delay)
                if not _:
                    #本轮检测结束
                    continue
                else:
                    all_rsp_delay[delay] = rsp_delay
                    all_rsp_delay_ratio.append(rsp_delay_ratio)
            sort_all_rsp_delay = sorted(all_rsp_delay.iteritems(), key=lambda x:x[0])

            last_delay = None
            last_rsp_delay = None
            for _ in sort_all_rsp_delay:
                if last_rsp_delay is None and last_delay is None:
                    last_rsp_delay = _[1]
                    last_delay = _[0]
                    continue

                if _[1] < last_rsp_delay:
                    continue  #over
                    #return False

                if (_[0] - last_delay) < ((_[1] - last_rsp_delay) * DURATION_VAR_RATIO):
                    continue #over
                    #return False

            rsp_delay_ratio_average = LalaMath.average(all_rsp_delay_ratio)
            rsp_delay_ratio_stdev   = LalaMath.stdev(all_rsp_delay_ratio)

            if rsp_delay_ratio_stdev > MAX_RSP_DELAY_RATIO:
                continue #over

            if bvul:
                vulresult.put_nowait(WebVulnerability(target = payload_resource, vulparam_point = k, method = method, payload = time_payload, injection_type = "SQLI"))
                logger.log_success('[!+>>>] found %s time-based sql inject vulnerable!' % payload_resource.url)
                return True

    #-----------------------------
    def add_normal_rsp_time(self, normal_rsp_time):
        '''
        # add normal rsp time to list
        :param normal_rsp_time:
        :return:
        '''
        if len(self.response_times) <= MIN_TIME_RESPONSES:
            self.response_times.append(normal_rsp_time)


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