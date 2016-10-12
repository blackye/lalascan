#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from . import BaseModel

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.dialects.mysql.base import LONGTEXT

class ScanVulDetail(BaseModel):

    __tablename__ = 'scan_vul_detail'

    id              = Column(Integer, primary_key = True, autoincrement=True)
    st_id           = Column(Integer, nullable = False)
    sli_id          = Column(Integer, nullable = False)
    url             = Column(Text, nullable = False)
    vulparam_point  = Column(String(10))
    method          = Column(String(5))
    payload         = Column(Text, nullable = False)
    get_param       = Column(Text)
    post_param      = Column(Text)
    ori_req_header  = Column(Text)
    ori_resp_header = Column(Text)
    ori_resp_body   = Column(LONGTEXT)
    insert_time     = Column(DateTime, nullable = False)

    def __repr__(self):
        return "<ScanVulDetail(url='%s')>" % self.url