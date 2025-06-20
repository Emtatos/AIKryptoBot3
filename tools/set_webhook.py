# =============================================================================
# set_webhook.py – Registrerar Telegram-webhook till aktiv ngrok-länk
# =============================================================================

import requests
from config.telegram_config import TELEGRAM_TOKEN

# === ÄNDRA DENNA till din aktiva ngrok-adress ===
NGROK_URL = "https://7392-188-149-236-45.ngrok-free.app"

# === Full webhookadress ===
WEBHOOK_URL = f"{NGROK_URL}/webhook"
API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"

try:
    response = requests.get(API_URL, params={"url": WEBHOOK_URL}, timeout=10)
    print(f"[OK] Webhook svar: {response.status_code}")
    print(response.json())
except Exception as e:
    print(f"[X] Kunde inte sätta webhook: {e}")
