#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from thirdparty_libs.argparse import argparse
from lalascan.libs.core.settings import USAGE, VERSION, UNICODE_ENCODING
from lalascan.libs.core.common import banner, console_output, generate_audit_name
from lalascan.libs.core.globaldata import cmdLineOptions, conf, L
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

    target = parser.add_argument_group('[ Targets ]')

    target.add_argument("-u", "--url", dest="url",
                        help="Target URL (e.g. \"http://www.lalascan.com/\")")

    target.add_argument("-t", "--threads", dest = "process_num",
                        help="max number of process, default cpu number")

    target = parser.add_argument_group('[ Resource Found ]')
    target.add_argument("-S", "--spider", dest="bspider", default = False, action = "store_true",
                        help="Enable user Spider")

    plugin = parser.add_argument_group('[ Plugin Option ]')

    plugin.add_argument("-e", "--enable-plugin", dest = "plugin", default = None,
                        help = "enable a plugin")

    request = parser.add_argument_group('[ Request Option ]')

    request.add_argument("--data", dest="post_data",
                         help="HTTP Post data")

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

    request = parser.add_argument_group('[ API Conf Option ]')
    request.add_argument("--update-leakinfo", dest="leakinfo", action="store_true", default=False,
                         help="Update or Generate webvulleak info.")

    request.add_argument("--update-policy", dest="policy", action="store_true", default = False,
                         help="Update or Generate vulnerability policy.")

    args = parser.parse_args()

    return args.__dict__

def initOptions(inputOptions = AttribDict()):

    try:
        #========================
        # api interface must be first
        if inputOptions['leakinfo']:
            from lalascan.api.option import generate_leak_info
            generate_leak_info()

        if inputOptions['policy']:
            from lalascan.api.option import _sava_policy2db
            _sava_policy2db()


        conf.url = inputOptions.url
        if conf.url is None:
            #L.logger.log_error("no target resource!")
            console_output(data = "[-] no target resource, lalascan over!\n")
            sys.exit()

        conf.audit_name = generate_audit_name(conf.url)
        L.set_logfilepath(conf.audit_name)  #设置扫描日志存放文件

        if inputOptions['process_num'] is not None:
            conf.threads = inputOptions.process_num
        else:
            conf.threads = cpu_count()

        if inputOptions['plugin'] is not None:
            conf.plugins = inputOptions.plugin
        else:
            conf.plugins = None

        #conf.audit_conf.cookie = inputOptions['cookie'] if inputOptions['cookie'] is not None else None

        conf.post_data = inputOptions['post_data'] if inputOptions['post_data'] is not None else None
        conf.cookie = inputOptions['cookie'] if inputOptions['cookie'] is not None else None

        conf.bspider = inputOptions['bspider']
        conf.targets = []
    except LalascanDataException:
        L.logger.log_error("init args option error!")
        sys.exit()

def main():

    banner()
    option_args = parse_cmd_options()
    cmdLineOptions.update(option_args)
    initOptions(cmdLineOptions)

    console_output("[*] Lalascanner starting at %s\n\n" % time.strftime("%X"))

    init()
    run()

if __name__  == '__main__': main()