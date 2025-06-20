# =============================================================================
# telegram.py – Skickar meddelanden till Telegram, med eller utan knappar
# =============================================================================

import os
import sys
import requests

# Robust projektrot
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.telegram_config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def send_telegram(message):
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        # "parse_mode": "Markdown"  # Avstängd tillfälligt pga fel vid specialtecken
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.ok:
            print("[TELEGRAM] Meddelande skickat.")
        else:
            print(f"[TELEGRAM-FEL] Status: {response.status_code} – {response.text}")
    except Exception as e:
        print(f"[TELEGRAM-FEL] {e}")

def send_telegram_with_buttons(message, buttons):
    url = f"{BASE_URL}/sendMessage"
    keyboard = {
        "inline_keyboard": [[{"text": txt, "callback_data": data}] for txt, data in buttons]
    }
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        # "parse_mode": "Markdown",
        "reply_markup": keyboard
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.ok:
            print("[TELEGRAM] Meddelande med knappar skickat.")
        else:
            print(f"[TELEGRAM-FEL] {response.status_code} – {response.text}")
    except Exception as e:
        print(f"[TELEGRAM-FEL] {e}")
