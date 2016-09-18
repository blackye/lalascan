__author__ = 'Ronald Bister'
__email__ =  'mini.pelle@gmail.com'
__license__ = 'CC-BY'
__version__ = '0.1'

from flask import Flask
from scanui import config
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
import datetime

app = Flask(__name__)
app.config.from_object(config)

mysqldb = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "loginui.login"

from scanui.views import login
from scanui.views import scan
app.register_blueprint(login.appmodule)
app.register_blueprint(scan.appmodule)

def unix2datetime(unixstr):
    _rstr = ''
    try:
        _dtime = datetime.datetime.fromtimestamp(int(unixstr))
        _rstr = _dtime.strftime('%d/%m/%Y %H:%M:%S')
    except ValueError:
        _rstr = 'Unknown'
    return _rstr

app.jinja_env.filters['unix2datetime'] = unix2datetime

if __name__ == '__main__':
    app.run()
