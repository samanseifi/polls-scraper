import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

class PollDataScraper:
    def __init__(self, url):
        self.url = url
        self.soup = None

    def fetch_page(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
            self.soup = BeautifulSoup(response.content, "html.parser")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error fetching the page: {e}")

    def scrape_to_csv(self, csv_filename):
        if self.soup is None:
            raise RuntimeError("Page content not fetched. Call fetch_page() first.")

        table = self.soup.find("table")

        with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",")
            csv_writer.writerow(
                ["Date", "Pollster", "Sample", "Bulstrode", "Lydgate", "Vincy", "Casaubon", "Chettam", "Others"]
            )

            rows = table.find("tbody").find_all("tr")

            for row in rows:
                cells = row.find_all("td")
                row_data = [cell.get_text(strip=True) for cell in cells]
                csv_writer.writerow(row_data)
    
    def csv_to_dataframe(self, csv_filename):
        try:
            df = pd.read_csv(csv_filename)
            return df
        except FileNotFoundError:
            raise RuntimeError(f"CSV file '{csv_filename}' not found.")
        except pd.errors.EmptyDataError:
            raise RuntimeError(f"CSV file '{csv_filename}' is empty.")
        except pd.errors.ParserError:
            raise RuntimeError(f"Error parsing CSV file '{csv_filename}'.")
