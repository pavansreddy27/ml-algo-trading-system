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

    # Messages to send in Telegram
    signals_message = "📢 *Trading Signals:*\n\n"
    ml_summary_message = "📊 *ML Predictions:*\n\n"

    for symbol, df in stock_data.items():
        print(f"\n--- {symbol} ---")

        # 1️⃣ Generate Trading Signals
        df_signals = generate_trade_signals(df)
        print(df_signals[['Close', 'RSI', '20MA', '50MA', 'Signal']].tail(5))

        for i in range(len(df_signals)):
            signal = df_signals.iloc[i]['Signal']
            if signal in ['BUY', 'SELL']:
                signal_type = signal
                signal_date = df_signals.index[i]
                price = df_signals.iloc[i]['Close']

                

        # 2️⃣ Run ML Prediction
        try:
            _, acc, pred = train_ml_model(df)
            prediction_text = "UP" if pred == 1 else "DOWN"

            print(f"✅ ML Model Accuracy: {round(acc*100, 2)}%")
            print(f"📈 Next-day Prediction: {prediction_text}")

            ml_summary_message += (
                f"--- {symbol} ---\n"
                f"✅ ML Model Accuracy: {round(acc*100, 2)}%\n"
                f"📈 Next-day Prediction: {prediction_text}\n\n"
            )

        except Exception as e:
            print(f"❌ Error training ML model for {symbol}: {e}")

    # 3️⃣ Update Google Sheets Summary
    update_summary_tab()

    # 4️⃣ Send all results to Telegram
    final_message = signals_message + "\n" + ml_summary_message
    send_telegram_message(final_message)
