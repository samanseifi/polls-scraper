import unittest
import pandas as pd
import numpy as np
from unittest.mock import Mock
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
import matplotlib.pyplot as plt

from scraper.poll_data_processor import PollDataProcessor

class TestPollDataProcessor(unittest.TestCase):
    def setUp(self):
        data = {
            'date': pd.date_range(start='2023-01-01', periods=10, freq='D'),
            'Candidate1': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        }
        self.df = pd.DataFrame(data)
        self.processor = PollDataProcessor(self.df)
    
    def test_preprocess_data(self):
        candidates = ['Candidate1']
        processed_data = self.processor.preprocess_data(candidates)
        self.assertEqual(len(processed_data), 1)
        self.assertIn('Candidate1', processed_data)
        self.assertTrue(isinstance(processed_data['Candidate1'][0], np.ndarray))
        self.assertTrue(isinstance(processed_data['Candidate1'][1], np.ndarray))
    
    def test_fit_gaussian_process(self):
        x = np.array([[1], [2], [3]])
        y = np.array([0.1, 0.2, 0.3])
        model = self.processor.fit_gaussian_process(x, y)
        self.assertIsNotNone(model)
    
    def test_predict_gaussian_process(self):
        model = Mock()
        model.predict.return_value = (np.array([0.2]), np.array([0.02]))
        x = np.array([[4]])
        y_pred, sigma = self.processor.predict_gaussian_process(model, x)
        self.assertTrue(np.allclose(y_pred, np.array([0.2])))
        self.assertTrue(np.allclose(sigma, np.array([0.02])))
    
    # Add more tests for other methods...

if __name__ == '__main__':
    unittest.main()