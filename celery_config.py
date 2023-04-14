from celery import Celery
import os
import ssl  # Add this import

broker_url = os.environ.get('REDIS')

celery_app = Celery('translation_tasks', broker=broker_url)
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    broker_use_ssl={'ssl_cert_reqs': ssl.CERT_NONE}  # Add this line
)
