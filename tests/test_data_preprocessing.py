import unittest
import os
import pandas as pd
from src.data_preprocessing import DataPreprocessor

class TestDataPreprocessor(unittest.TestCase):
    def setUp(self):
        self.raw_data_path = os.path.join('data', 'raw')
        self.processed_data_path = os.path.join('data', 'processed')
        self.preprocessor = DataPreprocessor(self.raw_data_path, self.processed_data_path)
        
        # Create a sample raw data file
        sample_data = pd.DataFrame({
            'Date': pd.date_range(start='2023-01-01', periods=5),
            'Close': [150, 152, None, 155, 157]
        })
        os.makedirs(self.raw_data_path, exist_ok=True)
        sample_data.to_csv(os.path.join(self.raw_data_path, 'AAPL.csv'), index=False)

    def test_preprocess_data(self):
        self.preprocessor.preprocess_data()
        processed_file_path = os.path.join(self.processed_data_path, 'AAPL.csv')
        self.assertTrue(os.path.exists(processed_file_path))
        df = pd.read_csv(processed_file_path)
        self.assertFalse(df.isnull().values.any())
        print('Test passed: Preprocessed data contains no NaN values.')

    def tearDown(self):
        # Clean up files
        raw_file = os.path.join(self.raw_data_path, 'AAPL.csv')
        processed_file = os.path.join(self.processed_data_path, 'AAPL.csv')
        if os.path.exists(raw_file):
            os.remove(raw_file)
        if os.path.exists(processed_file):
            os.remove(processed_file)

if __name__ == '__main__':
    unittest.main()
