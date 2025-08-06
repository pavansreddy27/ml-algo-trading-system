# telegram_alerts.py

import requests

# Replace these with your actual values
TELEGRAM_BOT_TOKEN = "8249631629:AAECKBPI9Peoh0MBrN6yBwiY7QdyLWUBlyM"
TELEGRAM_CHAT_ID = "1301565888"

def send_telegram_message(message: str):
    """
    Sends a message to your Telegram bot.
    """
    try:
        url = f"https://api.telegram.org/bot8249631629:AAECKBPI9Peoh0MBrN6yBwiY7QdyLWUBlyM/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }

        response = requests.post(url, data=payload)

        if response.status_code == 200:
            print("✅ Telegram message sent.")
        else:
            print(f"❌ Failed to send message: {response.text}")
    
    except Exception as e:
        print(f"❌ Telegram send error: {e}")
