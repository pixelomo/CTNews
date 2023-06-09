from app import app, db, ArticleStats

class StatsPipeline(object):
    def process_item(self, item, spider):
        if item["source"] not in ["CTJP", "Coinpost"]:
            return item

        with app.app_context():
            article = ArticleStats()
            print("STATS PIPELINE STARTED")
            article.title = item["title"]
            article.pubDate = item["pubDate"]
            article.source = item["source"]
            article.character_count = len(item["text"])

            try:
                db.session.add(article)
                db.session.commit()
                print(f"Saved article stats: {article.to_dict()}")
            except Exception as e:
                db.session.rollback()
                print(f"Failed to save article stats: {e}")
                raise
            finally:
                db.session.close()

            return item