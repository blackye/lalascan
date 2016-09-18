#from libnmap.parser import NmapParser, NmapParserException
from scanui.celeryapp import celery_pipe
from scanui import mysqldb
import hashlib

'''
class Users(object):
    @classmethod
    def find(cls, **kwargs):
        _users = []
        _dbusers = mysqldb.db.users.find(kwargs)
        for _dbuser in _dbusers:
            _users.append(User(id=_dbuser['_id'],
                               username=_dbuser['username'],
                               password=_dbuser['password'],
                               email=_dbuser['email']))
        return _users

    @classmethod
    def get(cls, user_id):
        _user = None
        if isinstance(user_id, unicode):
            user_id = ObjectId(user_id)

        if isinstance(user_id, ObjectId):
            _dbuser = mongo.db.users.find_one({'_id': user_id})
            _user = User(id=_dbuser['_id'],
                         username=_dbuser['username'],
                         password=_dbuser['password'],
                         email=_dbuser['email'])
        return _user

    @classmethod
    def add(cls, username=None, email=None, password=None):
        rval = False
        if username is not None and email is not None and password is not None:
            mongo.db.users.insert({'username': username,
                                   'email': email,
                                   'password': password})
            rval = True
        return rval

class User:
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.password = password
        self.email = email

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
      return False
    
    def get_id(self):
        return unicode(self.id)

    def credentials_valid(self, _password):
        return hashlib.sha256(_password).hexdigest() == self.password

    def __repr__(self):
        return "<User {0}>".format(self.username)


class NmapTask(object):
    @classmethod
    def find(cls, **kwargs):
        _reports = []
        _dbreports = mongo.db.reports.find(kwargs)
        for _dbreport in _dbreports:
            _nmap_task = celery_pipe.AsyncResult(_dbreport['task_id'])
            _reports.append(_nmap_task)
            
        return _reports

    @classmethod
    def get(cls, task_id):
        _report = None
        if isinstance(task_id, str) or isinstance(task_id, unicode):
            try:
                _resultdict = celery_pipe.AsyncResult(task_id).result
            except NmapParserException:
                pass
        return _resultdict

    @classmethod
    def get_report(cls, task_id):
        _report = None
        if isinstance(task_id, str) or isinstance(task_id, unicode):
            try:
                _resultdict = celery_pipe.AsyncResult(task_id).result
                _resultxml = _resultdict['report']
                _report = NmapParser.parse_fromstring(_resultxml)
            except NmapParserException:
                pass
        return _report

    @classmethod
    def add(cls, user_id=None, task_id=None):
        rval = False
        if user_id is not None and task_id is not None:
            mongo.db.reports.insert({'user_id': user_id, 'task_id': task_id})
            rval = True
        return rval
'''

class Users(object):

    pass