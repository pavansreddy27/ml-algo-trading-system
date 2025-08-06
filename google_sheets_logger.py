# google_sheets_logger.py

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file',
         'https://www.googleapis.com/auth/drive']

CREDENTIALS_FILE = 'credentials/credentials.json'  # Path to your credentials file
SHEET_NAME = 'Algo_Trade_Log'  # Replace with your actual Google Sheet name

def get_sheet():
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME)
    return sheet

def log_trade_to_sheet(ticker, signal_date, signal_type, price):
    try:
        sheet = get_sheet()

        try:
            log_tab = sheet.worksheet("Trade_Log")
        except gspread.exceptions.WorksheetNotFound:
            log_tab = sheet.add_worksheet(title="Trade_Log", rows="1000", cols="6")
            log_tab.append_row(["Date", "Stock", "Signal", "Price", "Logged_At"])

        log_tab.append_row([
            str(signal_date),
            ticker,
            signal_type,
            round(price, 2),
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ])
        print(f"✅ Logged {signal_type} for {ticker} on {signal_date}")
    
    except Exception as e:
        print("❌ Failed to log trade:", e)

def update_summary_tab():
    sheet = get_sheet()

    try:
        log_tab = sheet.worksheet("Trade_Log")
        summary_tab = sheet.worksheet("Summary")
    except gspread.exceptions.WorksheetNotFound:
        summary_tab = sheet.add_worksheet(title="Summary", rows="100", cols="2")
        summary_tab.update('A1:B1', [["Metric", "Value"]])
    
    records = log_tab.get_all_records()

    total_trades = len(records)
    total_wins = 0
    total_pnl = 0.0

    # Dummy logic: mark even-numbered trades as wins and simulate P&L
    for i, row in enumerate(records):
        price = float(row['Price'])
        if i % 2 == 0:
            total_wins += 1
            total_pnl += 100  # simulated profit
        else:
            total_pnl -= 50  # simulated loss

    win_ratio = (total_wins / total_trades) * 100 if total_trades > 0 else 0

    summary_data = [
        ["Total Trades", total_trades],
        ["Total Wins", total_wins],
        ["Win Ratio (%)", round(win_ratio, 2)],
        ["Total P&L", round(total_pnl, 2)]
    ]

    summary_tab.update('A2:B5', summary_data)
    print("✅ Updated Summary tab")

