from app import app, db, ArticleStats

class CountPipeline(object):
    def process_item(self, item, spider):
        with app.app_context():
            session = db.create_scoped_session()
            article = ArticleStats()

            article.pubDate = item["pubDate"]
            article.source = item["source"]
            article.character_count = len(item["text"])

            try:
                session.add(article)
                session.commit()
            except Exception as e:
                session.rollback()
                print(f"Failed to save article: {e}")
                raise
            finally:
                session.close()

            return item