from bs4 import BeautifulSoup, NavigableString
from translate import translate_with_gpt, translate_title_with_gpt
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
                new_tag = soup.new_tag("p")
                new_tag.string = translated_text
                element.replace_with(new_tag)

        return str(soup)

    def process_item(self, item, spider):
        # Translate title
        title_translated = translate_title_with_gpt(item["title"])
        item["title_translated"] = title_translated

        # Check if the text field is not None
        if item["text"]:
            # Set max tokens for text translation
            max_tokens = 5650

            # Translate text
            content_translated = self.translate_html(item["html"], max_tokens)
            item["content_translated"] = content_translated

        # Save article to database
        try:
            article = Article(
                title=item["title"],
                title_translated=item["title_translated"],
                pubDate=item["pubDate"],
                link=item["link"],
                text=item["text"] if item.get("text") else None,
                html=item["html"],
                content_translated=item["content_translated"],
                source=item["source"],
            )
            self.session.add(article)
            self.session.commit()

        except SQLAlchemyError as e:
            self.session.rollback()
            spider.logger.error(f"Error saving article: {e}")
            raise DropItem(f"Error saving article: {e}")

        return item

