#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from HTMLParser import HTMLParser
from xml.etree import ElementTree
import MySQLdb
import time, sys, os, json, redis, re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

SPIDER_TARGET     = 'spider_target'
SPIDER_SITE_FILES = 'spider_site_files'
SPIDER_PARM       = 'spider_parameter'
SPIDER_PARM_TYPES = 'spider_parm_types'

MYSQL_HOST      = '172.16.203.129'
MYSQL_PORT      = 3306
MYSQL_USER      = 'root'
MYSQL_PWD       = 'root'
MYSQL_DB        = 'luscan_spider'

CRAWL_FILENAME  = 'export.xml'
REDIS_SERVER    = '10.133.6.20'

class MySQLBase(object):
    u'''对MySQLdb常用函数进行封装的类'''

    error_code = '' #MySQL错误号码

    _instance = None #本类的实例
    _conn = None # 数据库conn
    _cur = None #游标

    _TIMEOUT = 30 #默认超时30秒
    _timecount = 0

    def __init__(self, dbconfig):
        u'构造器：根据数据库连接参数，创建MySQL连接'
        try:
            self._conn = MySQLdb.connect(host=dbconfig['host'],
                                         port=dbconfig['port'],
                                         user=dbconfig['user'],
                                         passwd=dbconfig['passwd'],
                                         db=dbconfig['db'])
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            error_msg = 'MySQL error! ', e.args[0], e.args[1]
            print error_msg
            sys.exit()
            
        self._cur = self._conn.cursor()
        self._instance = MySQLdb

    def query(self,sql):
        u'执行 SELECT 语句'
        try:
            self._cur.execute("SET NAMES utf8")
            result = self._cur.execute(sql)
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            print "数据库错误代码:",e.args[0],e.args[1]
            result = False
        return result

    def update(self,sql):
        u'执行 UPDATE 及 DELETE 语句'
        try:
            self._cur.execute("SET NAMES utf8")
            result = self._cur.execute(sql)
            self._conn.commit()
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            print "数据库错误代码:",e.args[0],e.args[1]
            result = False
        return result

    def insert(self,sql):
        u'执行 INSERT 语句。如主键为自增长int，则返回新生成的ID'
        try:
            self._cur.execute("SET NAMES utf8")
            self._cur.execute(sql)
            insert_id = self._conn.insert_id()
            self._conn.commit()
            return insert_id
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            print "数据库错误代码:",e.args[0],e.args[1]
            return -1

    def fetchAllRows(self):
        u'返回结果列表'
        return self._cur.fetchall()

    def fetchOneRow(self):
        u'返回一行结果，然后游标指向下一行。到达最后一行以后，返回None'
        return self._cur.fetchone()

    def getRowCount(self):
        u'获取结果行数'
        return self._cur.rowcount

    def commit(self):
        u'数据库commit操作'
        self._conn.commit()

    def rollback(self):
        u'数据库回滚操作'
        self._conn.rollback()

    def __del__(self):
        u'释放资源（系统GC自动调用）'
        try:
            self._cur.close()
            self._conn.close()
        except:
            pass

    def  close(self):
        u'关闭数据库连接'
        self.__del__()


class CrawlDB(MySQLBase):

    def __init__(self):
        MySQLBase.__init__(self, {'host':MYSQL_HOST, 'port':MYSQL_PORT, 'user':MYSQL_USER, 'passwd': MYSQL_PWD, 'db':MYSQL_DB})


class CrawlFileMonitor(FileSystemEventHandler):

    def __init__(self):
        super(CrawlFileMonitor, self).__init__()
        #self.crawl_log_path = crawl_log_path

    def on_created(self, event):
        super(CrawlFileMonitor, self).on_created(event)
        if not event.is_directory:
            #print event.src_path
            if CRAWL_FILENAME in event.src_path:
                print '[+] wait crawl xml file writing...'
                while True:
                    try:
                        open(event.src_path, "r").read(5)
                        print '[+] spider xml file write finish!'
                        crawlxml = CrawlXML(event.src_path)
                        crawlxml.xml2mysql()
                        break
                    except IOError:
                        time.sleep(2) # need file write finish
                

