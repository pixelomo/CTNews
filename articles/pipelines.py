from bs4 import BeautifulSoup, NavigableString
from translate import translate_with_gpt, translate_title_with_gpt
from app import app, db, Article
from sqlalchemy.exc import IntegrityError
import copy

class ArticlesPipeline(object):

    def translate_html(self, html, translated_title):
        soup = BeautifulSoup(html, "html.parser")
        paragraphs = soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "strong", "em", "u", "s", "blockquote", "article", "img", "iframe"])

        original_texts = []
        placeholder_index = 0
        for element in paragraphs:
            if element.name == "iframe" or element.name == "img":
                placeholder_text = f"[[{placeholder_index}]]"
                original_texts.append(placeholder_text)
                placeholder_index += 1
            elif element.name == "a":
                original_text = f"<a href='{element['href']}'>{element.get_text(strip=True)}</a>"
            else:
                original_text = element.get_text(strip=True)
            original_texts.append(original_text)

        original_full_text = "\n".join(original_texts)
        try:
            translated_full_text = translate_with_gpt(original_full_text, translated_title)
            if translated_full_text is not None and translated_full_text.strip():
                translated_full_text = translated_full_text.replace("翻訳・編集　コインテレグラフジャパン", "")
                translated_paragraphs = translated_full_text.splitlines()

                placeholders = soup.find_all(["iframe", "img"])
                for element, translated_text in zip(paragraphs, translated_paragraphs):
                    if element.name == "iframe" or element.name == "img":
                        new_tag = copy.copy(element)
                        placeholder_text = f"[[{placeholders.index(element)}]]"
                        translated_text = translated_text.replace(placeholder_text, str(new_tag))
                    elif element.name == "a":
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
                    raise DropItem("Title is None")
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


