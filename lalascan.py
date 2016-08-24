#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from thirdparty_libs.argparse import argparse
from lalascan.libs.core.settings import USAGE, VERSION, UNICODE_ENCODING
from lalascan.libs.core.common import banner, console_output
from lalascan.libs.core.globaldata import cmdLineOptions, conf, logger
from lalascan.data.datatype import AttribDict
from lalascan.data.enum import CUSTOM_LOGGING
from lalascan.api.exception import LalascanDataException
from lalascan.launcher import init, run

from multiprocessing import cpu_count

import sys, time

def parse_cmd_options():
    parser = argparse.ArgumentParser(usage=USAGE, formatter_class=argparse.RawTextHelpFormatter, add_help=False)

    parser.add_argument("-h", "--help", action="help",
                        help="Show help message and exit")

    parser.add_argument("--version", action="version",
                        version=VERSION, help="Show program's version number and exit")

    target = parser.add_argument_group('[Targets]')

    target.add_argument("-u", "--url", dest="url",
                        help="Target URL (e.g. \"http://www.lalascan.com/\")")

    target.add_argument("-t", "--threads", dest = "process_num",
                        help="max number of process, default cpu number")

    plugin = parser.add_argument_group('[Plugin Option]')

    plugin.add_argument("-e", "--enable-plugin", dest = "plugin", default=[],
                        help = "enable a plugin")

    request = parser.add_argument_group('[Request Option]')

    request.add_argument("--cookie", dest="cookie",
                         help="HTTP Cookie header value")

    request.add_argument("--referer", dest="referer",
                         help="HTTP Referer header value")

    request.add_argument("--user-agent", dest="agent",
                         help="HTTP User-Agent header value")

    request.add_argument("--random-agent", dest="randomAgent", action="store_true", default=False,
                         help="Use randomly selected HTTP User-Agent header value")

    request.add_argument("--proxy", dest="proxy",
                         help="Use a proxy to connect to the target URL")

    request.add_argument("--timeout", dest="timeout",
                         help="Seconds to wait before timeout connection (default 30)")

    request.add_argument("--retry", dest="retry", default=False,
                         help="Time out retrials times.")

    args = parser.parse_args()

    return args.__dict__

def initOptions(inputOptions = AttribDict()):

    try:
        conf.url = inputOptions.url
        if inputOptions['process_num'] is not None:
            conf.threads = inputOptions.process_num
        else:
            conf.threads = cpu_count()

        conf.plugins = inputOptions.plugin

        conf.targets = []
    except LalascanDataException:
        logger.log(CUSTOM_LOGGING.ERROR, "init args option error!")


def main():

    banner()

    option_args = parse_cmd_options()
    cmdLineOptions.update(option_args)
    initOptions(cmdLineOptions)

    console_output("[*] Lalascanner starting at %s\n\n" % time.strftime("%X"))

    init()
    run()

if __name__  == '__main__': main()