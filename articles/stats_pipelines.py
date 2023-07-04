from app import app, db, ArticleStats

class StatsPipeline(object):
    def process_item(self, item, spider):
        with app.app_context():
            article = ArticleStats()

            article.pubDate = item["pubDate"]
            article.source = item["source"]
            article.character_count = len(item["text"])

            try:
                db.session.add(article)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Failed to save article stats: {e}")
                raise
            finally:
                db.session.close()

            return item