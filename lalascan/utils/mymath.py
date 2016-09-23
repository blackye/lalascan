#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

'''
Math Common Class
'''

from lalascan.api.exception import LalascanTypeError

from math import sqrt

class LalaMath(object):

    @classmethod
    def average(cls, values):

        '''
        :param cls:
        :param values: dict
        :return:

        >>> average([0.9, 0.9, 0.9, 1.0, 0.8, 0.9])
        0.9
        '''
        if isinstance(values, list):
            return (sum(values) / len(values)) if values else None
        else:
            raise LalascanTypeError("The average method of the math class must pass in a variable of the type List!")


    @classmethod
    def stdev(cls, values):
        """
        Computes standard deviation of a list of numbers.
        >>> stdev([0.9, 0.9, 0.9, 1.0, 0.8, 0.9])
        0.06324555320336757
        """

        if not isinstance(values, list):
            raise LalascanTypeError("The stdev method of the math class must pass in a variable of the type List!")

        if not values or len(values) < 2:
            return None

        key = (values[0], values[-1], len(values))


        avg = LalaMath.average(values)
        _ = reduce(lambda x, y: x + pow((y or 0) - avg, 2), values, 0.0)
        return sqrt(_ / (len(values) - 1))
