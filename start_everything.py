# =============================================================================
# start_everything.py – Startar Flask-server, ngrok och påminner om webhook
# =============================================================================

import os
import time
import subprocess

# Ändra vid behov om ngrok.exe ligger i annan mapp
NGROK_PATH = "ngrok"  # eller t.ex. "C:/AIKryptoBot3/ngrok/ngrok.exe"
PORT = 5005

print("[1/3] Startar Flask-server i nytt fönster...")
os.system("start cmd /k python webhook/server.py")

time.sleep(2)
print("[2/3] Startar ngrok i nytt fönster...")
os.system(f"start cmd /k {NGROK_PATH} http {PORT}")

print("\n[3/3] Kontrollera att din ngrok-URL är korrekt i set_webhook.py")
print("→ Kör sedan set_webhook.py när ngrok är igång.")
