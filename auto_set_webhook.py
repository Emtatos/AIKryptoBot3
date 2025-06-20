# =============================================================================
# auto_set_webhook.py – Sätter Telegram-webhook automatiskt från ngrok-status
# =============================================================================

import requests
from config.telegram_config import TELEGRAM_TOKEN

# 1. Läs ngrok aktiv tunnel
try:
    ngrok_data = requests.get("http://localhost:4040/api/tunnels").json()
    public_url = None
    for tunnel in ngrok_data.get("tunnels", []):
        if tunnel.get("public_url", "").startswith("https"):
            public_url = tunnel["public_url"]
            break
except Exception as e:
    print(f"[X] Kunde inte hämta ngrok-URL: {e}")
    public_url = None

# 2. Sätt webhook
if public_url:
    webhook_url = f"{public_url}/webhook"
    api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"
    try:
        res = requests.get(api_url, params={"url": webhook_url})
        print(f"[OK] Webhook satt till: {webhook_url}")
        print(res.json())
    except Exception as e:
        print(f"[X] Fel vid webhookregistrering: {e}")
else:
    print("[X] Ingen giltig ngrok-URL hittades.")
