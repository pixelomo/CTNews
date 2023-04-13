from celery import Celery
import os

broker_url = os.environ.get('REDIS_URL')

celery_app = Celery('translation_tasks', broker=broker_url)
celery_app.conf.update(task_serializer='json', accept_content=['json'], result_serializer='json', timezone='UTC', enable_utc=True)
