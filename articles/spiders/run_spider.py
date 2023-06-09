import os
import subprocess

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run(["scrapy", "crawl", "ctjp"])
    subprocess.run(["scrapy", "crawl", "coinpost"])
    subprocess.run(["scrapy", "crawl", "articles"])
    subprocess.run(["scrapy", "crawl", "ambcrypto"])
    subprocess.run(["scrapy", "crawl", "blockworks"])
    subprocess.run(["scrapy", "crawl", "odaily"])
    subprocess.run(["scrapy", "crawl", "theblock"])
    # subprocess.run(["scrapy", "crawl", "cryptonews"])
    subprocess.run(["scrapy", "crawl", "coindesk"])

if __name__ == "__main__":
    main()
