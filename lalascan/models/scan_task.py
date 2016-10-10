#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from . import BaseModel

from sqlalchemy import Column, Integer, String, DateTime

class ScanTask(BaseModel):

    __tablename__ = 'scan_task'

    id         = Column(Integer, primary_key = True, autoincrement=True)
    audit_name = Column(String(100), nullable = False)
    scan_url   = Column(String(200), nullable = False)
    starttime  = Column(DateTime, nullable = False)
    finishtime = Column(DateTime)
    user       = Column(String(10))

    def __repr__(self):
        return "<ScanTask(audit_name='%s')>" % self.audit_name