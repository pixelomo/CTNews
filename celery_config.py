from flask import Flask
from celery import Celery
import os

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = os.environ.get('REDIS_URL')
app.config['CELERY_RESULT_BACKEND'] = os.environ.get('REDIS_URL')

celery = Celery('translation_tasks', broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
