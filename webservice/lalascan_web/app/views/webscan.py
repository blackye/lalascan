#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from flask import Blueprint, url_for, redirect, render_template

from app.services import PolicyService


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

@webscan_module.route('/webscan/policy', methods = ['GET', 'POST'])
def show_policys():
    #policys = PolicyService.get_policy()
    policys = PolicyService.get_policy_by_leakinfo()
    return render_template('/policy.html', policy = policys)