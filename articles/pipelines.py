from bs4 import BeautifulSoup
from translate import translate_with_gpt
from app import app, db, Article
from sqlalchemy.exc import IntegrityError

class ArticlesPipeline(object):
    def split_text(self, text, max_tokens):
        import re

        sentences = re.split(r'(?<=[\.\?\!])\s+', text)
        chunks = []
        current_chunk = []

        for sentence in sentences:
            current_chunk.append(sentence)
            if len(" ".join(current_chunk)) > max_tokens:
                current_chunk.pop()  # Remove the last sentence that caused the overflow
                chunks.append(" ".join(current_chunk))
                current_chunk = [sentence]

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def translate_html(self, html, max_tokens):
        soup = BeautifulSoup(html, "html.parser")
        paragraphs = soup.find_all("p")

        for paragraph in paragraphs:
            original_text = paragraph.get_text()
            chunks = self.split_text(original_text, max_tokens)
            translated_chunks = []

            for chunk in chunks:
                try:
                    translated_chunk = translate_with_gpt(chunk)
                    if translated_chunk is not None and translated_chunk.strip():
                        translated_chunks.append(translated_chunk)
                    else:
                        print(f"Empty translated chunk for original chunk: {chunk}")
                except Exception as e:
                    print(f"Error translating chunk: {chunk}. Error: {e}")

            paragraph.string.replace_with(" ".join(translated_chunks))

        return str(soup)

    def process_item(self, item, spider):
        article_html = item["html"]
        max_tokens = 2000  # Adjust based on the model limit

        # Translate the HTML
        translated_html = self.translate_html(article_html, max_tokens)

        # Save the translated content in the item
        item["content_translated"] = translated_html

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
