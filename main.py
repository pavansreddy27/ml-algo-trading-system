# main.py

from data_fetcher import fetch_multiple_stocks
from strategy import generate_trade_signals
from google_sheets_logger import log_trade_to_sheet, update_summary_tab
from telegram_alerts import send_telegram_message
from ml_model import train_ml_model

# List of stock tickers to track
tickers = ['INDUSINDBK.NS', 'ADANIENT.NS', 'TATASTEEL.NS']

if __name__ == "__main__":
    stock_data = fetch_multiple_stocks(tickers)

    for symbol, df in stock_data.items():
        print(f"\n--- {symbol} ---")

        # 1️⃣ Generate Technical Indicators & Signals
        df_signals = generate_trade_signals(df)
        print("\n📊 Last 5 rows with Indicators & Signals:")
        print(df_signals[['Close', 'RSI', '20MA', '50MA', 'Signal']].tail(5))

        # 2️⃣ PRICE-BASED SIGNAL (for Telegram)
        if len(df) < 2:
            print(f"Not enough data for {symbol}")
            continue

        close_today = float(df['Close'].iloc[-1])
        close_prev = float(df['Close'].iloc[-2])
        signal_date = df.index[-1]

        if close_today > close_prev:
            signal_type = "BUY"
            emoji = "🟢"
        else:
            signal_type = "SELL"
            emoji = "🔴"

        # Log to Google Sheets
        log_trade_to_sheet(symbol, signal_date, signal_type, close_today)

        # Telegram message
        message = (
            f"> Algo Trading Bot:\n"
            f"{emoji} {signal_type} Signal Alert!\n\n"
            f"Stock: {symbol}\n"
            f"Date: {signal_date.strftime('%Y-%m-%d')}\n"
            f"Price: ₹{round(close_today, 2)}"
        )
        send_telegram_message(message)

        # 3️⃣ ML MODEL PREDICTION (console only)
        try:
            _, acc, pred = train_ml_model(df)
            prediction_text = "UP" if pred == 1 else "DOWN"
            print(f"✅ ML Model Accuracy: {round(acc*100, 2)}%")
            print(f"📈 Next-day Prediction: {prediction_text}")
        except Exception as e:
            print(f"❌ Error training ML model for {symbol}: {e}")

    # 4️⃣ Update Google Sheets Summary
    update_summary_tab()
