import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = '973fb5503d479a2ccd1ce8b4227bdd3c'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@127.0.0.1:3306/lalascan'

# mongodb config
MONGO_DBNAME = 'nmapuidb'
MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_USERNAME = ''
MONGO_PASSWORD = ''

#mysql config
MYSQL_DBNAME   = "lalascan"
MYSQL_HOST     = '127.0.0.1'
MYSQL_PORT     = 3306
MYSQL_USERNAME = 'root'
MYSQL_PWD      = ''


# File upload config
UPLOAD_FOLDER = basedir + 'scanui/uploads'
ALLOWED_EXTENSIONS= set(['xml'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# nmap-webgui specific config variables
ROLE_USER = 2
ROLE_ADMIN = 4
