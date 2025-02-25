import yfinance as yf
import pandas as pd
import os
import argparse
from datetime import datetime


# Get past stock price data
def get_stock(symbol, period="1mo", interval="1d"):
    try:
        stock_data = yf.download(symbol, period=period, interval=interval, auto_adjust=False)

        if stock_data.empty:
            print(f"No data found for {symbol}")
            return None

        # Ensure the index is in datetime format
        stock_data.index = pd.to_datetime(stock_data.index)

        return stock_data
    except Exception as e:
        print(f"Error getting data: {e}")
        return None


# Save stock data to CSV file
def save_to_csv(data, symbol):
    filename = f"{symbol}_stock_data.csv"

    # Save cleaned data
    data.to_csv(filename, float_format="%.6f")
    print(f"Data saved to {filename}")


# Load stock data from CSV if it exists
def load_from_csv(symbol):
    filename = f"{symbol}_stock_data.csv"
    if os.path.exists(filename):
        print(f"Loading data from {filename}")

        try:
            # Read CSV, skipping potential incorrect extra headers
            df = pd.read_csv(filename, index_col=0, parse_dates=True)
            # Ensure index is in datetime format
            df.index = pd.to_datetime(df.index[2:], errors="coerce", yearfirst=True)

            return df
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return None

    return None


# Check if new data needs to be added.
# If outdated, update by appending.
def update_stock(symbol, period="1mo", interval="1d"):
    current_data = load_from_csv(symbol)

    if current_data is not None:
        last_date = current_data.index[-1].date()
        today = datetime.today().date()

        if last_date >= today:
            print(f"Stock data for {symbol} is already up to date.")
            return current_data

        print(f"Getting new stock data for {symbol}...")
        new_data = get_stock(symbol, period, interval)

        if new_data is not None:
            updated_data = pd.concat([current_data, new_data]).drop_duplicates()
            save_to_csv(updated_data, symbol)
            return updated_data

    # Fetch new data if the file does not exist
    new_data = get_stock(symbol, period, interval)
    if new_data is not None:
        save_to_csv(new_data, symbol)
    return new_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retrieve and analyze stock data.")
    parser.add_argument("symbols", nargs="+", help="Stock ticker(s) to analyze")
    args = parser.parse_args()

    for symbol in args.symbols:
        symbol = symbol.upper()
        data = update_stock(symbol)

        if data is not None:
            print(f"\nRecent stock data for {symbol}:")
            print(data.tail())