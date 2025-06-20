# =============================================================================
# server.py – Webhookserver för AIKryptoBot3 (Telegramknappar via ngrok)
# =============================================================================

from flask import Flask, request
from tools.telegram_manual_trade import handle_callback

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def telegram_webhook():
    try:
        data = request.json
        if "callback_query" in data:
            callback_data = data["callback_query"]["data"]
            print(f"[WEBHOOK] Inkommande knapp: {callback_data}")
            handle_callback(callback_data)
        return "OK"
    except Exception as e:
        print(f"[ERROR] Webhook-fel: {e}")
        return "ERROR", 500

if __name__ == "__main__":
    print("[OK] Webhookserver startad på http://localhost:5005")
    app.run(host="0.0.0.0", port=5005)
