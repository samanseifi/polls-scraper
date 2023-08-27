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
        
    @patch("scraper.poll_data_scraper.requests.get")
    def test_extract_column_order(self, mock_get):
        # Define the HTML content with the table header
        html_content = """
        <table>
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Pollster</th>
                    <th>Sample</th>
                    <th>Bulstrode</th>
                    <th>Lydgate</th>
                    <th>Vincy</th>
                    <th>Casaubon</th>
                    <th>Chettam</th>
                    <th>Others</th>
                </tr>
            </thead>
            <tbody>
                <!-- ... -->
            </tbody>
        </table>
        """

        # Set up the mock response
        mock_response = unittest.mock.Mock()
        mock_response.content = html_content.encode("utf-8")
        mock_get.return_value = mock_response

        # Create the scraper instance
        scraper = PollDataScraper("https://cdn-dev.economistdatateam.com/jobs/pds/code-test/index.html")
        scraper.fetch_page()

        # Extract the column order
        column_order = scraper.extract_column_order()

        # Define the expected column order
        expected_column_order = [
            "Bulstrode", "Lydgate", "Vincy", "Casaubon", "Chettam", "Others"
        ]

        # Check if the extracted column order matches the expected order
        self.assertEqual(column_order, expected_column_order)

    def test_clean_cell_percentage(self):
        cleaned_text = self.scraper.clean_cell("67.6%")
        self.assertAlmostEqual(float(cleaned_text), 0.6759, places=3)
    
    def test_clean_cell_number(self):
        cleaned_text = self.scraper.clean_cell("1,234*")
        self.assertEqual(cleaned_text, 1234)
        
        cleaned_text = self.scraper.clean_cell("1,235**")
        self.assertEqual(cleaned_text, 1235)
        
    def test_clean_cell_stars(self):
        cleaned_text = self.scraper.clean_cell("**")
        self.assertEqual(cleaned_text, "")

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
