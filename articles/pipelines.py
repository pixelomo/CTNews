# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
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
            translated_chunks.append(translated_chunk)
        content_translated = " ".join(translated_chunks)

        # Save the translated content in the item
        item["content_translated"] = content_translated

        # Save the item to the database
        # Your existing code to save the item to the database goes here

        return item

