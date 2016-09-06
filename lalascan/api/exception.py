#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exception Base class
"""

__all__ = ["LalascanBaseException",
           "LalascanDataException",
           "LalascanSystemException",
           "LalascanThreadException",
           "LalascanNetworkException",
           "LalascanNetworkOutOfScope",
           "LalascanNotImplementedError",
           "LalascanTypeError",
           "LalascanValueError",
           "LalascanFileNotFoundException"]



class LalascanBaseException(Exception):
    pass

class LalascanDataException(LalascanBaseException):
    pass

class LalascanSystemException(LalascanBaseException):
    pass

class LalascanThreadException(LalascanBaseException):
    pass

class LalascanNetworkException(LalascanBaseException):
    """
    Network connection errors.
    """
    pass

#------------------------------------------------------------------------------
class LalascanNetworkOutOfScope(LalascanNetworkException):
    """
    Resource is out of audit scope.
    """
    pass


class LalascanNotImplementedError(NotImplementedError):
    pass

class LalascanTypeError(TypeError):
    pass

class LalascanValueError(ValueError):
    pass

class LalascanFileNotFoundException(LalascanBaseException):
    pass