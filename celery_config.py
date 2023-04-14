from dotenv import load_dotenv
from celery import Celery
import os
import redis
from urllib.parse import urlparse

from translation_tasks import perform_translation  # Add this line

load_dotenv()
REDIS_URL = os.environ.get("REDIS_URL")
url = urlparse(REDIS_URL)

ssl_options = {
    'ssl_cert_reqs': None,
}

redis_url_with_ssl = f'redis://{url.username}:{url.password}@{url.hostname}:{url.port}/0'

celery_app = Celery('translation_tasks', broker=redis_url_with_ssl, backend=REDIS_URL, broker_use_ssl=ssl_options)
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)
