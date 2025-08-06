# 📈 ML-Based Algo-Trading System with Automation & Telegram Alerts

An automated stock trading analysis system that:

* Fetches real-time stock market data
* Applies technical indicators (RSI, Moving Averages)
* Generates **Buy/Sell signals**
* Uses **Machine Learning** (Logistic Regression) to predict next-day trends
* Sends **Telegram alerts**
* Logs all trades into **Google Sheets** for performance tracking

---

## 🚀 Features

* ✅ Automated technical indicator calculation (RSI, 20-day MA, 50-day MA)
* 🤖 ML-based next-day prediction using Logistic Regression
* 📱 Instant Telegram alerts for Buy/Sell signals
* 🧾 Trade logging to Google Sheets
* 📊 Summary tab for performance stats (P\&L, Win Ratio, etc.)
* 🔐 Environment-friendly: `.gitignore` and secure credentials management

---

## 🧠 ML Model

* **Model**: Logistic Regression
* **Inputs**: RSI, 20MA, 50MA
* **Output**: Predicted trend (UP / DOWN)
* **Accuracy**: Varies by stock — shown in the summary
* **Training Data**: Last 15 days’ features & next-day movement as label

---

## 🛠️ Technologies Used

| Component          | Technology                   |
| ------------------ | ---------------------------- |
| Data Source        | Yahoo Finance via `yfinance` |
| ML Model           | `scikit-learn`               |
| Automation         | Python + Scheduler           |
| Messaging          | Telegram Bot                 |
| Logging            | Google Sheets via `gspread`  |
| Scripting Language | Python 3.10+                 |
| Environment Config | `.env`, `.gitignore`         |

---

## 📂 Folder Structure

```
.
├── main.py                     # Main script to run everything
├── telegram_alerts.py          # Telegram messaging logic
├── google_sheets_logger.py     # Google Sheets logging
├── signal_generator.py         # Signal logic with RSI + MA crossover
├── ml_model.py                 # ML model training and prediction
├── credentials/
│   └── credentials.json        # 🔒 Your Google credentials (ignored by git)
├── .env                        # Contains TELEGRAM_TOKEN, etc.
├── .gitignore                  # Ensures credentials are not committed
└── README.md
```

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/ml-algo-trading-system.git
cd ml-algo-trading-system
```

### 2. Install requirements

```bash
pip install -r requirements.txt
```

### 3. Setup Telegram Alerts

* Create a Telegram bot from [BotFather](https://t.me/BotFather)
* Copy the `BOT TOKEN`
* Get your Telegram `CHAT ID` from [userinfobot](https://t.me/userinfobot)
* Create a `.env` file:

```env
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

### 4. Setup Google Sheets

* Go to [Google Cloud Console](https://console.cloud.google.com)
* Create a project → Enable Google Sheets + Drive API
* Create a **Service Account**, download the JSON key
* Place it in `credentials/credentials.json`
* Share your Google Sheet with the email in the service account

---

## ✅ Running the Bot

```bash
python main.py
```

You'll see:

* 📈 Buy/Sell signals printed for each stock
* 📊 ML accuracy and prediction (UP/DOWN)
* 🟢 Telegram alerts sent
* 📄 Trades logged to Google Sheets
* 📋 Summary tab auto-updated with win ratio, P\&L

---

## 📊 Example Output

```
--- RELIANCE.NS ---
📅 ML Model Accuracy: 61.5%
📈 Next-day Prediction: UP
🟢 BUY Signal Alert!
Date: 2025-08-06 | Price: ₹1392.8

📄 Logged BUY to Google Sheets
📋 Summary tab updated
```

---

## 🛡️ Security

* `.gitignore` ensures `credentials/credentials.json` is not committed

  * Use [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/) or `git filter-branch`
* Always rotate and regenerate credentials after exposure

---

## 🧠 Credits

* [yfinance](https://github.com/ranaroussi/yfinance)
* [gspread](https://github.com/burnash/gspread)
* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

---

## 📄 License

This project is licensed under the MIT License.

---

## 📬 Contact

* Created by [Pavan S Reddy](https://github.com/pavansreddy27)
