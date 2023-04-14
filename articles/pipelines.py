from bs4 import BeautifulSoup, NavigableString
from translation_tasks import perform_translation
from app import app, db, Article
from sqlalchemy.exc import IntegrityError
from celery_app import celery_app

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
        if html is None:
            return ""

        soup = BeautifulSoup(html, "html.parser")

        if not soup.body:
            return ""

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

        first_suitable_tag = soup.body.find(["p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "strong", "em", "u", "s"])
        if first_suitable_tag:
            first_suitable_tag.insert_before(h3_tag)

        return str(soup)

    from celery import signature

def process_item(self, item, spider):
    def on_translate_title_done(task_id, item):
        translated_title = celery_app.AsyncResult(task_id).get()
        item["title_translated"] = translated_title
        print(f"Translated title: {translated_title}")

    def on_translate_html_done(task_id, item):
        content_translated = celery_app.AsyncResult(task_id).get()
        print(f"Translated content: {content_translated}")

        # Save the item to the database
        with app.app_context():
            article = Article(
                title=item["title"],
                title_translated=item["title_translated"],
                pubDate=item["pubDate"],
                link=item["link"],
                text=item["text"],
                html=item["html"],
                content_translated=content_translated
            )

            try:
                db.session.add(article)
                db.session.commit()
                print("Article saved successfully.")
            except IntegrityError:
                db.session.rollback()
                print("Article with the same link already exists.")

    # Create Celery signatures for the callback functions
    on_translate_title_done_sig = signature(on_translate_title_done, args=(item,))
    on_translate_html_done_sig = signature(on_translate_html_done, args=(item,))

    # Translate the title
    translation_task_title = perform_translation.apply_async(
        args=(item["title"], "en"),
        link=on_translate_title_done_sig
    )

    # Translate the HTML content
    translation_task_html = perform_translation.apply_async(
        args=(item["html"], "en"),
        link=on_translate_html_done_sig
    )

    return item



