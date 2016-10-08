#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from models.policy import SLeakPolicy
from models.leakinfo import SLeakInfo
from models.leakinfo import SPluginType

from models import db

class PolicyService(object):

    @staticmethod
    def get_policy():
        all_policy = SLeakPolicy.query.order_by("id desc").all()
        return [policy.to_dict() for policy in all_policy]

    @staticmethod
    def get_policy_by_leakinfo():
        return db.session.query(SLeakInfo.leak_name_cn, SLeakPolicy).join(SLeakPolicy, SLeakInfo.id == SLeakPolicy.spt_id).order_by(SLeakPolicy.id).all()

    @staticmethod
    def get_leakinfo():
        all_leakinfo = db.session.query(SPluginType.name, SLeakInfo).join(SLeakInfo, SLeakInfo.spt_id == SPluginType.id).order_by(SLeakInfo.id.desc()).all()
        return [leakinfo[1].to_dict(plugin_type = leakinfo[0]) for leakinfo in all_leakinfo]

    @staticmethod
    def get_plugin_type():
        all_plugin_type = SPluginType.query.all()
        return [plugin_type.get_plugin_name() for plugin_type in all_plugin_type]


    @staticmethod
    def add_leakinfo(**kwargs):
        sleakinfo = SLeakInfo(leak_name = kwargs['leak_name'],
                              leak_name_cn = kwargs['leak_name_cn'],
                              spt_id = kwargs['spt'],
                              description = kwargs['description'],
                              risk_level = kwargs['risk_level'],
                              fix_content = None)

        db.session.add(sleakinfo)
        db.session.commit()
        return sleakinfo.to_dict()

    @staticmethod
    def del_leakinfo(leak_id):
        leakinfo = SLeakInfo.query.get(leak_id)
        db.session.delete(leakinfo)
        db.session.commit()