#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'



BANNER = '''
 _          _
| |    __ _| | __ _ ___  ___ __ _ _ __
| |   / _` | |/ _` / __|/ __/ _` | '_ \\
| |__| (_| | | (_| \__ \ (_| (_| | | | |
|_____\__,_|_|\__,_|___/\___\__,_|_| |_|

LalaScan WebApplication vul scanner! '''

USAGE  = "Fuck"

VERSION = "1.0"


UNICODE_ENCODING = "utf-8"


PLUGIN_IMPORTDICT = {
    "from pocsuite.net import": "from pocsuite.lib.request.basic import",
    "from pocsuite.poc import": "from pocsuite.lib.core.poc import",
    "from pocsuite.utils import register": "from pocsuite.lib.core.register import registerPoc as register",
}

PLUGIN_REGISTER_STRING = "\nfrom lalascan.libs.core.plugin.pluginregister import reg_instance_plugin\nreg_instance_plugin({})"
PLUGIN_REGISTER_REGEX = "reg_instance_plugin\(.*\)"
PLUGIN_CLASSNAME_REGEX = "class\s+(.*?)\(PluginBase\)"


PLUGIN_SUFFIX = '.py'

NGX_HTTP_CODE = {
    'NGX_HTTP_ERROR'     : 500,
    'NGX_HTTP_FORBIDDEN' : 403,
    'NGX_HTTP_NOT_FOUND' : 404,
    'NGX_HTTP_AUTH'      : 401,
    'NGX_HTTP_REDIRECT'  : 301
}
