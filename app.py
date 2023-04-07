from flask import Flask, render_template, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from dateutil.parser import parse
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
api = Api(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    pubDate = db.Column(db.DateTime)
    link = db.Column(db.String(500), unique=True)
    text = db.Column(db.Text)
    html = db.Column(db.Text)
    content_translated = db.Column(db.Text)

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
            content_translated=data["content_translated"],
        )

        try:
            db.session.add(article)
            db.session.commit()
            return {"message": "Article saved successfully."}
        except IntegrityError:
            db.session.rollback()
            return {"message": "Article with the same link already exists."}, 409

api.add_resource(SaveArticleResource, "/api/save_article")

@app.route("/")
def index():
    articles = Article.query.order_by(Article.pubDate.desc()).all()
    return render_template("index.html", articles=articles)

@app.route("/article/<int:article_id>")
def article(article_id):
    article = Article.query.get(article_id)
    return render_template("article.html", article=article)

if __name__ == "__main__":
    app.run()
