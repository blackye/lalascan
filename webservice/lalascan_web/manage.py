#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from flask.ext.script import Manager, Server
from app import create_app

import os

env = os.environ.get('WEBAPP_ENV', 'config')
app = create_app(env)
manager = Manager(app)
manager.add_command("runserver", Server(use_debugger = True,
                                        use_reloader = True,
                                        host = '172.16.203.129', port = 8080))


if __name__ == '__main__':
    manager.run()