class CrawlXML(object):
    '''
    crawl xml解析类
    '''

    def __init__(self, filepath = CRAWL_FILENAME):
        self.filepath = filepath
        self.xml_root_node = ElementTree.fromstring(open(self.filepath).read())
        self.xml_object = {}
        self.domain_node_tagname   = 'Crawler'
        self.domain_node_attrib    = 'StartUrl'
        self.sitefile_node_tagname = 'SiteFile'
        self.crawldb = CrawlDB()


    def xml_unescape(self, content):
        h = HTMLParser()
        return h.unescape(content)

    def __get_node_text(self, node):
        '''
        获取节点的文本内容
        :param node:
        :return:
        '''
        return node.text

    def __get_node_tag(self, node):
        '''
        获取节点的标签值
        :param node:
        :return:
        '''
        return node.tag

    def __get_domain(self):
        starturl_node = self.xml_root_node.getiterator(self.domain_node_tagname)
        if len(starturl_node) == 1:
            if starturl_node[0].attrib.has_key(self.domain_node_attrib):
                self.xml_object['domain'] = starturl_node[0].attrib[self.domain_node_attrib]

    def _parse_domain(self):
        '''
        TODO need find the right path
        '''
        return os.path.split(os.path.split(self.filepath)[0])[1]
        
            

    def __get_sitefile_object(self):
        sitefile_arr = []
        sitefiles_nodes = self.xml_root_node.getiterator(self.sitefile_node_tagname)
        for site_node in sitefiles_nodes:
            sitefile_item = {}
            name_node_text     = self.__get_node_text(site_node.find('Name'))    #name: user.do
            nameurl_node_text  = self.__get_node_text(site_node.find('URL'))    #URL: /user.do
            fullurl_node_text  = self.__get_node_text(site_node.find('FullURL'))  #FullUrl: http://xxxxx.com/user.do
            sitefile_item['name'] = name_node_text
            sitefile_item['nameurl'] = nameurl_node_text
            sitefile_item['fullurl'] = fullurl_node_text

            #---------get all url and parameter ----------
            all_cgi_nodes = site_node.getiterator('Variation')
            sitefile_item['content'] = []
            for cgi_node in all_cgi_nodes:
                cgiinfo_dict = {}
                cgiinfo_dict['url'] = self.__get_node_text(cgi_node.find('URL'))
                param_data = self.__get_node_text(cgi_node.find('PostData'))
                cgiinfo_dict['param_data'] = self.xml_unescape(param_data) if param_data is not None else ''
                cgiinfo_dict['method']     = 'POST' if param_data is not None else 'GET'
                sitefile_item['content'].append(cgiinfo_dict)

            sitefile_arr.append(sitefile_item)

        self.xml_object['info'] = sitefile_arr


    def xml2mysql(self):
        self.__get_domain()
        print self.xml_object
        self.__get_sitefile_object()
        print self.xml_object
        '''
         ------------
         push redis
        '''
        pool = redis.ConnectionPool(host = REDIS_SERVER, port = '6379', db =0)
        redis_conn = redis.Redis(connection_pool = pool)
        redis_conn.set(self._parse_domain(), json.dumps(self.xml_object))
        
        print 'Domain:%s' % self.xml_object['domain']

        cur_time = time.strftime( '%Y-%m-%d %X', time.localtime( time.time() ) )
        sql = "insert into %s(`starturl`, `starttime`, `finishtime`) values('%s', '%s', '%s')" % (SPIDER_TARGET, self.xml_object['domain'], cur_time, cur_time)
        id = self.crawldb.insert(sql)
       
        sfid = 0
        for item in self.xml_object['info']:
            print '-----------------'
            print 'Name:%s' % item['name']
            print 'nameurl:%s' % item['nameurl']
            print 'fullurl:%s' % item['fullurl']
            sql = "insert into %s values('%d', '%d', '%s', '%s', '%s')" % (SPIDER_SITE_FILES, id, sfid, item['name'], item['nameurl'], item['fullurl'])
            print sql
            if self.crawldb.insert(sql) == -1:
                print '[-] spider_site_files insert data Mysql Error! error_code:%s sql:%s' % (self.crawldb.error_code, sql)
            else:
                schemeid = 0
                for each_cgi in item['content']:
                    print 'Cgi:%s' % each_cgi['url']
                    print 'Parm:%s' % each_cgi['param_data']
                    print 'Method:%s' % each_cgi['method']
                    sql = "insert into %s values('%d', '%d', '%d', '%s', '%s', '%s')" % (SPIDER_PARM, id, sfid, schemeid, each_cgi['url'], each_cgi['param_data'],  each_cgi['method'])

                    if self.crawldb.insert(sql) == -1:
                        print '[-] spider_parameter insert data Mysql Error! sql:%s' % sql
                    schemeid = schemeid + 1
            sfid = sfid + 1

        print '[+] %s crawl success!' % self.xml_object['domain']

def monitor(path):
    event_handler = CrawlFileMonitor()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def main():
    #crawlxml = CrawlXML('/Users/BlackYe_Mac/worktools/export.xml')
    #crawlxml.analyse()
    monitor('D:/spider_db/')
    
if __name__  == '__main__':
    main()
