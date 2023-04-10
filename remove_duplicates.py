from app import app, db, Article

def remove_duplicates():
    with app.app_context():
        articles = Article.query.all()
        unique_articles = {}

        for article in articles:
            if article.link not in unique_articles:
                unique_articles[article.link] = article
            else:
                db.session.delete(article)

        db.session.commit()

if __name__ == "__main__":
    remove_duplicates()
