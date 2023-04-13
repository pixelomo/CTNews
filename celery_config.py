from celery import Celery
import os

broker_url = os.environ.get('REDIS_URL')

celery = Celery('translation_tasks', broker=broker_url)
