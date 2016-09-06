#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys

from lalascan.data.enum import CUSTOM_LOGGING

logging.addLevelName(CUSTOM_LOGGING.SYSINFO, "*")
logging.addLevelName(CUSTOM_LOGGING.SUCCESS, "+")
logging.addLevelName(CUSTOM_LOGGING.ERROR, "-")
logging.addLevelName(CUSTOM_LOGGING.WARNING, "!")

LOGGER = logging.getLogger("lalascan")

LOGGER_HANDLER = None
try:
    from pocsuite.thirdparty.ansistrm.ansistrm import ColorizingStreamHandler

    disableColor = False

    for argument in sys.argv:
        if "disable-col" in argument:
            disableColor = True
            break

    if disableColor:
        LOGGER_HANDLER = logging.StreamHandler(sys.stdout)
    else:
        LOGGER_HANDLER = ColorizingStreamHandler(sys.stdout)
        LOGGER_HANDLER.level_map[logging.getLevelName("*")] = (None, "cyan", False)
        LOGGER_HANDLER.level_map[logging.getLevelName("+")] = (None, "green", False)
        LOGGER_HANDLER.level_map[logging.getLevelName("-")] = (None, "red", False)
        LOGGER_HANDLER.level_map[logging.getLevelName("!")] = (None, "yellow", False)
except ImportError, e:
    LOGGER_HANDLER = logging.StreamHandler(sys.stdout)

FORMATTER = logging.Formatter("\r[%(asctime)s] [%(levelname)s] %(name)s: %(message)s", datefmt = "%Y-%m-%d %H:%M:%S")

LOGGER_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(LOGGER_HANDLER)
LOGGER.setLevel(CUSTOM_LOGGING.WARNING)

class ScanLog(object):

    def log_verbose(self, msg):
        LOGGER.log(CUSTOM_LOGGING.SYSINFO,msg)

    def log_warning(self, msg):
        LOGGER.log(CUSTOM_LOGGING.WARNING, msg)

    def log_success(self, msg):
        LOGGER.log(CUSTOM_LOGGING.SUCCESS, msg)

    def log_error(self, msg):
        LOGGER.log(CUSTOM_LOGGING.ERROR, msg)


