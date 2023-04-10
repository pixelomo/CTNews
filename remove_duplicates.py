from app import app, db, Article
from sqlalchemy.exc import IntegrityError

def remove_duplicates():
    with app.app_context():
        articles = Article.query.all()
        unique_links = set()
        duplicates = []

        for article in articles:
            if article.link in unique_links:
                duplicates.append(article)
            else:
                unique_links.add(article.link)

        for duplicate in duplicates:
            try:
                db.session.delete(duplicate)
                db.session.commit()
                print(f"Deleted duplicate article: {duplicate.title}")
            except IntegrityError:
                db.session.rollback()
                print("Error deleting duplicate article.")

if __name__ == "__main__":
    remove_duplicates()
