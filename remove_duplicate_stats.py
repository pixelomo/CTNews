from app import app, db, ArticleStats
from sqlalchemy.exc import IntegrityError

def remove_duplicates():
    with app.app_context():
        articles = ArticleStats.query.all()
        unique_titles = set()
        duplicates = []

        for article in articles:
            if article.title in unique_titles:
                duplicates.append(article)
            else:
                unique_titles.add(article.title)

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
