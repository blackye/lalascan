#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from . import db

from datetime import datetime


class SLeakPolicy(db.Model):

    __tablename__ = 'scan_leak_policy'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sli_id = db.Column(db.Integer, nullable = False)
    spt_id = db.Column(db.Integer, nullable = False)
    policy_name = db.Column(db.String(50), nullable = False)
    content = db.Column(db.Text())
    insert_time = db.Column(db.DateTime, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Integer, default = 1)

    def to_dict(self):
        return dict(
            id = self.id,
            sli_id = self.sli_id,
            spt_id = self.spt_id,
            policy_name = self.policy_name,
            content = self.content,
            insert_time = self.insert_time,
            update_time = self.update_time,
            status = self.status
        )