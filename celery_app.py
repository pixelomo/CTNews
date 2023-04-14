from dotenv import load_dotenv
from celery import Celery
import os
import ssl

load_dotenv()

redis_url = os.environ.get("REDIS_URL")

celery_app = Celery('translation_tasks', broker=redis_url, backend=redis_url)
celery_app.conf.update(
    broker_use_ssl={
        'ssl_cert_reqs': ssl.CERT_NONE,
        'keyfile': None,
        'certfile': None,
        'ca_certs': None,
    },
    redis_backend_use_ssl={
        'ssl_cert_reqs': ssl.CERT_NONE,
        'keyfile': None,
        'certfile': None,
        'ca_certs': None,
    },
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)
