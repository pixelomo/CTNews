import os
import subprocess

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run(["scrapy", "crawl", "articles"])
    subprocess.run(["scrapy", "crawl", "cryptopanic"])
    # subprocess.run(["scrapy", "crawl", "coindesk"])
    # subprocess.run(["scrapy", "crawl", "wublock"])

if __name__ == "__main__":
    main()
