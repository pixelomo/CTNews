from translate import translate_with_gpt
from app import app, db
from CTNews.models import Article

class ArticlesPipeline(object):
    def split_text(self, text, max_tokens):
        words = text.split()
        chunks = []
        current_chunk = []

        for word in words:
            current_chunk.append(word)
            if len(" ".join(current_chunk)) > max_tokens:
                current_chunk.pop()  # Remove the last word that caused the overflow
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def process_item(self, item, spider):
        article_text = item["text"]
        max_tokens = 2048  # Adjust based on the model limit

        # Split the text into chunks
        chunks = self.split_text(article_text, max_tokens)

        # Translate each chunk and join them together
        translated_chunks = []
        for chunk in chunks:
            translated_chunk = translate_with_gpt(chunk)
            print(f"Translated chunk: {translated_chunk}")  # Debugging
            if translated_chunk is not None:
                translated_chunks.append(translated_chunk)
        content_translated = " ".join(translated_chunks)
        print(f"Full translated content: {content_translated}")  # Debugging

        # Save the translated content in the item
        item["content_translated"] = content_translated
        print(f"Item content_translated: {item['content_translated']}")  # Debugging

        # Save the item to the database
        with app.app_context():
            article = Article(
                title=item["title"],
                pubDate=item["pubDate"],
                link=item["link"],
                text=item["text"],
                html=item["html"],
                content_translated=item["content_translated"]
            )

            try:
                db.session.add(article)
                db.session.commit()
                print("Article saved successfully.")
            except IntegrityError:
                db.session.rollback()
                print("Article with the same link already exists.")

        return item

        return item
