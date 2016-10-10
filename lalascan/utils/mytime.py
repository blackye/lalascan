#!/usr/bin/env/python
#-*- coding:utf-8 -*-

"""
封装常用的时间函数
"""

__author__ = 'BlackYe.'

from lalascan.api.exception import LalascanDataException

import time
from datetime import datetime

class MyTime(object):

    format_datetime = "%Y-%m-%d %H:%M:%S"

    @classmethod
    def get_current_datetime(cls):
        return time.strftime(cls.format_datetime, time.localtime(time.time()))


    @classmethod
    def parse_audit_times(cls, start_time, stop_time):
        """
        Converts the audit start and stop times into human readable strings.

        :param start_time: Audit start time,
        :type start_time: float | None

        :param stop_time: Audit stop time
        :type stop_time: float | None

        :returns: Audit start and stop times, total execution time.
        :rtype: tuple(str, str, str)
        """
        if start_time and stop_time:

            start = time.mktime(time.strptime(start_time, cls.format_datetime))
            end   = time.mktime(time.strptime(stop_time, cls.format_datetime))

            _start_time = datetime.fromtimestamp(start)
            _end_time  = datetime.fromtimestamp(end)
            if _start_time <= _end_time:
                td       = _end_time - _start_time
                days     = td.days
                hours    = td.seconds // 3600
                minutes  = (td.seconds // 60) % 60
                seconds  = td.seconds % 60
                run_time = "%d days, %d hours, %d minutes and %d seconds" % \
                    (days, hours, minutes, seconds)
                return start_time, stop_time, run_time

        raise LalascanDataException('Run time can not be calculated, please check the incoming time parameters!')