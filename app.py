from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///articles.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app)

class SaveArticleResource(Resource):
    def post(self):
        data = request.get_json()
        article = ArticleModel(
            title=data["title"],
            pubDate=data["pubDate"],
            link=data["link"],
            text=data["text"],
            html=data["html"]
        )
        db.session.add(article)
        db.session.commit()
        return {"message": "Article saved successfully."}

api.add_resource(SaveArticleResource, "/api/save_article")

if __name__ == "__main__":
    app.run(debug=True)