from bs4 import BeautifulSoup, NavigableString
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

    def translate_html(self, html, max_tokens, translated_title):
        soup = BeautifulSoup(html, "html.parser")
        paragraphs = soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "strong", "em", "u", "s"])

        for element in paragraphs:
            original_text = element.get_text()
            chunks = self.split_text(original_text, max_tokens)
            translated_chunks = []

            for chunk in chunks:
                try:
                    translated_chunk = translate_with_gpt(chunk)
                    if translated_chunk is not None and translated_chunk.strip():
                        translated_chunk = translated_chunk.replace("翻訳・編集　コインテレグラフジャパン", "")
                        translated_chunks.append(translated_chunk)
                    else:
                        print(f"Empty translated chunk for original chunk: {chunk}")
                except Exception as e:
                    print(f"Error translating chunk: {chunk}. Error: {e}")

            translated_text = " ".join(translated_chunks)
            if translated_text:
                new_tag = soup.new_tag(element.name)
                new_tag.string = translated_text
                element.replace_with(new_tag)

        h3_tag = soup.new_tag("h3")
        h3_tag.string = translated_title

        if soup.body is not None:
            first_suitable_tag = soup.body.find(["p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "strong", "em", "u", "s"])
            if first_suitable_tag:
                first_suitable_tag.insert_before(h3_tag)

        return str(soup)

    def process_item(self, item, spider):
        with app.app_context():
            # Check if an article with the same title already exists in the database
            existing_article = Article.query.filter_by(title=item["link"]).first()

            if existing_article:
                print("Article with the same link already exists.")
                return item

            article_text = item["text"]
            max_tokens = 5650  # Adjust based on the model limit

            # Translate the title
            translated_title = translate_with_gpt(item["title"])

            # Translate the HTML content
            content_translated = self.translate_html(item["html"], max_tokens, translated_title)

            # Save the translated content in the item
            item["content_translated"] = content_translated

            # Save the item to the database
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
            except IntegrityError as e:
                db.session.rollback()
                print("Article with the same link already exists. Error:", e)

        return item