import yfinance as yf
import pandas as pd

# Get past stock price data
def get_stock(symbol, period="1mo", interval="1d"):
    try:
        stock_data = yf.download(symbol, period=period, interval=interval)
        if stock_data.empty:
            print("No data found for " + symbol)
            return None
        return stock_data
    except Exception as e:
        print("Error getting data: " + e)
        return None

if __name__ == "__main__":
    symbol = input("Enter stock symbol: ").upper()
    data = get_stock(symbol)

    if data is not None:
        print("\n Recent stock data:")
        print(data.tail())