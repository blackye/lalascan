#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'


from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class STarget(db.Model):

    __tablename__ = 'spider_target'

    id = db.Column(db.Integer(), primary_key = True)
    starturl = db.Column(db.String(255))
    starttime = db.Column(db.String(255))

    '''
    @classmethod
    def query(cls):
        return cls.query.all()
    '''