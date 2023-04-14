from dotenv import load_dotenv
from celery import Celery
import os
import ssl
import redis

load_dotenv()
REDIS_URL = redis.from_url(os.environ.get("REDIS_URL"))

ssl_options = {
    'ssl_cert_reqs': None,
}

celery_app = Celery('translation_tasks', broker=REDIS_URL, broker_use_ssl=ssl_options)
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)


