import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
# from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
from sklearn.gaussian_process.kernels import Matern, ConstantKernel as C
import logging

class PollDataProcessor:
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.logger = self.setup_logger()  # Initialize the logger
    
    def setup_logger(self):
        # Set up logging configuration
        logger = logging.getLogger("poll_data_processor")
        logger.setLevel(logging.ERROR)
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        file_handler = logging.FileHandler('processor_error_log.txt')  # Log errors to a file
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        return logger

    def preprocess_data(self, candidates):
        processed_data = {}
        try:
            for candidate in candidates:
                candidate_data = self.dataframe[['date', candidate]].dropna()
                x = np.array((candidate_data['date'] - candidate_data['date'].min()).dt.days).reshape(-1, 1)
                y = np.array(candidate_data[candidate])
                processed_data[candidate] = (x, y)
        except Exception as e:
            self.logger.error(f"An error occurred while preprocessing data: {e}")  # Log the error
            raise e
        return processed_data

    def fit_gaussian_process(self, x, y):
        try:
            
            # Define the kernel (Matern kernel with nu=1.5)
            kernel = C(1.0, (1e-3, 1e3)) * Matern(length_scale=1.0, length_scale_bounds=(1e-2, 1e5), nu=5.5)

            model = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10, alpha=0.001)
            model.fit(x, y)
            return model
        except Exception as e:
            self.logger.error(f"An error occurred while fitting Gaussian Process: {e}")  # Log the error
            raise e

    def predict_gaussian_process(self, model, x):
        try:
            y_pred, sigma = model.predict(x, return_std=True)
            return y_pred, sigma
        except Exception as e:
            self.logger.error(f"An error occurred while predicting using Gaussian Process: {e}")  # Log the error
            raise e

    def calculate_moving_average(self, data_series, window_size, outliers=True):
        try:
            header = data_series.columns[1]
            
            data_series.set_index('date', inplace=True)          
            daily_data = data_series.resample('D').mean() # Resample data to daily frequency, filling missing values with NaN
            daily_data = daily_data.interpolate() # Interpolate missing values
            
            if outliers:
                # Clip outliers
                clipped_data = pd.DataFrame(index=daily_data.index)
                clipped_data[header] = daily_data[header].clip(lower=daily_data[header].quantile(0.01), upper=daily_data[header].quantile(0.99))
            else:  
                clipped_data = daily_data
                
            # Calculate the moving average and standard deviation for daily data
            moving_averages = clipped_data.rolling(window=window_size, min_periods=1).mean()
            std_deviations = clipped_data.rolling(window=window_size, min_periods=1).std()

            return moving_averages, std_deviations
        except Exception as e:
            self.logger.error(f"An error occurred while calculating moving average: {e}")  # Log the error
            raise e

    def plot_polling_data(self, x, y_actual, x_mapped, y_pred, sigma, label, method, color):
        plt.plot(x, y_actual, marker='o', linestyle='', alpha=0.3, label=label, color=color)
        plt.plot(x_mapped, y_pred, linestyle='--', label=method, color=color)
        plt.fill_between(x_mapped, y_pred - 3*sigma, y_pred + 3*sigma, alpha=0.1, color=color)
        
    def plot_gaussian_process_trends(self, candidates):
        colors = ['blue', 'green', 'red', 'purple', 'brown', 'orange']  # Choose your desired colors
        processed_data = self.preprocess_data(candidates)

        plt.figure(figsize=(10, 6))
        try:
            for i, candidate in enumerate(candidates):
                x, y = processed_data[candidate]
                model = self.fit_gaussian_process(x, y)
                y_pred, sigma = self.predict_gaussian_process(model, x)
                self.plot_polling_data(x, y, x.flatten(), y_pred, sigma, candidate, method="Gaussian Process", color=colors[i])

            plt.xlabel('Date')
            plt.ylabel('Percentage')
            plt.title('Gaussian Process Regression Trends for Candidates')
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.grid(False)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig('figures/gaussian_process.png')
            plt.show()
        except Exception as e:
            self.logger.error(f"An error occurred while plotting Gaussian Process trends: {e}")  # Log the error
            raise e

    def plot_moving_average_trends(self, candidates, window_size, outliers=True, save_to_csv=True):
        colors = ['blue', 'green', 'red', 'purple', 'brown', 'orange']  # Choose your desired colors
        if save_to_csv:
            moving_averages_df = pd.DataFrame()
        
        plt.figure(figsize=(10, 6))
        try:
            for candidate in candidates:
                candidate_data = self.dataframe[['date', candidate]].dropna()
                moving_averages, std_deviations = self.calculate_moving_average(candidate_data, window_size=window_size, outliers=outliers)
                self.plot_polling_data(candidate_data.index, candidate_data[candidate], moving_averages.index, moving_averages.values.flatten(), std_deviations.values.flatten(), candidate, 'Moving Average', color=colors[candidates.index(candidate)])
                if save_to_csv:
                    moving_averages_df[candidate] = moving_averages      
            
            if save_to_csv:
                moving_averages_df.index = moving_averages.index  # Use the date index

                # save moving averages to csv
                moving_averages_df.to_csv('data/trend.csv', index=True) 
            
            plt.xlabel('Date')
            plt.ylabel('Percentage')
            plt.title(str(window_size)+'-day Moving Average Trends for Candidates')
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.grid(False)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig('figures/moving_average.png')
            plt.show()
        except Exception as e:
            self.logger.error(f"An error occurred while plotting moving average trends: {e}")  # Log the error
            raise e
