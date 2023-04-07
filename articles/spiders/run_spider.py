import os
import subprocess

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run(["scrapy", "crawl", "articles"])

if __name__ == "__main__":
    main()
