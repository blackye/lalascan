#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'


from flask import Flask
from flask.ext.login import LoginManager

from models import db

def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'login.login'

    from app.views import login
    from app.views import webscan
    app.register_blueprint(login.login_module)
    app.register_blueprint(webscan.webscan_module)

    return app