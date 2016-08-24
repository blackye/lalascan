#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exception Base class
"""


class LalascanBaseException(Exception):
    pass

class LalascanDataException(LalascanBaseException):
    pass

class LalascanSystemException(LalascanBaseException):
    pass

class LalascanThreadException(LalascanBaseException):
    pass

class LalascanNotImplementedError(NotImplementedError):
    pass

class LalascanTypeError(TypeError):
    pass

class LalascanValueError(ValueError):
    pass

class LalascanFileNotFoundException(LalascanBaseException):
    pass