# main.py

from data_fetcher import fetch_multiple_stocks
from strategy import generate_trade_signals
from google_sheets_logger import log_trade_to_sheet, update_summary_tab
from telegram_alerts import send_telegram_message
from ml_model import train_ml_model

tickers = ['INDUSINDBK.NS', 'ADANIENT.NS', 'TATASTEEL.NS']

if __name__ == "__main__":
    stock_data = fetch_multiple_stocks(tickers)

    for symbol, df in stock_data.items():
        print(f"\n--- {symbol} ---")

        # Generate signals
        df_signals = generate_trade_signals(df)

        # ✅ Force a dummy BUY signal for testing 
        #df_signals.at[df_signals.index[-1], 'Signal'] = 'BUY'


        # 🔍 Print last few rows with indicators
        print(df_signals[['Close', 'RSI', '20MA', '50MA', 'Signal']].tail(10))

        # ✅ Handle signals: BUY or SELL
        for i in range(len(df_signals)):
            signal = df_signals.iloc[i]['Signal']
            if signal in ['BUY', 'SELL']:
                signal_type = signal
                signal_date = df_signals.index[i]
                price = df_signals.iloc[i]['Close']

                # Log to Sheets
                log_trade_to_sheet(symbol, signal_date, signal_type, price)

                # Send Telegram Alert
                emoji = "🟢" if signal_type == "BUY" else "🔴"
                message = (
                    f"{emoji} *{signal_type} Signal Alert!*\n\n"
                    f"*Stock:* {symbol}\n"
                    f"*Date:* {signal_date.strftime('%Y-%m-%d')}\n"
                    f"*Price:* ₹{round(price, 2)}"
                )
                send_telegram_message(message)


    # 📊 Update Summary Tab
    update_summary_tab()

    # 🤖 Run ML Predictions
    print("\n📊 ML Predictions:")
    for symbol, df in stock_data.items():
        print(f"\n--- {symbol} ---")
        try:
            _, acc, pred = train_ml_model(df)
        except Exception as e:
            print(f"❌ Error training ML model for {symbol}: {e}")
