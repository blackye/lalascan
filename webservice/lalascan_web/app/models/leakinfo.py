#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from . import db

class SLeakInfo(db.Model):


    __tablename__ = 'scan_leak_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    spt_id = db.Column(db.Integer, nullable = False)
    leak_name = db.Column(db.String(100), nullable = False)
    leak_name_cn = db.Column(db.String(100), nullable = False)
    description = db.Column(db.Text())
    risk_level = db.Column(db.Integer)

    def to_dict(self):

        return dict(
            id = self.id,
            spt_id = self.spt_id,
            leak_name = self.leak_name,
            leak_name_cn = self.leak_name_cn,
            description = self.description,
            risk_level = self.risk_level,
        )

class SPluginType(db.Model):

    __tablename__ = 'scan_plugin_type'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable = False)
    description = db.Column(db.Text())

