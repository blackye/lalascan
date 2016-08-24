#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'


from lalascan.libs.core.globaldata import conf, logger
from lalascan.data.enum import CUSTOM_LOGGING
from lalascan.libs.core.common import readfile, multiple_replace
from lalascan.libs.core.settings import PLUGIN_SUFFIX

from lalascan.api.exception import LalascanFileNotFoundException, LalascanSystemException, LalascanValueError
from conf import PLUGINDIR

from .settings import PLUGIN_IMPORTDICT
from .settings import PLUGIN_CLASSNAME_REGEX
from .settings import PLUGIN_REGISTER_REGEX
from .settings import PLUGIN_REGISTER_STRING


import sys
import os
import re
import imp
import marshal

conf.plugin = "sqli,reflect_xss"


class PluginManager(object):


    def __init__(self, audit = None):

        self.__audit = audit

        self.__all_fplugin = set()

        #或许所有的插件
        self.__get_all_plugin()

    def set_plugin(self):
        """
        @function 设置载入的plugin
        """
        if conf.plugin is not None:
            if len(conf.plugin.split(",")) > 1:
                for plugin_name in conf.plugin.split(","):
                    retval = self._load_plugin_by_name(plugin_name)
            else:
                plugin_name = conf.plugin
                self._load_plugin_by_name(plugin_name)

        else:
            # all plugin load except infocollect
            conf.pocFile = None

    def _load_plugin_by_name(self, plugin_name):
        try:
            fplugin = self.__get_plugin_by_name(plugin_name)

            plugin_module = plugin_name + PLUGIN_SUFFIX
            retval = self.__load_plugin(plugin_module, fplugin)
            #print retval[plugin_module]

            if retval[plugin_module] != '':
                importer = PluginImporter(plugin_name, retval[plugin_module])
                importer.load_module(plugin_name)

        except LalascanFileNotFoundException,e:
            logger.log_error(str(e))

        except LalascanSystemException,e:
            logger.log_error(str(e))

        except ImportError, ex:
            errmsg = "%s register failed \"%s\"" % (plugin_name, str(ex))
            logger.log_error(errmsg)
            #logger.log(CUSTOM_LOGGING.ERROR, errMsg)

        return

    def __get_plugin_by_name(self, plugin_name):
        for fplugin in self.__all_fplugin:
            try:
                plugin_module = plugin_name + PLUGIN_SUFFIX
                if plugin_module == fplugin[fplugin.rindex('/') + 1:]:
                     return fplugin
            except LalascanValueError:
                pass
        raise LalascanFileNotFoundException("%s plugin not found" % plugin_name)


    def __get_all_plugin(self):
        #for plugin_path in os.walk(PLUGINDIR):
        plugin_path = [plugin for plugin in os.walk(PLUGINDIR)]
        for plugin_folder, folder_list , fplugin_list in plugin_path:
            for each_file in fplugin_list:
                if each_file != '__init__.py' and '.pyc' not in each_file and each_file.endswith(PLUGIN_SUFFIX):
                    self.__all_fplugin.add(os.path.join(plugin_folder, each_file))


    def __load_plugin(self, plugin_name, fplugin):

        try:
            plugin_content = readfile(fplugin)
        except LalascanSystemException:
            raise LalascanSystemException("%s plugin file can not be read" % plugin_name)

        if plugin_content is not None:

            #TODO need check get_accept_type and run method

            if not re.search(PLUGIN_REGISTER_REGEX, plugin_content):
                #not register, plugin is enable

                #className = self.__get_plugin_classname(plugin_content)
                #plugin_content += PLUGIN_REGISTER_STRING.format(className)

                warnmsg = "plugin: %s not register" % plugin_name
                logger.log_warning(warnmsg)
                retval = ''
            else:
                #retval = multiple_replace(plugin_content, PLUGIN_IMPORTDICT)
                retval = plugin_content

        return {plugin_name: retval}


    def __get_plugin_classname(self, poc):
        try:
            className = re.search(PLUGIN_CLASSNAME_REGEX, poc).group(1)
        except:
            className = ""
        return className


class PluginImporter(object):

    """
    Use custom meta hook to import modules available as strings.
    Cp. PEP 302 http://www.python.org/dev/peps/pep-0302/#specification-part-2-registering-hooks
    """

    def __init__(self, fullname, contents):
        self.fullname = fullname
        self.contents = contents

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]

        mod = sys.modules.setdefault(fullname, imp.new_module(fullname))
        mod.__file__ = "<%s>" % fullname
        mod.__loader__ = self
        if False: #conf.isPycFile
            code = marshal.loads(self.contents[8:])
        else:
            code = compile(self.contents, mod.__file__, "exec")
        exec code in mod.__dict__
        return mod

    @classmethod
    def del_module(cls, modname):
        from sys import modules
        try:
            thismod = modules[modname]
        except KeyError:
            raise ValueError(modname)
        these_symbols = dir(thismod)
        del modules[modname]
        for mod in modules.values():
            try:
                delattr(mod, modname)
            except AttributeError:
                pass