# GPTelegraph

Our editors use ChatGPT to translate articles from Cointelegraph into Japanese. Since it takes a few minutes for the translation to process we would like to automate translations so editors can review and edit faster. We require an app which checks the Cointelegraph RSS feed https://cointelegraph.com/rss every hour. If there are new articles it will scrape the content (including links) and save it to a database. Next, it will call the OpenAI API to request translation. Once processed this will also be saved to the database. When editors open the app they will be able to select any article and view both the original and translated articles. The translated article will be inside a WYSIWYG. There will also be a link to the original article page.

## Tree

- Aptfile
- Procfile
- README.md
- __init__.py
- app.py
- articles/__init__.py
- articles/items.py
- articles/pipelines.py
- articles/settings.py
- articles/spiders/__init__.py
- articles/spiders/articles.py
- articles/spiders/run_spider.py
- celery_app.py
- dummy_data.json
- favicon.ico
- init_db.py
- remove_duplicates.py
- requirements.txt
- runtime.txt
- scrapinghub.yml
- scrapy.cfg
- setup.py
- static/main.js
- templates/index.html
- templates/layout.html
- translate.py
- translation_tasks.py

## Useful commands

### Get db schema
- SELECT column_name, data_type, is_nullable
- FROM information_schema.columns
- WHERE table_name = 'article';

### Heroku
- heroku logs --tail --app gentle-earth-02543
- heroku builds -a gentle-earth-02543
- heroku builds:cancel build-ID -a gentle-earth-02543
- heroku pg:killall
- heroku config:set OPENAI_API_KEY=key -a gentle-earth-02543
- heroku run:detached -t python remove_duplicates.py -a gentle-earth-02543
- heroku ps:scale worker=0 --app gentle-earth-02543

### switch between development/production
- export FLASK_DEBUG=0
- export FLASK_DEBUG=1

