from celery import Celery
from scanui import celeryconfig
from scanui.config import *
celery_pipe = Celery()
celery_pipe.conf.update(BROKER_URL = "amqp://guest:guest@localhost:5672//",
CELERY_IMPORTS = ("scanui.tasks", ),
CELERY_ENABLE_UTC = True,
CELERY_RESULT_BACKEND = "mongodb",
CELERY_MONGODB_BACKEND_SETTINGS = {
    "host": MONGO_HOST,
    "port": MONGO_PORT,
    "database": MONGO_DBNAME,
    "taskmeta_collection": "celery_taskmeta",
    },
CELERY_TIMEZONE = 'Europe/Brussels',
)
