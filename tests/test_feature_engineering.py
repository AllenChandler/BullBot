import unittest
import os
import pandas as pd
from src.feature_engineering import FeatureEngineer

class TestFeatureEngineer(unittest.TestCase):
    def setUp(self):
        self.processed_data_path = os.path.join('data', 'processed')
        self.features_data_path = os.path.join('data', 'features')
        self.feature_engineer = FeatureEngineer(self.processed_data_path, self.features_data_path)
        
        # Create a sample processed data file
        sample_data = pd.DataFrame({
            'Date': pd.date_range(start='2023-01-01', periods=10),
            'Close': [150, 152, 154, 153, 155, 157, 159, 158, 160, 162]
        })
        os.makedirs(self.processed_data_path, exist_ok=True)
        sample_data.to_csv(os.path.join(self.processed_data_path, 'AAPL.csv'), index=False)

    def test_engineer_features(self):
        self.feature_engineer.engineer_features()
        features_file_path = os.path.join(self.features_data_path, 'AAPL.csv')
        self.assertTrue(os.path.exists(features_file_path))
        df = pd.read_csv(features_file_path)
        # Check if the new features are created
        self.assertIn('Return', df.columns)
        self.assertIn('RollingMean', df.columns)
        self.assertIn('RollingStd', df.columns)
        self.assertIn('Momentum', df.columns)
        print('Test passed: Feature engineering added all expected features.')

    def tearDown(self):
        # Clean up files
        processed_file = os.path.join(self.processed_data_path, 'AAPL.csv')
        features_file = os.path.join(self.features_data_path, 'AAPL.csv')
        if os.path.exists(processed_file):
            os.remove(processed_file)
        if os.path.exists(features_file):
            os.remove(features_file)

if __name__ == '__main__':
    unittest.main()
