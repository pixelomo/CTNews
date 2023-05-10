from bs4 import BeautifulSoup, NavigableString
from translate import translate_with_gpt, translate_title_with_gpt
from app import app, db, Article
from sqlalchemy.exc import IntegrityError
import os

class ArticlesPipeline(object):
    def divide_into_chunks(self, text, max_chunk_size):
        paragraphs = text.split('\n')
        chunks = []
        current_chunk = []

        for paragraph in paragraphs:
            current_chunk_size = sum(len(p) for p in current_chunk) + len(current_chunk) - 1  # Account for newline characters
            if current_chunk_size + len(paragraph) <= max_chunk_size:
                current_chunk.append(paragraph)
            else:
                chunks.append("\n".join(current_chunk))
                current_chunk = [paragraph]

        if current_chunk:
            chunks.append("\n".join(current_chunk))

        return chunks

    def translate_html(self, html, translated_title):
        soup = BeautifulSoup(html, "html.parser")
        paragraphs = soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "strong", "em", "u", "s", "blockquote", "article", "img", "iframe", "figure", "figcaption", "a"])

        original_texts = []
        for element in paragraphs:
            if element.name == "a":
                original_text = f"<a href='{element['href']}'>{element.get_text(strip=True)}</a>"
            else:
                original_text = element.get_text(strip=True)
            original_texts.append(original_text)

        original_full_text = "\n".join(original_texts)

        if len(original_texts) > 3:
            summary = "\n".join(original_texts[:3]) + "\n"
        else:
            summary = "\n".join(original_texts) + "\n"

        chunks = self.divide_into_chunks(original_full_text, 5100)  # 5400 minus some room for the summary

        translated_chunks = []
        for chunk in chunks:
            try:
                translated_chunk = translate_with_gpt(summary + chunk, translated_title)
                if translated_chunk:
                    # Remove the translated summary from the beginning of the translated_chunk
                    translated_chunk = "\n".join(translated_chunk.split('\n')[len(summary.split('\n')) - 1:])
                    translated_chunks.append(translated_chunk)
                else:
                    print(f"Empty translated text for chunk: {chunk}")
            except Exception as e:
                print(f"Error translating chunk: {chunk}. Error: {e}")

        translated_full_text = "\n".join(translated_chunks)
        translated_full_text = translated_full_text.replace("翻訳・編集　コインテレグラフジャパン", "")
        translated_paragraphs = translated_full_text.splitlines()

        for element, translated_text in zip(paragraphs, translated_paragraphs):
            if element.name == "a":
                a_tag_start = translated_text.find("<a href=")
                if a_tag_start != -1:
                    a_tag_end = translated_text.find("</a>") + 4
                    new_tag = soup.new_tag("a", href=element["href"])
                    new_tag.string = translated_text[a_tag_start + len("<a href='") : a_tag_end - len("</a>") - 1]
                    element.replace_with(new_tag)
                else:
                    new_tag = soup.new_tag("p")
                    new_tag.string = translated_text
                    element.replace_with(new_tag)
            else:
                new_tag = soup.new_tag("p")
                new_tag.string = translated_text
                element.replace_with(new_tag)

        return str(soup)


    def process_item(self, item, spider):
        with app.app_context():
            # Check if the title field is not None
            if item.get("title"):
                # Translate title
                title_translated = translate_title_with_gpt(item["title"])

                if title_translated is not None:
                    item["title_translated"] = title_translated

                    # Check if the text field is not None

                    if item.get("text"):
                        # Translate text
                        # content_translated = self.translate_html(item["html"], title_translated)
                        content_translated = translate_with_gpt(item["html"], title_translated)
                        if content_translated is not None:
                            item["content_translated"] = content_translated
                        else:
                            raise DropItem("Missing content_translated")
                else:
                    raise DropItem("Title is None")
            else:
                raise DropItem("Missing title")

            # Save article to database
            if os.environ.get('APP_ENV') != 'test':
                try:
                    article = Article(
                        title=item["title"],
                        title_translated=item["title_translated"],
                        pubDate=item["pubDate"],
                        link=item["link"],
                        text=item["text"] if item.get("text") else None,
                        html=item["html"],
                        content_translated=item.setdefault("content_translated", None),
                        source=item["source"],
                    )
                    db.session.add(article)
                    db.session.commit()
                except IntegrityError as e:
                    db.session.rollback()

            return item


