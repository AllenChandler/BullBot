import unittest
import os
from src.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    def setUp(self):
        self.tickers = ['AAPL']
        self.start_date = '2023-01-01'
        self.end_date = '2023-01-10'
        self.data_loader = DataLoader(self.tickers, self.start_date, self.end_date)
        self.raw_data_path = os.path.join('data', 'raw')

    def test_download_data(self):
        self.data_loader.download_data()
        for ticker in self.tickers:
            file_path = os.path.join(self.raw_data_path, f'{ticker}.csv')
            self.assertTrue(os.path.exists(file_path))
            print(f'Test passed: Data for {ticker} downloaded successfully.')

    def tearDown(self):
        # Clean up downloaded files after test
        for ticker in self.tickers:
            file_path = os.path.join(self.raw_data_path, f'{ticker}.csv')
            if os.path.exists(file_path):
                os.remove(file_path)

if __name__ == '__main__':
    unittest.main()
