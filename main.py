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


    # Load the polling data from the DataFrame
    # Replace 'data.csv' with the actual path to your CSV file
    df = pd.read_csv('data/poll_data.csv', parse_dates=['date'])


    # Fill missing values with NaN
    df = df.replace('', float('nan'))

    # Create an instance of PollDataProcessor
    processor = PollDataProcessor(df)

    # Candidates to analyze
    candidates_to_analyze = ['Bulstrode', 'Lydgate', 'Vincy', 'Casaubon', 'Chettam',	'Others']

    # Call the methods
    processor.plot_gaussian_process_trends(candidates_to_analyze)
    processor.plot_moving_average_trends(candidates_to_analyze, window_size=10)
