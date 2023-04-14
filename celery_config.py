from celery import Celery
import os
import redis
import ssl

# Get the Redis URL from environment variables
broker_url = os.environ.get('REDIS_URL')

# Parse the URL to extract the different components
parsed_url = redis.Redis.from_url(broker_url)

# Set up the SSL options for the Redis connection
ssl_options = {
    'ssl_cert_reqs': ssl.CERT_NONE,
}

# Create a Celery app with the specified broker URL and SSL options
celery_app = Celery('translation_tasks', broker=broker_url, broker_use_ssl=ssl_options)

# Update Celery app configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)
