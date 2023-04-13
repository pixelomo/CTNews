# celery_config.py
from flask import Flask
from celery import Celery
import os

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = os.environ.get('REDIS_URL')
app.config['CELERY_RESULT_BACKEND'] = os.environ.get('REDIS_URL')

# In celery_config.py
celery = Celery('translation_tasks', broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

app = Celery('translation_tasks', broker=os.environ['REDIS_URL'])
