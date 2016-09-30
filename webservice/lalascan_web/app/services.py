#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from models.policy import SLeakPolicy
from models.leakinfo import SLeakInfo

from models import db

class PolicyService(object):

    @staticmethod
    def get_policy():
        all_policy = SLeakPolicy.query.order_by("id desc").all()
        return [policy.to_dict() for policy in all_policy]

    @staticmethod
    def get_policy_by_leakinfo():
        policy = db.session.query(SLeakInfo.leak_name_cn, SLeakPolicy).join(SLeakPolicy, SLeakInfo.id == SLeakPolicy.spt_id).order_by(SLeakPolicy.id).all()
        return policy
        #all_policy = SLeakInfo.query.join(SLeakPolicy, SLeakPolicy.id == SLeakInfo.spt_id).order_by(SLeakPolicy.id).all()
        #for item in all_policy:
            #print item.policy_name
            #print 'fuck!!'
            #print item.leak_name_cn

    @staticmethod
    def get_leakinfo():
        all_leakinfo = SLeakInfo.query.order_by("id desc").all()
        return [leakinfo.to_dict() for leakinfo in all_leakinfo]