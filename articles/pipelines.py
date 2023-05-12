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

    def is_child_of_any(self, element, elements):
        for e in elements:
            if element in e.descendants:
                return True
        return False

    def translate_text(self, text, translated_title):
        translated_text = translate_with_gpt(text, translated_title)

        sentences = translated_text.split("。")
        formatted_text = ""
        for i, sentence in enumerate(sentences):
            formatted_text += sentence
            if i % 2 == 1:
                formatted_text += "。\n\n"
            else:
                formatted_text += "。"
        print(formatted_text)

        return formatted_text

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
            translated_full_text = translate_with_gpt(original_full_text, translated_title)
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
        # print(item)
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
                        content_translated = self.translate_text(item["text"], title_translated)
                        if content_translated is not None:
                            item["content_translated"] = content_translated
                            # print(f"Content Translated: {item['content_translated']}")
                        else:
                            print("Dropping item: Missing content_translated")  # Add this line
                            # raise DropItem("Missing content_translated")
                else:
                    print("Dropping item: Title is None")
                    # raise DropItem("Title is None")
            else:
                print("Dropping item: Missing title")
                # raise DropItem("Missing title")

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


