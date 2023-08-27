import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import re
from typing import List

class PollDataScraper:
    def __init__(self, url: str):
        self.url = url
        self.soup = None

    def fetch_page(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
            self.soup = BeautifulSoup(response.content, "html.parser")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error fetching the page: {e}")
        
    def clean_cell(self, cell_text: str) -> str:
        # Remove the * and ** if they appear at the end of the string
        cleaned_text = re.sub(r'[*+,]+', '', cell_text)

        # This removes entries with only "**"
        cleaned_text = "" if cleaned_text == "**" else cleaned_text

        # Convert percentage to decimal
        if "%" in cell_text:
            try:
                cleaned_text = str(float(cleaned_text.strip('%')) / 100)
            except ValueError:
                pass  # Handle the case where conversion to float fails

        return cleaned_text

    def extract_column_order(self) -> List[str]:
        if self.soup is None:
            raise RuntimeError("Page content not fetched. Call fetch_page() first.")

        table = self.soup.find("table")

        # Find the table header
        thead = table.find("thead")

        # Find all th elements within the thead
        column_names = [th.get_text(strip=True) for th in thead.find_all("th")]

        # Remove the first three columns (Date, Pollster, Sample)
        column_names = column_names[3:]

        return column_names

    def scrape_to_csv(self, csv_filename: str):
        if self.soup is None:
            raise RuntimeError("Page content not fetched. Call fetch_page() first.")

        table = self.soup.find("table")

        with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:        
            csv_writer = csv.writer(csv_file, delimiter=",")
            csv_writer.writerow(
                ["date", "pollster", "n"] + self.extract_column_order()
            )
            
            rows = table.find("tbody").find_all("tr")

            for row in rows:
                cells = row.find_all("td")
                row_data = [self.clean_cell(cell.get_text(strip=True)) for cell in cells]
                csv_writer.writerow(row_data)
    
    def csv_to_dataframe(self, csv_filename: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(csv_filename)
            return df
        except FileNotFoundError:
            raise RuntimeError(f"CSV file '{csv_filename}' not found.")
        except pd.errors.EmptyDataError:
            raise RuntimeError(f"CSV file '{csv_filename}' is empty.")
        except pd.errors.ParserError:
            raise RuntimeError(f"Error parsing CSV file '{csv_filename}'.")
