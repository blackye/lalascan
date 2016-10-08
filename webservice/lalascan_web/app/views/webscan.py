#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from flask import Blueprint, url_for, redirect, render_template, request, flash, jsonify


from app.services import PolicyService
from app.forms import LeakInfoForm

from app.util import RETCODE


webscan_module = Blueprint('webscan', __name__)

@webscan_module.route('/webscan/', methods = ['GET'])
def index():
    return redirect(url_for('login.login'))

@webscan_module.route('/webscan/scanner', methods = ['GET', 'POST'])
def scanner():
    return render_template("/scanner.html")

@webscan_module.route('/webscan/add_task', methods = ['GET', 'POST'])
def add_task():
    return render_template('/add_task.html')

@webscan_module.route('/webscan/leakinfo', methods = ['GET', 'POST'])
def show_leakinfo():
    leakinfo = PolicyService.get_leakinfo()
    return render_template('/leakinfo.html', leakinfo = leakinfo)

@webscan_module.route('/webscan/add_leakinfo')
def add_leakinfo():
    plugin_type = PolicyService.get_plugin_type()
    return render_template('/add_leakinfo.html', plugin_type = plugin_type)

@webscan_module.route('/webscan/leak_add', methods = ['GET', 'POST'])
def leak_add():
    leakinfo_form = LeakInfoForm(request.form)

    if leakinfo_form.validate_on_submit():
        return redirect('/add_leakinfo')

    if request.method == 'GET':
        return redirect(url_for('webscan.add_leakinfo'))

    if request.method == 'POST':
        leak_name    = leakinfo_form.leak_name.data
        leak_name_cn = leakinfo_form.leak_name_cn.data
        spt          = leakinfo_form.spt.data
        description  = leakinfo_form.description.data
        risk_level   = leakinfo_form.risk_level.data

        PolicyService.add_leakinfo(leak_name = leak_name, leak_name_cn = leak_name_cn, spt = spt, description = description, risk_level = risk_level)

        return redirect(url_for('webscan.show_leakinfo'))

@webscan_module.route('/webscan/del_leakinfo', methods = ['GET', 'POST'])
def delete_leakinfo():
    leak_id = request.args.get('leak_id')

    PolicyService.del_leakinfo(leak_id)
    return jsonify(status = RETCODE.SUCCESS , info = 'success', data = None)


@webscan_module.route('/webscan/policy', methods = ['GET', 'POST'])
def show_policys():
    #policys = PolicyService.get_policy()
    policys = PolicyService.get_policy_by_leakinfo()
    return render_template('/policy.html', policy = policys)



