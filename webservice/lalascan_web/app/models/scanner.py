#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from . import db

class STarget(db.BaseModel):

    __tablename__ = 'spider_target'

    id = db.Column(db.Integer(), primary_key = True)
    starturl = db.Column(db.String(255))
    starttime = db.Column(db.String(255))

    '''
    @classmethod
    def query(cls):
        return cls.query.all()
    '''

