# strategy.py

import pandas as pd
import numpy as np
import ta  # technical analysis library

def calculate_indicators(df):
    """
    Adds RSI, 20-day MA, and 50-day MA to the DataFrame
    """
    df = df.copy()
    df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
    df['20MA'] = df['Close'].rolling(window=20).mean()
    df['50MA'] = df['Close'].rolling(window=50).mean()
    return df

def generate_trade_signals(df):
    df = calculate_indicators(df)
    df['Signal'] = None

    for i in range(1, len(df)):
        rsi = df.loc[df.index[i], 'RSI']
        ma_20 = df.loc[df.index[i], '20MA']
        ma_50 = df.loc[df.index[i], '50MA']
        prev_ma_20 = df.loc[df.index[i - 1], '20MA']
        prev_ma_50 = df.loc[df.index[i - 1], '50MA']

        # BUY Signal
        if pd.notnull(rsi) and rsi < 30 and pd.notnull(ma_20) and pd.notnull(ma_50) and prev_ma_20 < prev_ma_50 and ma_20 > ma_50:
            df.at[df.index[i], 'Signal'] = 'BUY'

        # SELL Signal — opposite crossover + RSI > 70
        if pd.notnull(rsi) and rsi > 70 and pd.notnull(ma_20) and pd.notnull(ma_50) and prev_ma_20 > prev_ma_50 and ma_20 < ma_50:
            df.at[df.index[i], 'Signal'] = 'SELL'
    
    return df
