import unittest
import pandas as pd
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
import matplotlib.pyplot as plt
from scraper.poll_data_processor import PollDataProcessor


class TestPollDataProcessor(unittest.TestCase):
    def setUp(self):
        data = {
            'date': pd.date_range(start='2023-01-01', periods=10, freq='D'),
            'Candidate1': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            'Candidate2': [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
        }
        self.df = pd.DataFrame(data)
        self.processor = PollDataProcessor(self.df)
    
    def test_preprocess_data(self):
        candidates = ['Candidate1', 'Candidate2']
        processed_data = self.processor.preprocess_data(candidates)
        self.assertEqual(len(processed_data), len(candidates))
        self.assertTrue(all(isinstance(data, tuple) and len(data) == 2 for data in processed_data.values()))
    
    def test_fit_gaussian_process(self):
        x = np.array([[1], [2], [3]])
        y = np.array([0.1, 0.2, 0.3])
        model = self.processor.fit_gaussian_process(x, y)
        self.assertIsInstance(model, GaussianProcessRegressor)
    
    def test_predict_gaussian_process(self):
        model = GaussianProcessRegressor()
        x = np.array([[1], [2], [3]])
        y_pred, sigma = self.processor.predict_gaussian_process(model, x)
        self.assertEqual(len(y_pred), len(sigma))
    
    def test_calculate_moving_average(self):
        data_series = pd.Series([0.1, 0.2, 0.3, 0.4, 0.5])
        window_size = 3
        moving_average = self.processor.calculate_moving_average(data_series, window_size=window_size)
        self.assertEqual(len(moving_average), len(data_series))
    

if __name__ == '__main__':
    unittest.main()
