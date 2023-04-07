from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dateutil.parser import parse
import os
from sqlalchemy.exc import IntegrityError
from flask import render_template
from translate import translate_with_gpt4
# from flask_cors import CORS

app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": ["https://gentle-earth-02543.herokuapp.com/", "http://127.0.0.1:5000"]}})
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL', 'sqlite:///articles.db').replace('postgres://', 'postgresql://')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

@app.route('/')
def index():
    return render_template('index.html')


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    pubDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    link = db.Column(db.String, nullable=False, unique=True)  # Add unique constraint
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
        article_text = data["text"]
        max_tokens = 2048  # Adjust based on the model limit

        # Split the text into chunks
        chunks = split_text(article_text, max_tokens)

        # Translate each chunk and join them together
        translated_chunks = []
        for chunk in chunks:
            translated_chunk = translate_with_gpt4(chunk)
            print(f"Translated chunk: {translated_chunk}")  # Debugging
            translated_chunks.append(translated_chunk)
        content_translated = " ".join(translated_chunks)
        print(f"Full translated content: {content_translated}")  # Debugging

        article = Article(
            title=data["title"],
            pubDate=pubDate,
            link=data["link"],
            text=data["text"],
            html=data["html"],
            content_translated=content_translated,
        )

        try:
            db.session.add(article)
            db.session.commit()
            return {"message": "Article saved and translated successfully."}
        except IntegrityError:
            db.session.rollback()
            return {"message": "Article with the same link already exists."}, 409

class GetAllArticlesResource(Resource):
    def get(self):
        articles = Article.query.all()
        return jsonify([article.to_dict() for article in articles])

api.add_resource(SaveArticleResource, "/api/save_article")
api.add_resource(GetAllArticlesResource, "/api/get_all_articles")

if __name__ == "__main__":
    app.run(debug=True)
