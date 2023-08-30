import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import re
from typing import List
import logging

class PollDataScraper:
    def __init__(self, url: str):
        self.url = url
        self.soup = None
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger("poll_data_scraper")
        logger.setLevel(logging.ERROR)
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        file_handler = logging.FileHandler('scraper_error_log.txt')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        return logger
    
    def fetch_page(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
            self.soup = BeautifulSoup(response.content, "html.parser")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching the page: {e}")
            raise RuntimeError(f"Error fetching the page: {e}")
        
    def clean_cell(self, cell_text: str) -> str:
        cleaned_text = re.sub(r'[*+,]+', '', cell_text)
        cleaned_text = "" if cleaned_text == "**" else cleaned_text
        
        if "%" in cell_text:
            try:
                cleaned_text = str(float(cleaned_text.strip('%')) / 100)
            except ValueError:
                pass  # Handle the case where conversion to float fails
        
        return cleaned_text

    def extract_column_candidates(self) -> List[str]:
        if self.soup is None:
            raise RuntimeError("Page content not fetched. Call fetch_page() first.")
        
        table = self.soup.find("table")
        thead = table.find("thead")
        column_names = [th.get_text(strip=True) for th in thead.find_all("th")]
        column_names = column_names[3:]  # Remove the first three columns
        
        return column_names
    
    def clean_columns(self, df, column_names):
        for column_name in column_names:
            df[column_name] = pd.to_numeric(df[column_name], errors='coerce')
            df.loc[(df[column_name] > 1) & (df[column_name] <= 100), column_name] /= 100
        
        return df
    
    def scrape_to_dataframe_and_csv(self, csv_filename: str) -> pd.DataFrame:
        try:
            if self.soup is None:
                raise RuntimeError("Page content not fetched. Call fetch_page() first.")
            
            table = self.soup.find("table")
            if table is None:
                raise ValueError("Table not found in the page content.")
            
            column_headers = ["date", "pollster", "n"] + self.extract_column_candidates()
            data = []
            
            tbody = table.find("tbody")
            if tbody is None:
                raise ValueError("Table body (tbody) not found in the table.")
            
            rows = tbody.find_all("tr")
            if not rows:
                raise ValueError("No rows found in the table.")
            
            for row in rows:
                cells = row.find_all("td")
                if not cells:
                    self.logger.warning("Empty row found.")
                    continue
                
                row_data = [self.clean_cell(cell.get_text(strip=True)) for cell in cells]
                data.append(row_data)
            
            df = pd.DataFrame(data, columns=column_headers)
            df = self.clean_columns(df, column_headers[3:])
            
            df.to_csv(csv_filename, index=False)  # Save DataFrame to CSV
            return df
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            raise e
