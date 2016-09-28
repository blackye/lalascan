#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from flask import Blueprint, url_for, redirect, render_template


webscan_module = Blueprint('webscan', __name__)

@webscan_module.route('/webscan/', methods = ['GET'])
def index():
    return redirect(url_for('login.login'))

@webscan_module.route('/webscan/scanner', methods = ['GET', 'POST'])
def scanner():
    return render_template("/scanner.html")