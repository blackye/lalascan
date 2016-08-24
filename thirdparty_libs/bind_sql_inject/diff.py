#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

import difflib


def diff(a, b):
    """
    :param a: A string
    :param b: A string (similar to a)
    :return: Two strings (a_mod, b_mod) which are basically:
                a_mod = a - (a intersection b)
                b_mod = b - (a intersection b)
             Or if you want to see it in another way, the results are the
             parts of the string that make it unique between each other.

    >>> diff('123456', '123a56')
    ('4', 'a')

    >>> diff('yes 123abc', 'no 123abc')
    ('yes', 'no')

    >>> diff('123abc yes', '123abc no')
    ('yes', 'no')

    >>> diff('123abc yes', 'no 123abc no')
    ('yes', 'no no')
    """
    matching_blocks = difflib.SequenceMatcher(None, a, b).get_matching_blocks()
    removed_a = 0
    removed_b = 0

    for block in matching_blocks:
        a_index, b_index, size = block
        a = a[:a_index - removed_a] + a[a_index - removed_a + size:]
        b = b[:b_index - removed_b] + b[b_index - removed_b + size:]
        removed_a += size
        removed_b += size

    return a, b
