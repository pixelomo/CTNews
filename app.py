from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dateutil.parser import parse
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('postgres://lzitmwilupkzby:607d003af773d4ac532c8bab5ae63da535da8a134ce08c51d998d4cc38df2ade@ec2-34-226-11-94.compute-1.amazonaws.com:5432/damb56efd6dkql', 'sqlite:///articles.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    pubDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    link = db.Column(db.String, nullable=False)
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
        pubDate = parse(data["pubDate"])
        article = Article(
            title=data["title"],
            pubDate=pubDate,
            link=data["link"],
            text=data["text"],
            html=data["html"]
        )
        db.session.add(article)
        db.session.commit()
        return {"message": "Article saved successfully."}

class GetAllArticlesResource(Resource):
    def get(self):
        articles = Article.query.all()
        return jsonify([article.to_dict() for article in articles])

api.add_resource(SaveArticleResource, "/api/save_article")
api.add_resource(GetAllArticlesResource, "/api/get_all_articles")

if __name__ == "__main__":
    app.run(debug=True)