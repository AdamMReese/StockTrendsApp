"""
/*********************************************/
* Assignment: Final Project - Stock Trends App
* Author: Adam Reese
* Created: April 23, 2023
* Course: CIS 289 - Python II
* Program: PyCharm Professional
/*********************************************/
"""

import csv
import json
import tkinter as tk
from tkinter import ttk, messagebox

import requests
from alpha_vantage.timeseries import TimeSeries
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkcalendar import DateEntry

API_KEY = 'MZD1AXZWXXKO6JNC'


class StockTrendsApp(tk.Tk):
    """A tkinter application for displaying stock trends using Alpha Vantage API."""

    def __init__(self):
        super().__init__()

        # Set window title and size
        self.title("Stock Trends")
        self.geometry("800x600")

        # Create and pack UI elements
        self.stock_label = ttk.Label(self, text="Stock Symbol:")
        self.stock_label.pack(pady=10)

        self.stock_entry = ttk.Entry(self)
        self.stock_entry.pack(pady=10)

        self.company_label_text = tk.StringVar()
        self.company_label = ttk.Label(self, textvariable=self.company_label_text)
        self.company_label.pack(pady=10)

        self.date_label = ttk.Label(self, text="Date Span:")
        self.date_label.pack(pady=10)

        self.start_date_label = ttk.Label(self, text="Start Date:")
        self.start_date_label.pack(pady=5)

        self.start_date_entry = DateEntry(self)
        self.start_date_entry.pack(pady=5)

        self.end_date_label = ttk.Label(self, text="End Date:")
        self.end_date_label.pack(pady=5)

        self.end_date_entry = DateEntry(self)
        self.end_date_entry.pack(pady=5)

        self.plot_button = ttk.Button(self, text="Plot", command=self.plot_stock_data)
        self.plot_button.pack(pady=10)

        self.canvas = None

        # Add an export button for exporting stock data to a CSV file
        self.export_button = ttk.Button(self, text="Export CSV", command=self.export_stock_data_to_csv)
        self.export_button.pack(pady=10)

        # Initialize an instance variable to store the stock data
        self.stock_data = None

    def plot_stock_data(self):
        """Plot stock data based on the provided stock symbol and date range."""

        # Get user input values
        stock_symbol = self.stock_entry.get()
        company_name = self.get_company_name(stock_symbol)

        # Show an error message if the company name cannot be found
        if not company_name:
            tk.messagebox.showerror("Error", "Unable to retrieve the company name for the given stock symbol.")
            return

        # Update the company label text
        self.company_label_text.set(f"Company: {company_name}")

        # Get start and end dates as strings
        start_date = self.start_date_entry.get_date().strftime("%Y-%m-%d")
        end_date = self.end_date_entry.get_date().strftime("%Y-%m-%d")

        # Retrieve stock data using Alpha Vantage API
        ts = TimeSeries(key=API_KEY, output_format='pandas')
        data, _ = ts.get_daily_adjusted(symbol=stock_symbol, outputsize='full')

        # Sort the index before slicing
        data = data.sort_index(ascending=True)

        # Filter data based on the specified date range
        data = data[start_date.strip():end_date.strip()]

        # Calculate simple moving averages
        data['SMA50'] = data['4. close'].rolling(window=50).mean()
        data['SMA200'] = data['4. close'].rolling(window=200).mean()

        # Create a new figure and subplot
        fig = Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)

        # Plot stock data on the axes
        ax.plot(data.index, data['4. close'], label='Close')
        ax.plot(data.index, data['SMA50'], label='50-day SMA')
        ax.plot(data.index, data['SMA200'], label='200-day SMA')

        # Customize plot appearance
        ax.legend(loc='best')
        ax.set_title(f'#{stock_symbol} ({company_name}) Stock Trends')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.grid()

        # Remove the previous canvas if it exists
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        # Add a new canvas with the updated plot
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().pack()
        self.canvas = canvas

        # Store the stock data in the instance variable for later use
        self.stock_data = data

    def get_company_name(self, stock_symbol):
        """
        Get the company name for a given stock symbol using the Alpha Vantage API.

        Args:
            stock_symbol (str): The stock symbol to search for.

        Returns:
            str: The company name if found, None otherwise.
        """
        search_url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={stock_symbol}&apikey={API_KEY}"

        # Send a GET request to the search URL
        response = requests.get(search_url)

        # Check if the response is successful (status code 200)
        if response.status_code == 200:
            # Parse JSON response
            search_results = json.loads(response.text)
            matches = search_results.get("bestMatches", [])

            # Return the company name if there are any matches
            if len(matches) > 0:
                return matches[0]["2. name"]
            else:
                return None
        else:
            return None

    def export_stock_data_to_csv(self):
        # Check if there is any stock data available
        if self.stock_data is None:
            tk.messagebox.showerror("Error", "No stock data available. Please plot the stock data first.")
            return

        # Get the stock symbol and company name for the filename
        stock_symbol = self.stock_entry.get()
        company_name = self.get_company_name(stock_symbol)
        file_path = f"{stock_symbol}_{company_name}_stock_data.csv"

        # Open a new CSV file and write the stock data to it
        with open(file_path, "w", newline="") as csvfile:
            fieldnames = ["date", "open", "high", "low", "close", "adjusted_close", "volume", "dividend_amount",
                          "SMA50", "SMA200"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header row
            writer.writeheader()
            # Write stock data rows
            for date, row in self.stock_data.iterrows():
                writer.writerow({
                    "date": date,
                    "open": row["1. open"],
                    "high": row["2. high"],
                    "low": row["3. low"],
                    "close": row["4. close"],
                    "adjusted_close": row["5. adjusted close"],
                    "volume": row["6. volume"],
                    "dividend_amount": row["7. dividend amount"],
                    "SMA50": row["SMA50"],
                    "SMA200": row["SMA200"]
                })

        # Show a message box to inform the user that the export was successful
        tk.messagebox.showinfo("Export Successful", f"Stock data has been exported to {file_path}.")


if __name__ == "__main__":
    # Create and run the StockTrendsApp
    app = StockTrendsApp()
    app.mainloop()
