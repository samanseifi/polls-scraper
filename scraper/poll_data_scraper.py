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
    
    def clean_columns(self, df, column_names):
        for column_name in column_names:
            # Convert the column to numeric
            df[column_name] = pd.to_numeric(df[column_name], errors='coerce')
            
            # Divide values between 1 and 100 by 100
            df.loc[(df[column_name] > 1) & (df[column_name] <= 100), column_name] /= 100
        
        return df
    
    def scrape_to_dataframe_and_csv(self, csv_filename: str) -> pd.DataFrame:
        if self.soup is None:
            raise RuntimeError("Page content not fetched. Call fetch_page() first.")
        
        table = self.soup.find("table")
        if table is None:
            raise ValueError("Table not found in the page content.")
        
        column_headers = ["date", "pollster", "n"] + self.extract_column_order()
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
                print("Warning: Empty row found.")
                continue
            
            row_data = [self.clean_cell(cell.get_text(strip=True)) for cell in cells]
            data.append(row_data)
        
        df = pd.DataFrame(data, columns=column_headers)
        df = self.clean_columns(df, column_headers[3:])
        
        df.to_csv(csv_filename, index=False)  # Save DataFrame to CSV
        return df
