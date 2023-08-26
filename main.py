# main.py
from scraper.poll_data_scraper import PollDataScraper
import pandas as pd

if __name__ == "__main__":
    url = "https://cdn-dev.economistdatateam.com/jobs/pds/code-test/index.html"
    scraper = PollDataScraper(url)
    scraper.fetch_page()
    scraper.scrape_to_csv("data/poll_data.csv")
    df = scraper.csv_to_dataframe("data/poll_data.csv")
    print(df.head())