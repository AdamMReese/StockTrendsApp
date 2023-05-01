# Stock Trends Analysis App

## Description
This is a Python-based application developed for a Python II class final project. The application integrates with the Alpha Vantage API to provide real-time stock market data. It allows users to visualize stock performance over a user-defined period and export the data into a CSV file for further analysis.

## Features
- Fetch real-time stock market data from Alpha Vantage API
- Visualization of stock performance over a selected period
- Export stock market data into CSV format
- The application shows various stock market data points such as opening price, closing price, adjusted closing price, volume, dividend amount, and 50-day and 200-day Simple Moving Averages (SMA)

## Setup and Installation
1. Clone this repository to your local machine
2. Install the required Python packages listed in the `requirements.txt` file by running `pip install -r requirements.txt`
3. Make sure you have an API key from Alpha Vantage. You can get one [here](https://www.alphavantage.co/support/#api-key)
4. Add your Alpha Vantage API key as an environment variable with the key name "MZD1AXZWXXKO6JNC"

## Usage
Run the `StockTrendsApp.py` file to start the application. Enter a stock symbol and select a date range, then click 'Plot' to see the stock trend. Click 'Generate CSV' to save the stock data to a CSV file.

## Project Status
This project is complete and fully functional. Future updates might include additional stock analysis features and improvements based on user feedback.

## Contributing
While this project is mainly for educational purposes, suggestions and contributions are welcome. Feel free to open an issue or make a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
