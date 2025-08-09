# ml_model.py

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from ta.momentum import RSIIndicator
from ta.trend import MACD

def prepare_features(df):
    df = df.copy()

    df['RSI'] = RSIIndicator(close=df['Close'], window=14).rsi()
    macd = MACD(close=df['Close'])
    df['MACD'] = macd.macd()
    df['MACD_signal'] = macd.macd_signal()

    df['20MA'] = df['Close'].rolling(window=20).mean()
    df['50MA'] = df['Close'].rolling(window=50).mean()

    df['Volume'] = df['Volume']
    
    # Label: 1 if next day's close is higher, else 0
    df['Target'] = np.where(df['Close'].shift(-1) > df['Close'], 1, 0)

    df.dropna(inplace=True)
    return df

def train_ml_model(df):
    df = prepare_features(df)

    X = df[['RSI', 'MACD', 'MACD_signal', '20MA', '50MA', 'Volume']]
    y = df['Target']

    # Split: last 10% for test
    split = int(len(df) * 0.9)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    # Predict latest signal
    latest_features = X.iloc[-1].values.reshape(1, -1)
    latest_df = pd.DataFrame(latest_features, columns=X.columns)
    prediction = model.predict(latest_df)[0]

    return model, accuracy, prediction
