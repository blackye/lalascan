#!/usr/bin/env/python
#-*- coding:utf-8 -*-

"""
 单例模式基类
"""

__author__ = 'BlackYe.'


class Singleton (object):
    """
    Implementation of the Singleton pattern.
    """
    _instance = None

    def __new__(cls, *args, **kw):

        # If the singleton has already been instanced, return it.
        if cls._instance is not None:
            return cls._instance

        # Create the singleton's instance.
        cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)

        # Call the constructor.
        cls.__init__(cls._instance, *args, **kw)

        # Delete the constructor so it won't be called again.
        cls._instance.__init__ = object.__init__
        cls.__init__ = object.__init__

        # Return the instance.
        return cls._instance