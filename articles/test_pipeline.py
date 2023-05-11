import json
from .pipelines import ArticlesPipeline
import os
os.environ['APP_ENV'] = 'test'

def test_process_scraped_article():
    # Load json
    with open("./articles/test_article.json", "r") as f:
        scraped_article = json.load(f)

    # print("Loaded JSON:", scraped_article)
    # print("Text value:", scraped_article["values"][0][4])
    # Create an instance of ArticlesPipeline
    pipeline = ArticlesPipeline()

    # Call the process_item method with the loaded scraped_article
    processed_article = pipeline.process_item(scraped_article, None)

    # Print the processed article
    # print(processed_article)

if __name__ == "__main__":
    test_process_scraped_article()
