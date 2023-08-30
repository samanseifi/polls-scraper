# main.py
from scraper.poll_data_scraper import PollDataScraper
from scraper.poll_data_processor import PollDataProcessor

from matplotlib import pyplot as plt
import pandas as pd

if __name__ == "__main__":
    url = "https://cdn-dev.economistdatateam.com/jobs/pds/code-test/index.html"
    scraper = PollDataScraper(url)
    scraper.fetch_page()
    df = scraper.scrape_to_dataframe_and_csv("data/poll_data.csv")

    df['date'] = pd.to_datetime(df['date'])

    # Fill missing values with NaN
    df = df.replace('', float('nan'))

    # Create an instance of PollDataProcessor
    processor = PollDataProcessor(df)

    # Candidates to analyze if new candidates added it will be captured here
    candidates_to_analyze = scraper.extract_column_candidates()

    # Call the methods
    processor.plot_gaussian_process_trends(candidates_to_analyze)
    processor.plot_moving_average_trends(candidates_to_analyze, window_size=10, save_to_csv=True)
