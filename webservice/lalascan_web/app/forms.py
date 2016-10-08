#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from flask_wtf import Form
from wtforms import StringField, TextField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length

from models.leakinfo import SLeakInfo

class LeakInfoForm(Form):
    leak_name    = StringField('leak_name', validators = [DataRequired('leak_name'), Length(max=100)])
    leak_name_cn = StringField('leak_name_cn', validators = [DataRequired('leak_name_cn'), Length(max=100)])

    spt          = IntegerField('spt', validators = [DataRequired('spt')])
    description  = TextField('description', validators = [DataRequired('description')])
    risk_level   = IntegerField('risk_level')

    '''
    def validate(self):
        check_validate = super(LeakInfoForm, self).validate()

        print check_validate
        if not check_validate:
            print '2222'
            return False
        print '1111'
        bret = SLeakInfo.query.filter_by(leak_name = self.leak_name.data).first()
        if bret:
            return False
    '''


