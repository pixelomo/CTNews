from dotenv import load_dotenv
from celery import Celery
import os
import redis
from urllib.parse import urlparse

load_dotenv()

url = urlparse(os.environ.get("REDIS_URL"))
r = redis.Redis(host=url.hostname, port=url.port, password=url.password, ssl=True, ssl_cert_reqs=None)

celery_app = Celery('translation_tasks', broker=r)
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)
