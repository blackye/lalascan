#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

import os

from .settings import BANNER
from lalascan.libs.core.settings import BANNER, UNICODE_ENCODING
from lalascan.libs.core.globaldata import logger
from lalascan.libs.core.logger import LOGGER_HANDLER

from lalascan.data.enum import CUSTOM_LOGGING
from lalascan.utils.text_utils import to_utf8

from lalascan.api.exception import LalascanSystemException

from thirdparty_libs.colorizer import colored

from urllib import quote, quote_plus, unquote, unquote_plus
import sys
import re

def banner():
    """
    Function prints lalascan banner with its version
    """
    _ = BANNER
    #if not getattr(LOGGER_HANDLER, "is_tty", False):
    #    _ = re.sub("\033.+?m", "", _)
    #dataToStdout(_)


def console_output(data, bold = True):
    """
    Writes text to the stdout (console) stream
    """

    if isinstance(data, unicode):
        message = _stdoutencode(data)
    else:
        message = data

    sys.stdout.write(_setColor(message, bold))

    try:
        sys.stdout.flush()
    except IOError:
        pass

    return

def _stdoutencode(data):
    retVal = None

    try:
        data = data or ""
        retVal = data.encode(sys.stdout.encoding)
    except:
        retVal = data.encode(UNICODE_ENCODING) if isinstance(data, unicode) else data

    return retVal

def _setColor(message, bold=False):
    retVal = message

    if message and getattr(LOGGER_HANDLER, "is_tty", False):  # colorizing handler
        if bold:
            retVal = colored(message, color= None, on_color=None, attrs=("bold",))
    return retVal


class Singleton (object):
    """
    Implementation of the Singleton pattern.
    """
    _instance = None

    def __new__(cls):

        # If the singleton has already been instanced, return it.
        if cls._instance is not None:
            return cls._instance

        # Create the singleton's instance.
        cls._instance = super(Singleton, cls).__new__(cls)

        # Call the constructor.
        cls.__init__(cls._instance)

        # Delete the constructor so it won't be called again.
        cls._instance.__init__ = object.__init__
        cls.__init__ = object.__init__

        # Return the instance.
        return cls._instance


try:
    # The fastest JSON parser available for Python.
    from cjson import decode as json_decode
    from cjson import encode as json_encode
except ImportError:
    try:
        # Faster than the built-in module, usually found.
        from simplejson import loads as json_decode
        from simplejson import dumps as json_encode
    except ImportError:
        # Built-in module since Python 2.6, very very slow!
        from json import loads as json_decode
        from json import dumps as json_encode

# Remove the docstrings. This prevents errors when generating the API docs.
try:
    json_encode.__doc__ = ""
except Exception:
    _orig_json_encode = json_encode
    def json_encode(*args, **kwargs):
        return _orig_json_encode(*args, **kwargs)
try:
    json_decode.__doc__ = ""
except Exception:
    _orig_json_decode = json_decode
    def json_decode(*args, **kwargs):
        return _orig_json_decode(*args, **kwargs)


def readfile(filename):
    try:
        with open(filename) as f:
            retval = f.read()
        return retval
    except IOError, ex:
        errMsg = "something went wrong while trying to read "
        errMsg += "the input file ('%s')" % ex
        raise LalascanSystemException(errMsg)


def multiple_replace(text, adict):
    rx = re.compile("|".join(map(re.escape, adict)))

    def oneXlat(match):
        return adict[match.group(0)]
    return rx.sub(oneXlat, text)


def post_query(query):

    try:
        # much faster than parse_qsl()
        query_params = dict(( map(unquote_plus, (to_utf8(token) + '=').split('=', 2)[:2])
                              for token in query.split('&') ))
        if len(query_params) == 1 and not query_params.values()[0]:
            query_params = {}
        else:
            query = None
    except Exception:
        ##raise   # XXX DEBUG
        query_params = {}
    return query_params