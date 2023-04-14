from celery import Celery
import os
import ssl

broker_url = os.environ.get('REDIS_URL')

ssl_options = {
    'ssl_cert_reqs': ssl.CERT_NONE,
}

celery_app = Celery('translation_tasks', broker=broker_url, broker_use_ssl=ssl_options)
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

