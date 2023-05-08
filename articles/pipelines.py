from bs4 import BeautifulSoup, NavigableString
from translate import translate_with_gpt, translate_title_with_gpt
from app import app, db, Article
from sqlalchemy.exc import IntegrityError

class ArticlesPipeline(object):
    # def split_text(self, text, max_tokens):
    #     import re

    #     sentences = re.split(r'(?<=[\.\?\!])\s+', text)
    #     chunks = []
    #     current_chunk = []

    #     for sentence in sentences:
    #         current_chunk.append(sentence)
    #         if len(" ".join(current_chunk)) > max_tokens:
    #             current_chunk.pop()  # Remove the last sentence that caused the overflow
    #             chunks.append(" ".join(current_chunk))
    #             current_chunk = [sentence]

    #     if current_chunk:
    #         chunks.append(" ".join(current_chunk))

    #     num_chunks = len(chunks)
    #     return chunks, num_chunks

    # def translate_html(self, html, max_tokens, translated_title):
    #     soup = BeautifulSoup(html, "html.parser")
    #     paragraphs = soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "strong", "em", "u", "s"])

    #     for element in paragraphs:
    #         original_text = element.get_text()
    #         chunks, num_chunks = self.split_text(original_text, max_tokens)
    #         translated_chunks = []

    #         for index, chunk in enumerate(chunks):
    #             is_last_chunk = index == num_chunks - 1
    #             is_not_first = index > 0
    #             try:
    #                 translated_chunk = translate_with_gpt(chunk, is_last_chunk, is_not_first, translated_title)
    #                 if translated_chunk is not None and translated_chunk.strip():
    #                     translated_chunk = translated_chunk.replace("翻訳・編集　コインテレグラフジャパン", "")
    #                     translated_chunks.append(translated_chunk)
    #                 else:
    #                     print(f"Empty translated chunk for original chunk: {chunk}")
    #             except Exception as e:
    #                 print(f"Error translating chunk: {chunk}. Error: {e}")

    #         translated_text = " ".join(translated_chunks)
    #         if translated_text:
    #             new_tag = soup.new_tag("p")
    #             new_tag.string = translated_text
    #             element.replace_with(new_tag)

    #     return str(soup)

    def translate_html(self, html, translated_title):
        soup = BeautifulSoup(html, "html.parser")
        paragraphs = soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "strong", "em", "u", "s", "blockquote", "article"])

        original_texts = []
        for element in paragraphs:
            original_text = element.get_text(strip=True)
            original_texts.append(original_text)

        original_full_text = "\n".join(original_texts)
        try:
            translated_full_text = translate_with_gpt(original_full_text, translated_title)
            if translated_full_text is not None and translated_full_text.strip():
                translated_full_text = translated_full_text.replace("翻訳・編集　コインテレグラフジャパン", "")
                translated_paragraphs = translated_full_text.split("\n")

                for element, translated_text in zip(paragraphs, translated_paragraphs):
                    new_tag = soup.new_tag("p")
                    new_tag.string = translated_text
                    element.replace_with(new_tag)
            else:
                print(f"Empty translated text for original text: {original_full_text}")
        except Exception as e:
            print(f"Error translating text: {original_full_text}. Error: {e}")

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
                    if item["text"]:
                        # Translate text
                        content_translated = self.translate_html(item["html"], title_translated)
                        if content_translated is not None:
                            item["content_translated"] = content_translated
                        else:
                            raise DropItem("Missing content_translated")
            else:
                raise DropItem("Missing title")

                # Save article to database
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

