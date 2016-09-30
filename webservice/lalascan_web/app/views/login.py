#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from flask import Blueprint, url_for, redirect


login_module = Blueprint('login', __name__)

@login_module.route('/cloudscan', methods = ['GET'])
def index():
    return redirect(url_for('login.login'))

@login_module.route('/cloudscan/login', methods = ['GET', 'POST'])
def login():
    return 'hello world!'
