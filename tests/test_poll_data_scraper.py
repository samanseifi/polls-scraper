import unittest
from unittest.mock import MagicMock, patch
from scraper.poll_data_scraper import PollDataScraper

class TestPollDataScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = PollDataScraper("https://cdn-dev.economistdatateam.com/jobs/pds/code-test/index.html")

    @patch("requests.get")
    def test_fetch_page_successful(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = b"<html><table>...</table></html>"
        mock_get.return_value = mock_response

        self.scraper.fetch_page()
        self.assertIsNotNone(self.scraper.soup)

    def test_clean_cell_percentage(self):
        cleaned_text = self.scraper.clean_cell("67.6%")
        self.assertEqual(cleaned_text, 0.676)

    # Add more test cases for clean_cell based on your data variations

    def test_csv_to_dataframe_successful(self):
        df = self.scraper.csv_to_dataframe("tests/test_data.csv")
        self.assertIsNotNone(df)

    def test_csv_to_dataframe_file_not_found(self):
        with self.assertRaises(RuntimeError):
            self.scraper.csv_to_dataframe("nonexistent.csv")

    def test_csv_to_dataframe_empty_file(self):
        with open("empty.csv", "w") as f:
            f.write("")

        with self.assertRaises(RuntimeError):
            self.scraper.csv_to_dataframe("tests/empty.csv")

    # Add more test cases for csv_to_dataframe based on different scenarios

if __name__ == "__main__":
    unittest.main()
