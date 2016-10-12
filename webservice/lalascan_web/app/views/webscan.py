#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from flask import Blueprint, url_for, redirect, render_template, request, flash, jsonify
from flask import current_app

from app.services import PolicyService, VulDetailInfo
from app.models.scanner import Scanner
from app.forms import LeakInfoForm
from app.extensions.flask_paginate import Pagination, get_page_args

from app.util import RETCODE


webscan_module = Blueprint('webscan', __name__)

@webscan_module.route('/webscan/', methods = ['GET'])
def index():
    return redirect(url_for('login.login'))


@webscan_module.route('/webscan/scanner', defaults = {'page' : 1})
@webscan_module.route('/webscan/scanner/', defaults = {'page' : 1})
@webscan_module.route('/webscan/scanner/<int:page>')
@webscan_module.route('/webscan/scanner/<int:page>/')
def show_vuldetail(page):
    _scan = VulDetailInfo.get_scan_task()
    all_scan = {}

    _scanner = {}

    for _ in _scan:


        _scan_task = _[0]
        _scan_vul_detail = _[1]
        _leakinfo = _[2]

        single_scan_task = {}
        single_scan_task['scan_task'] = None
        single_scan_task['scan_info'] = []

        if all_scan.has_key(_scan_task.id):
            #scan_info = all_scan[_scan_task.id]['scan_info']
            __ = (_scan_vul_detail, _leakinfo)

            all_scan[_scan_task.id]['scan_info'].append(__)
            all_scan[_scan_task.id] = {'scan_task' : _scan_task, 'scan_info' :all_scan[_scan_task.id]['scan_info']}
            #all_scan[_scan_task.id]['scan_info'].append((_scan_vul_detail, _leakinfo))

            if _leakinfo != None:
                _scanner[_scan_task.id].add_risk_cnt(int(_leakinfo.risk_level))
        else:

            single_scan_task['scan_task'] = _scan_task
            single_scan_task['scan_info'].append((_scan_vul_detail, _leakinfo))

            all_scan[_scan_task.id] = single_scan_task


            scanner = Scanner(audit_name = _scan_task.audit_name,
                              scan_url   = _scan_task.scan_url,
                              starttime  = _scan_task.starttime,
                              finishtime = _scan_task.finishtime,
                              status     = _scan_task.status,
                              )

            if _leakinfo != None:
                scanner.add_risk_cnt(int(_leakinfo.risk_level))

            _scanner[_scan_task.id] = scanner

    print _scanner

    '''
    scanner = Scanner(audit_name = _scan_task.audit_name,
                      scan_url   = _scan_task.scan_url,
                      starttime  = _scan_task.starttime,
                      finishtime = _scan_task.finishtime,
                      status     = _scan_task.status,

                      )



    all_scan_task.append(scan_task)
    '''

    return render_template("/scanner.html", scanner = [p for x , p in _scanner.iteritems()])


@webscan_module.route('/webscan/add_task', methods = ['GET', 'POST'])
def add_task():
    return render_template('/add_task.html')

@webscan_module.route('/webscan/leakinfo', defaults = {'page' : 1})
@webscan_module.route('/webscan/leakinfo/', defaults = {'page' : 1})
@webscan_module.route('/webscan/leakinfo/<int:page>')
@webscan_module.route('/webscan/leakinfo/<int:page>/')
def show_leakinfo(page):

    total = PolicyService.get_leakinfo_cnt()
    page, per_page, offset = get_page_args()

    leakinfo = PolicyService.get_leakinfo(offset, per_page)

    pagination = get_pagination(page=page,
                                per_page=per_page,
                                total=total,
                                record_name='leakinfo',
                                )

    return render_template('/leakinfo.html', leakinfo = leakinfo,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )

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


@webscan_module.route('/webscan/policy', defaults = {'page' : 1})
@webscan_module.route('/webscan/policy/', defaults = {'page' : 1})
@webscan_module.route('/webscan/policy/<int:page>')
@webscan_module.route('/webscan/policy/<int:page>/')
def show_policys(page):
    total = PolicyService.get_policy_cnt()

    page, per_page, offset = get_page_args()
    policys = PolicyService.get_policy_by_leakinfo(offset, per_page)

    pagination = get_pagination(page=page,
                                per_page=per_page,
                                total=total,
                                record_name='policys',
                                )

    return render_template('/policy.html', policy = policys,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


def get_css_framework():
    return current_app.config.get('CSS_FRAMEWORK', 'bootstrap3')

def get_link_size():
    return current_app.config.get('LINK_SIZE', 'sm')

def show_single_page_or_not():
    return current_app.config.get('SHOW_SINGLE_PAGE', False)

def get_pagination(**kwargs):
    kwargs.setdefault('record_name', 'records')
    return Pagination(css_framework=get_css_framework(),
                      link_size=get_link_size(),
                      show_single_page=show_single_page_or_not(),
                      **kwargs
                      )

