# polls-scraper

This is a simple polls-scraper for reading polls data published in https://cdn-dev.economistdatateam.com/jobs/pds/code-test/index.html and print out two files `trend.csv` and `polls.csv` into the `data` directory. It also plots the trends using two methods: 

## 1) n-Day Moving Averages

The user can control the behavior of moving averages in the `main.py` in the line:

    processor.plot_moving_average_trends(candidates_to_analyze, window_size=10, outliers=True, save_to_csv=True)

where arguments `window_size` controls the average days, `outliers` controls the removal of outlier polling data and leaving `save_to_scv=True` creates the `trend.csv` otherwise it only plots the final results. For example, 10 Day Moving Average trend on polling data:

With `outliers=False`

![MovAve_fig](https://github.com/samanseifi/polls-scraper/assets/9206261/967735f9-533c-4969-ac2e-bf4ea5b7a3cb)

With `outliers=True`

![MovinAve_fig_cliped](https://github.com/samanseifi/polls-scraper/assets/9206261/8abe53a3-3274-4f65-b34d-e2fe2a2ccaf2)


## 2) Gaussian Process (Experimental)

This code also implements the Gaussian Process to fit a model to polling data. The implementation is simple, and does not write the trends into any files, however it generates a plot that shows the trend very well captured the trend of each candidates polls during the cycle (x-axis is how many days into cycle not the date). It nicely and automatically ignores the outliers that were implemented manually in n-Day Moving Average model. GP accounts for both the mean and the covariance structure of the data. In areas where the data is sparse or noisy, the GP fit might assign a higher uncertainty (larger standard deviation) to its predictions. Conversely, in areas with dense data or strong patterns, the GP fit can provide more precise estimates and a narrower standard deviation.
