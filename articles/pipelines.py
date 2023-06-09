from bs4 import BeautifulSoup, NavigableString
from translate import translate_text, translate_title, request_translation
from briefings import briefings
from app import app, db, Article
from sqlalchemy.exc import IntegrityError
from itertools import islice
import os
import re

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

    def is_child_of_any(self, element, elements):
        for e in elements:
            if element in e.descendants:
                return True
        return False

    def process_original_text(self, text):
        text = re.sub(r'(?<=[a-z])([A-Z])', r'. \1', text)  # Insert full stop and space before uppercase letters between lowercase letters
        text = re.sub(r'(?<=\s|\.)Related:.*?(?<=\w)(?=\s|\.|$)|(?<=\s|\.)Magazine:.*?(?<=\w)(?=\s|\.|$)', '', text)
        return text.strip()

    def wrap_paragraphs_in_tags(self, text):
        paragraphs = text.split('\n\n')
        wrapped_paragraphs = ['<p>{}</p>'.format(p) for p in paragraphs]
        return '\n'.join(wrapped_paragraphs)

    def translate_article(self, text, translated_title, target_language):
        # Function to split the text into chunks
        def split_text_by_chunks(text, chunk_size):
            words = text.split()
            for _ in range(0, len(words), chunk_size):
                yield ' '.join(islice(words, chunk_size))

        # Check if the text exceeds the token limit and chunk it accordingly
        if len(text) > 5450:
            chunks = list(split_text_by_chunks(text, 5450))
        else:
            chunks = [text]

        translated_chunks = []

        for i, chunk in enumerate(chunks):
            # context = ""
            # if i > 0:
                # last_sentence = translated_chunks[-1].rsplit("。", 1)[-2] + "。"
                # context = f"Based on this summary, continue writing this article cohesively: {last_sentence}"
                # chunk = context + chunk
            translated_chunk = request_translation(translate_text, chunk, translated_title, target_language)
            translated_chunks.append(translated_chunk)

        translated_text = " ".join(filter(None, translated_chunks))
        translated_text = self.wrap_paragraphs_in_tags(translated_text)

        return translated_text

    def translate_html(self, html, translated_title):
        soup = BeautifulSoup(html, "html.parser")
        # for script in soup.find_all("script"):
        #     script.decompose()
        # for tweet in soup.find_all("blockquote", class_="twitter-tweet"):
        #     tweet.decompose()
        for script in soup(["script"]):
            script.extract()
        paragraphs = soup.find_all(["p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "li", "strong", "blockquote", "article", "a"])

        original_texts = []
        for element in paragraphs:
            original_text = element.get_text()
            if original_text.startswith("Related:") or original_text.startswith("Magazine:"):
                continue
            if self.is_child_of_any(element, paragraphs):
                continue
            # if element.name == "a":
            #     original_text = f"&nbsp;<a href='{element['href']}'>{element.get_text(strip=True)}</a>&nbsp;"
            # if element.name == "blockquote":
            #     original_text = f'{element.get_text(strip=True)}'

            # Replace double quotes with single quotes
            original_text = original_text.replace('“', "'")
            original_text = original_text.replace('”', "'")
            original_text = original_text.replace('\n', " ")
            # Only add the text to the list if it's not a duplicate
            if original_text not in original_texts:
                original_texts.append(original_text)

        original_full_text = "\n".join(original_texts)

        print("START: \n" +original_full_text+ "\n :END")

        try:
            translated_full_text = request_translation(translate_text, original_full_text, translated_title)
            if translated_full_text is not None and translated_full_text.strip():
                translated_full_text = translated_full_text.replace("翻訳・編集　コインテレグラフジャパン", "")
                translated_paragraphs = translated_full_text.split("\n")

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

            else:
                print(f"Empty translated text for original text: {original_full_text}")
        except Exception as e:
            print(f"Error translating text: {original_full_text}. Error: {e}")

        return str(soup)

    def process_item(self, item, spider):
        print("process_item called")

        with app.app_context():
            # Check if the title field is not None
            if item.get("title"):
                # Loop over each language in briefings
                for language in briefings:
                    target_language = language['language']

                    # Translate title
                    title_translated = request_translation(translate_title, item["title"], target_language=target_language)

                    if title_translated is not None:
                        # Save Japanese translated title directly to 'title_translated' field
                        if target_language == "Japanese":
                            item["title_translated"] = title_translated
                        else:
                            item[f"title_{target_language}"] = title_translated

                        # Check if the text field is not None
                        if item.get("text"):
                            # Translate text
                            content_translated = self.translate_article(item["text"], title_translated, target_language)
                            if content_translated is not None:
                                # Save Japanese translated text directly to 'content_translated' field
                                if target_language == "Japanese":
                                    item["content_translated"] = content_translated
                                else:
                                    item[f"text_{target_language}"] = content_translated
                                print(f"Content Translated: {item[f'text_{target_language}' if target_language != 'Japanese' else 'content_translated']}")
                            else:
                                print(f"Dropping item: Missing content_translated for {target_language}")
                    else:
                        print(f"Dropping item: Title is None for {target_language}")
            else:
                print("Dropping item: Missing title")

            # Save article to database
            if os.environ.get('APP_ENV') != 'test':
                try:
                    article = Article(
                        title=item["title"],
                        pubDate=item["pubDate"],
                        link=item["link"],
                        html=item["html"],
                        source=item["source"],
                    )
                    for language in briefings:
                        target_language = language['language']
                        if target_language == "Japanese":
                            article.title_translated = item.get("title_translated")
                            article.content_translated = item.get("content_translated")
                        else:
                            setattr(article, f"title_{target_language}", item.get(f"title_{target_language}"))
                            setattr(article, f"text_{target_language}", item.get(f"text_{target_language}"))
                    db.session.add(article)
                    db.session.commit()
                except IntegrityError as e:
                    db.session.rollback()

            return item


