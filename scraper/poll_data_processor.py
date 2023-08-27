import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C

class PollDataProcessor:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def preprocess_data(self, candidates):
        processed_data = {}
        for candidate in candidates:
            candidate_data = self.dataframe[['date', candidate]].dropna()
            x = np.array((candidate_data['date'] - candidate_data['date'].min()).dt.days).reshape(-1, 1)
            y = np.array(candidate_data[candidate])
            processed_data[candidate] = (x, y)
        return processed_data

    def fit_gaussian_process(self, x, y):
        kernel = C(1.0, (1e-3, 1e3)) * RBF(1.0, (1e-2, 1e2))
        model = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10, alpha=0.001)
        model.fit(x, y)
        return model

    def predict_gaussian_process(self, model, x):
        y_pred, sigma = model.predict(x, return_std=True)
        return y_pred, sigma

    def calculate_moving_average(self, data_series, window_size=7):
        return data_series.rolling(window=window_size, min_periods=1).mean()

    def plot_polling_data(self, x, y_actual, y_pred, sigma, label, method, color):
        plt.plot(x, y_actual, marker='o', linestyle='', alpha=0.3, label=label, color=color)
        plt.plot(x, y_pred, linestyle='--', label=method, color=color)
        if method == 'Gaussian Process':
            plt.fill_between(x.flatten(), y_pred - 3*sigma, y_pred + 3*sigma, alpha=0.3, color=color)
    
    def plot_gaussian_process_trends(self, candidates):
        colors = ['blue', 'green', 'red', 'purple', 'brown', 'orange']  # Choose your desired colors
        processed_data = self.preprocess_data(candidates)

        plt.figure(figsize=(10, 6))
        for i, candidate in enumerate(candidates):
            x, y = processed_data[candidate]
            model = self.fit_gaussian_process(x, y)
            y_pred, sigma = self.predict_gaussian_process(model, x)
            self.plot_polling_data(x, y, y_pred, sigma, candidate, method="Gaussian Process", color=colors[i])


        plt.xlabel('Date')
        plt.ylabel('Percentage')
        plt.title('Gaussian Process Regression Trends for Candidates')
        plt.legend()
        plt.grid(False)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_moving_average_trends(self, candidates, window_size):
        colors = ['blue', 'green', 'red', 'purple', 'brown', 'orange']  # Choose your desired colors

        plt.figure(figsize=(10, 6))
        for candidate in candidates:
            candidate_data = self.dataframe[['date', candidate]].dropna()
            candidate_data = candidate_data.set_index('date')
            rolling_average = self.calculate_moving_average(candidate_data[candidate], window_size=window_size)
            self.plot_polling_data(candidate_data.index, candidate_data[candidate], rolling_average, None, candidate, 'Moving Average', color=colors[candidates.index(candidate)])

        plt.xlabel('Date')
        plt.ylabel('Percentage')
        plt.title(str(window_size)+'-day Moving Average Trends for Candidates')
        plt.legend()
        plt.grid(False)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

