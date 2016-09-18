import os
from scanui.config import *
basedir = os.path.abspath(os.path.dirname(__file__))

BROKER_URL = "amqp://guest:guest@localhost:5672//"
CELERY_IMPORTS = ("scanui.tasks", )
CELERY_ENABLE_UTC = True
CELERY_RESULT_BACKEND = "mongodb"
CELERY_MONGODB_BACKEND_SETTINGS = {
    "host": MONGO_HOST,
    "port": MONGO_PORT,
    "database": MONGO_DBNAME,
    "taskmeta_collection": "celery_taskmeta",
    }
CELERY_TIMEZONE = 'Europe/Brussels'
