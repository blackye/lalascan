#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from . import db

class STarget(db.Model):

    __tablename__ = 'scan_task'

    id = db.Column(db.Integer(), primary_key = True, autoincrement=True)
    audit_name = db.Column(db.String(100), nullable = False)
    scan_url   = db.Column(db.String(200), nullable = False)
    starttime  = db.Column(db.DateTime, nullable = False)
    finishtime = db.Column(db.DateTime, nullable = False)
    status     = db.Column(db.Integer)
    user       = db.Column(db.String(10))

    def to_dict(self):
        return dict(
            id = self.id,
            audit_name = self.audit_name,
            scan_url = self.scan_url,
            starttime = self.starttime,
            finishtime = self.finishtime,
            user = self.user
        )


class SVulDetail(db.Model):

    __tablename__  = 'scan_vul_detail'

    id = db.Column(db.Integer(), primary_key = True, autoincrement=True)
    st_id = db.Column(db.Integer(), primary_key = True)
    sli_id = db.Column(db.Integer(), nullable = False)
    url = db.Column(db.Text, nullable = False)
    vulparam_point = db.Column(db.String(10), nullable = False)
    method      = db.Column(db.String(5))
    payload     = db.Column(db.Text)
    get_param   = db.Column(db.Text)
    post_param  = db.Column(db.Text)
    ori_req_header = db.Column(db.Text)
    ori_resp_header = db.Column(db.Text)
    ori_resp_body = db.Column(db.Text)
    insert_time = db.Column(db.DateTime)



class Scanner(object):

    def __init__(self, **kwargs):
        self.scan_url = kwargs.get('scan_url', None)
        self.audit_name = kwargs.get('audit_name', None)
        self.starttime = kwargs.get('starttime', None)
        self.finishtime = kwargs.get('finishtime', None)
        self.status = kwargs.get('status', None)

        self.risk_cnt = kwargs.get('high_cnt', {})

        self.high_risk_cnt = 0
        self.middle_risk_cnt = 0
        self.low_risk_cnt = 0
        self.info_risk_cnt = 0

    def add_risk_cnt(self, risk_level):
        if risk_level == 4:
            self.high_risk_cnt += 1
        elif risk_level == 3:
            self.middle_risk_cnt += 1
        elif risk_level == 2:
            self.low_risk_cnt += 1
        elif risk_level == 1:
            self.info_risk_cnt += 1


