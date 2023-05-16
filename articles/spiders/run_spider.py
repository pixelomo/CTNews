import os
import subprocess

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run(["scrapy", "crawl", "articles"])
    subprocess.run(["scrapy", "crawl", "cryptonews"])

if __name__ == "__main__":
    main()
