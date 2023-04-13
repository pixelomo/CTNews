from celery import shared_task
from models import db, Article
from dateutil.parser import parse
from sqlalchemy.exc import IntegrityError

# @shared_task
# def save_article(data):
#     pubDate = parse(data["pubDate"])

#     article = Article(
#         title=data["title"],
#         pubDate=pubDate,
#         link=data["link"],
#         text=data["text"],
#         html=data["html"],
#         content_translated=data.get("content_translated", "")
#     )

#     try:
#         db.session.add(article)
#         db.session.commit()
#         return {"message": "Article saved successfully."}
#     except IntegrityError:
#         db.session.rollback()
#         return {"message": "Article with the same link already exists."}, 409
