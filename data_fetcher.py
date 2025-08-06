# data_fetcher.py

import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker, period="1y", interval="1d"):

    data = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=False)
    data.dropna(inplace=True)
    
    # Reset columns to single-level
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    
    return data


def fetch_multiple_stocks(tickers):
    """
    Fetch data for multiple stock symbols.
    :param tickers: List of stock symbols
    :return: Dictionary of DataFrames
    """
    all_data = {}
    for ticker in tickers:
        print(f"Fetching data for {ticker}...")
        df = fetch_stock_data(ticker)
        all_data[ticker] = df
    return all_data
