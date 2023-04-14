from dotenv import load_dotenv
from celery import Celery
import os

load_dotenv()

REDIS_URL = os.environ.get("REDIS_URL")

celery_app = Celery('translation_tasks', broker=REDIS_URL, backend=REDIS_URL)
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    broker_use_ssl=True,
    result_backend_use_ssl=True,
)
