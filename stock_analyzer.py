import yfinance as yf
import pandas as pd
import os

# Get past stock price data
def get_stock(symbol, period="1mo", interval="1d"):
    try:
        stock_data = yf.download(symbol, period=period, interval=interval)
        if stock_data.empty:
            print(f"No data found for {symbol}")
            return None
        return stock_data
    except Exception as e:
        print(f"Error getting data: {e}")
        return None

# Save stock to csv file
def save_to_csv(data, symbol):
    filename = f"{symbol}_stock_data.csv"
    data.to_csv(filename, float_format="%.6f")
    print(f"Data saved to {filename}")

# Load stock from csv if it exists
def load_from_csv(symbol):
    filename = f"{symbol}_stock_data.csv"
    if os.path.exists(filename):
        print(f"Loading data from {filename}")
        return pd.read_csv(filename, index_col=0, parse_dates=True, date_format="%Y-%m-%d")
    return None

if __name__ == "__main__":
    symbol = input("Enter stock symbol: ").upper()
    data = load_from_csv(symbol)

    if data is None:
        data = get_stock(symbol)
        if data is not None:
            save_to_csv(data, symbol)

    if data is not None:
        print("\n Recent stock data:")
        print(data.tail())