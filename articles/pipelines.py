from translate import translate_with_gpt4

class ArticlesPipeline(object):
    def process_item(self, item, spider):
        article_text = item["text"]
        max_tokens = 2048  # Adjust based on the model limit

        # Split the text into chunks
        chunks = split_text(article_text, max_tokens)

        # Translate each chunk and join them together
        translated_chunks = []
        for chunk in chunks:
            translated_chunk = translate_with_gpt4(chunk)
            print(f"Translated chunk: {translated_chunk}")  # Debugging
            translated_chunks.append(translated_chunk)
        content_translated = " ".join(translated_chunks)
        print(f"Full translated content: {content_translated}")  # Debugging

        # Save the translated content in the item
        item["content_translated"] = content_translated
        print(f"Item content_translated: {item['content_translated']}")  # Debugging

        # Save the item to the database
        # Your existing code to save the item to the database goes here

        return item
