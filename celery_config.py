from dotenv import load_dotenv
from celery import Celery
import os
import ssl
import redis

load_dotenv()
REDIS_URL = os.environ.get('REDIS_URL')

# Create a Redis connection using SSL
redis_conn = redis.Redis.from_url(
    REDIS_URL,
    ssl_cert_reqs=ssl.CERT_NONE,
)

ssl_options = {
    'ssl_cert_reqs': ssl.CERT_NONE,
}

celery_app = Celery('translation_tasks', broker=REDIS_URL, broker_use_ssl=ssl_options)
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)
