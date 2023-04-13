import json
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from translation_tasks import perform_translation
from celery_config import app as celery_app
from datetime import datetime
from dateutil.parser import parse
from sqlalchemy.exc import IntegrityError
from flask import render_template
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from tasks import save_article

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL', 'sqlite:///articles.db').replace('postgres://', 'postgresql://')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

@app.route('/api/translate', methods=['POST'])
def translate():
    text = request.form.get('text')
    target_language = request.form.get('target_language')

    translation_task = perform_translation.delay(text, target_language)
    return jsonify({"task_id": translation_task.id})

@app.route('/api/translate_status/<task_id>', methods=['GET'])
def translate_status(task_id):
    task = celery_app.AsyncResult(task_id)
    return jsonify({"status": task.status, "result": task.result})

def load_dummy_data():
    with open('dummy_data.json', 'r') as file:
        raw_data = json.load(file)

    data = []
    for article in raw_data["values"]:
        formatted_article = {
            "id": article[0],
            "title": article[1],
            "pubDate": article[2],
            "link": article[3],
            "text": article[4],
            "html": article[5],
            "content_translated": article[6]
        }
        data.append(formatted_article)

    return data

@app.route('/api/get_dummy_data')
def get_dummy_data():
    if os.environ.get('FLASK_ENV') == 'development':
        return jsonify(load_dummy_data())
    else:
        return jsonify({"error": "Dummy data is only available in development environment"})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    pubDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    link = db.Column(db.String, nullable=False, unique=True)
    text = db.Column(db.Text, nullable=True)
    html = db.Column(db.Text, nullable=True)
    content_translated = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "pubDate": self.pubDate.isoformat(),
            "link": self.link,
            "text": self.text,
            "html": self.html,
            "content_translated": self.content_translated,
        }

class SaveArticleResource(Resource):
    def post(self):
        data = request.get_json()
        save_article_task = save_article.delay(data)
        return {"task_id": save_article_task.id}

class GetAllArticlesResource(Resource):
    def get(self):
        articles = Article.query.all()
        return jsonify([article.to_dict() for article in articles])

api.add_resource(SaveArticleResource, "/api/save_article")
api.add_resource(GetAllArticlesResource, "/api/get_all_articles")

def run_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl('articles')
    process.start()

@app.before_first_request
def start_spider_on_deploy():
    run_spider()

if __name__ == '__main__':
    if os.environ.get('FLASK_ENV') == 'development':
        dummy_data = load_dummy_data()
    app.run(debug=True)