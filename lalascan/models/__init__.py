#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from lalascan.libs.core.singletonclass import Singleton
from conf import DB_MYSQL_HOST, DB_MYSQL_USER, DB_MYSQL_PORT, DB_MYSQL_PWD, DB_MYSQL_DATABASE

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class _DBConfig(Singleton):

    def __init__(self, max_overflow = 10):
        conn = "mysql+pymysql://{0}@{1}:{2}/{3}?charset=utf8".format(DB_MYSQL_USER, DB_MYSQL_HOST, DB_MYSQL_PORT, DB_MYSQL_DATABASE)
        engine  = create_engine(conn, max_overflow = max_overflow)
        Session = sessionmaker(bind=engine)

        self.session = Session()

BaseModel = declarative_base()
