# =============================================================================
# start_webhook.py – Startar Flask-server och sätter webhook via ngrok
# =============================================================================

import os
import subprocess
import time
import webbrowser

# === Ändra sökväg om ngrok ligger på annan plats ===
NGROK_PATH = "https://e49f-188-149-236-45.ngrok-free.app"
PORT = 5005

# 1. Starta Flask-server
print("[START] Flask-server startas...")
os.system("start cmd /k python webhook/server.py")

# 2. Starta ngrok
print("[START] ngrok tunnlas...")
os.system(f"start cmd /k {NGROK_PATH} http {PORT}")

# 3. Vänta lite innan du kör set_webhook.py manuellt
print("\n[INFO] Vänta 5 sekunder och kör sedan: set_webhook.py")
