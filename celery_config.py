from celery import Celery
import os

broker_url = os.environ.get('REDIS_URL')

celery = Celery('translation_tasks', broker=broker_url)
celery.conf.update(task_serializer='json', accept_content=['json'], result_serializer='json', timezone='UTC', enable_utc=True)
