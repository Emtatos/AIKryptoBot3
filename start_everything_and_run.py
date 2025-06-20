# =============================================================================
# start_full_sequence.py – Startar ngrok, Flask, sätter webhook och startar loop
# =============================================================================

import os
import time
import requests
from config.telegram_config import TELEGRAM_TOKEN

NGROK_PATH = "C:\\AIKryptoBot3\\ngrok\\ngrok.exe"  # Ändra om sökvägen är annorlunda
PORT = 5005

# 1. Starta ngrok i nytt fönster
print("[1/5] Startar ngrok i nytt kommandofönster...")
os.system(f'start cmd /k "cd /d {os.path.dirname(NGROK_PATH)} && ngrok.exe http {PORT}"')

# 2. Vänta tills ngrok är redo och ge URL
print("[2/5] Väntar på ngrok-tunnel...")
public_url = None
for attempt in range(20):
    try:
        tunnels = requests.get("http://localhost:4040/api/tunnels").json()
        public_url = next(
            (tunnel["public_url"] for tunnel in tunnels["tunnels"] if tunnel["public_url"].startswith("https")),
            None
        )
        if public_url:
            break
    except:
        pass
    print(f"[WAIT] ({attempt+1}/20) ngrok svarar inte ännu...")
    time.sleep(1.5)

# 3. Sätt webhook
if public_url:
    webhook_url = f"{public_url}/webhook"
    print(f"[3/5] Sätter webhook till: {webhook_url}")
    try:
        api = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"
        res = requests.get(api, params={"url": webhook_url})
        print(f"[OK] Webhook registrerad: {res.json()}")
    except Exception as e:
        print(f"[X] Misslyckades med att sätta webhook: {e}")
else:
    print("[X] Ingen giltig ngrok-tunnel hittades. Avbryter.")
    exit()

# 4. Starta Flask-server
print("[4/5] Startar Flask-server i nytt fönster...")
os.system("start cmd /k python webhook/server.py")

# 5. Starta dynamic_scheduler.py i separat fönster
print("[5/5] Startar dynamic_scheduler.py i loop...")
os.system("start cmd /k python scheduler/dynamic_scheduler.py")
