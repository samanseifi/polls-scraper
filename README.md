# polls-scraper

This repository hosts a straightforward polls-scraper designed to extract polls data from https://cdn-dev.economistdatateam.com/jobs/pds/code-test/index.html. The scraper generates two essential files, `trend.csv` and `polls.csv`, both placed within the `data` directory. Additionally, it provides visualization of trends through two distinct methods:

## 1) n-Day Moving Averages

The behavior of the moving averages can be customized within the main.py file using the following line of code:

    processor.plot_moving_average_trends(candidates_to_analyze, window_size=10, outliers=True, save_to_csv=True)

In this line, the window_size argument determines the number of days for the moving average calculation, while the outliers argument controls whether outlier polling data is excluded. Setting save_to_csv=True generates the trend.csv file, otherwise, the script only generates visual plots. For instance, here is the result of a 10-Day Moving Average trend on polling data:

When `outliers=False`

![MovAve_fig](https://github.com/samanseifi/polls-scraper/assets/9206261/967735f9-533c-4969-ac2e-bf4ea5b7a3cb)

When `outliers=True`

![MovinAve_fig_cliped](https://github.com/samanseifi/polls-scraper/assets/9206261/8abe53a3-3274-4f65-b34d-e2fe2a2ccaf2)

In the provided examples, the first image demonstrates the trend without excluding outliers, while the second image showcases the trend after excluding them.

## 2) Gaussian Process (Experimental)

This codebase also features the utilization of Gaussian Process modeling to establish a trend within the polling data. The implementation follows a streamlined approach and **does not store the trends in any files.** Instead, it generates a plot that adeptly encapsulates the polling trends of individual candidates across the electoral cycle. Notably, the x-axis denotes the days into the cycle rather than specific dates. To control this process, navigate to the `main.py` script and locate the line:

    processor.plot_gaussian_process_trends(candidates_to_analyze)
    
This command requires no additional external arguments and operates solely on the data slated for analysis.

The method intrinsically addresses outliers that were manually managed within the **n-Day Moving Average model**. Gaussian Process (GP) fundamentally takes into account both the data's mean and its covariance structure. In scenarios where data points are sparse or subjected to noise, the GP fit allocates higher uncertainty, thus resulting in a wider standard deviation (Look at Chettam's trend). Conversely, in areas characterized by denser data or "pronounced patterns", the GP fit offers more accurate predictions with a narrower standard deviation.

![Figure_1](https://github.com/samanseifi/polls-scraper/assets/9206261/04f7c970-90f0-4e84-bcc4-60793694c2e1)

However, a detailed study on hyper parameters is required to achieve a robust model.

## Instruction to run the project

Setting up a virtual environment for this Python project:


Create a virtual environment using the following command:
   
   ```
   python3 -m venv poll_scraper
   ```

This will create a directory named `poll_scraper` which will contain your virtual environment.
   
Activate the virtual environment on macOS and Linux:

     ```
     source poll_scraper/bin/activate
     ```

Once the virtual environment is activated, you can install your project's dependencies. You can install them using:
   
   ```
   pip install -r requirements.txt
   ```

Now you can run your `main.py` script within the virtual environment. Any libraries you install using `pip` will be isolated to this environment.

When you're done working on your project, you can deactivate the virtual environment using the command:
   
   ```
   deactivate
   ```
