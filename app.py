import json
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dateutil.parser import parse
from sqlalchemy import Column, String
from sqlalchemy.exc import IntegrityError
from flask import render_template
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL', 'sqlite:///articles.db').replace('postgres://', 'postgresql://')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)

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
            "content_translated": article[6],
            "title_translated": 'Title'
        }
        data.append(formatted_article)

    return data

@app.route('/api/get_dummy_data')
def get_dummy_data():
    if os.environ.get('FLASK_DEBUG') == '1':
        return jsonify(load_dummy_data())
    else:
        return jsonify({"error": "Dummy data is only available in development environment"})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    pubDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    link = db.Column(db.String, nullable=False, unique=True)
    text = db.Column(db.Text, nullable=True)
    html = db.Column(db.Text, nullable=True)
    title_translated = db.Column(db.String, nullable=True)
    content_translated = db.Column(db.Text, nullable=True)
    source = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "pubDate": self.pubDate.isoformat(),
            "link": self.link,
            "text": self.text,
            "html": self.html,
            "source": self.source,
            "title_translated": self.title_translated,
            "content_translated": self.content_translated,
        }

class SaveArticleResource(Resource):
    def post(self):
        data = request.get_json()
        pubDate = parse(data["pubDate"])

        article = Article(
            title=data["title"],
            pubDate=pubDate,
            link=data["link"],
            text=data["text"],
            html=data["html"],
            source=data["source"],
            title_translated=data["title_translated"],
            content_translated=data["content_translated"]
        )
        print(f"Article to be saved: {article.__dict__}")

        try:
            db.session.add(article)
            db.session.commit()
            return {"message": "Article saved successfully."}
        except IntegrityError:
            db.session.rollback()
            return {"message": "Article with the same link already exists."}, 409

class GetAllArticlesResource(Resource):
    def get(self):
        articles = Article.query.all()
        return jsonify([article.to_dict() for article in articles])

api.add_resource(SaveArticleResource, "/api/save_article")
api.add_resource(GetAllArticlesResource, "/api/get_all_articles")

if __name__ == '__main__':
    if os.environ.get('FLASK_ENV') == 'development':
        dummy_data = load_dummy_data()
    app.run()