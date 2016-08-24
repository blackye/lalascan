#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

import os, datetime, time, urllib, random, hashlib, threading, subprocess
from lib.config import XML_SAVE_PATH
from lib.config import WVS_INSTALL_PATH
from lib.config import WVS_SETTINGS_PATH , WVS_DEFAULT_TEMPLATE
from HTMLParser import HTMLParser
from xml.etree import ElementTree as ET

class WVSSpider(threading.Thread):

    def __init__(self, url, keys, cookie = 'None'):
        super(WVSSpider, self).__init__()
        self.url = url
        self.save_folder_name = keys
        self.cookie = cookie
        
    def _set_crawl_setting_template(self):

        if self.cookie != None:

            default_template_path = os.path.join(WVS_SETTINGS_PATH, WVS_DEFAULT_TEMPLATE)
            tree = ET.parse(default_template_path)
            xml_root_node = tree.getroot()
            cookie_node = xml_root_node.getiterator('CustomCookies')
            if cookie_node != None and len(cookie_node) == 1:
                if cookie_node[0].find('Cookie') == None:
                    ET.SubElement(cookie_node[0], tag = "Cookie", attrib = {"CookieString":"%s" % self.cookie, "Url":"%s" % self.url, "Enabled":"0"})

                    crawl_template_file = os.path.join(WVS_SETTINGS_PATH, self.save_folder_name + '.xml')
                    print crawl_template_file
                    with open(crawl_template_file, 'w') as f:
                        f.write(ET.tostring(xml_root_node))
                        return crawl_template_file

        return None


    def _get_wvs_console_path(self):
        return WVS_INSTALL_PATH

    def get_run_cmd(self):
    	save_folder_path = XML_SAVE_PATH + self.save_folder_name
        if self.cookie != None:
            crawl_template_file = self._set_crawl_setting_template()
            if crawl_template_file is not None:
                return '{0}/wvs_console.exe /Scan {1} /Profile Empty /ExportXML /SaveLogs /Settings {2} /SaveCrawlerData /SaveFolder {3} --EnablePortScanning=False --ManipHTTPHeaders=True'.format(self._get_wvs_console_path(), self.url, self.save_folder_name , save_folder_path)
            else:
                return '{0}/wvs_console.exe /Crawl {1}  /ExportXML /SaveLogs /Settings Default /SaveCrawlerData /SaveFolder {2} --EnablePortScanning=False --ManipHTTPHeaders=True'.format(self._get_wvs_console_path(), self.url, save_folder_path)

        else:
            return '{0}/wvs_console.exe /Crawl {1}  /ExportXML /SaveLogs /Settings Default /SaveCrawlerData /SaveFolder {2} --EnablePortScanning=False --ManipHTTPHeaders=True'.format(self._get_wvs_console_path(), self.url, save_folder_path)

    def run(self):
    	self.__spider_proc = subprocess.Popen(args=self.get_run_cmd(),
                                               stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE,
                                                bufsize=0)
        print self.__spider_proc.stdout.readlines()
		


def main():
	wvs_spider = WVSSpider(url = 'http://www.baidu.com/afdasf', keys = "ff", cookie = 'login=fuck')
	wvs_spider.start()
    


if __name__  == '__main__': main()
