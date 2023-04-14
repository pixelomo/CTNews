web: gunicorn --bind 0.0.0.0:$PORT app:app
worker: scrapy crawl articles
celery_worker: -A celery_app worker --loglevel=info
release: python -m articles.spiders.run_spider
