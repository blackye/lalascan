#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from lalascan.api.exception import LalascanNotImplementedError
from conf import DB_MYSQL_HOST, DB_MYSQL_USER, DB_MYSQL_PWD, DB_MYSQL_PORT, DB_MYSQL_DATABASE

from thirdparty_libs.torndb import Connection

class BaseDB(object):

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def query(self):
        raise LalascanNotImplementedError("Subclasses MUST implement this method! Method:execute")

    def close(self):
        raise LalascanNotImplementedError("Subclasses MUST implement this method! Method:close")


class AuditMysqlDB(BaseDB):

    #====================
    def __init__(self):
        self.auditdb = Connection( host = DB_MYSQL_HOST, user = DB_MYSQL_USER, password = DB_MYSQL_PWD, database = DB_MYSQL_DATABASE)


    def __initdb(self):
        pass


    def query(self, sql):
        return self.auditdb.query(sql)

    def get_alldata(self, audit_table, **kwargs):
        if kwargs is not None:
            condition = '1 = 1'
            for table_column, content in kwargs.iteritems():
                condition += " and `%s` = '%s'" % (table_column, content)
            sql = "select * from %s where %s" % (audit_table, condition)
        else:
            sql = "select * from %s" % audit_table

        return self.auditdb.query(sql)

    def close(self):
        self.auditdb.close()