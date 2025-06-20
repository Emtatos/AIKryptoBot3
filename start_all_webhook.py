# =============================================================================
# start_all_webhook.py – Startar Flask, ngrok och sätter webhook automatiskt
# =============================================================================

import os
import time
import requests
from config.telegram_config import TELEGRAM_TOKEN

NGROK_PATH = "ngrok"  # Justera vid behov
PORT = 5005

# 1. Starta Flask-server
print("[1/3] Startar Flask-server i nytt fönster...")
os.system("start cmd /k python webhook/server.py")

# 2. Starta ngrok
print("[2/3] Startar ngrok i nytt fönster...")
os.system(f"start cmd /k {NGROK_PATH} http {PORT}")

# 3. Vänta på att ngrok ska bli tillgänglig
print("[INFO] Väntar på ngrok...")
time.sleep(6)

# 4. Hämta ngrok-url och sätt webhook
try:
    tunnels = requests.get("http://localhost:4040/api/tunnels").json()
    public_url = next(
        (tunnel["public_url"] for tunnel in tunnels["tunnels"] if tunnel["public_url"].startswith("https")),
        None
    )
    if not public_url:
        raise Exception("Ingen giltig tunnel hittades.")

    webhook_url = f"{public_url}/webhook"
    set_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"
    res = requests.get(set_url, params={"url": webhook_url})
    print(f"[3/3] Webhook satt till: {webhook_url}")
    print(res.json())
except Exception as e:
    print(f"[X] Misslyckades med att sätta webhook: {e}")
