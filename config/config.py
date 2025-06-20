# =============================================================================
# config.py – Gemensamma konfigurationsinställningar för AIKryptoBot3
# =============================================================================

import os

# === Telegram-inställningar ===
TELEGRAM_TOKEN = "7205234176:AAE9OYcNsmFHm0Nc40zZ9Q-y86nsU3B8FSY"
TELEGRAM_CHAT_ID = "1968695549"

# === Visningsgränser ===
MIN_USD_DISPLAY = 1.00
MIN_SELL_VALUE = 1.00

# === Coin-filter (används i hela systemet) ===
ACTIVE_COINS = ["BTC", "ETH", "ADA", "BNB", "XRP", "SOL", "DOT", "LTC"]

# === Dynamisk SWITCH_THRESHOLD från fil ===
def get_switch_threshold():
    path = os.path.join(os.path.dirname(__file__), "adaptive_thresholds.txt")
    if os.path.exists(path):
        with open(path, "r") as f:
            for line in f:
                if line.startswith("SWITCH_THRESHOLD"):
                    try:
                        return float(line.strip().split("=")[1])
                    except:
                        break
    return 0.75

# === Dynamisk MIN_BUY_SCORE från fil ===
def get_min_buy_score():
    path = os.path.join(os.path.dirname(__file__), "adaptive_thresholds.txt")
    if os.path.exists(path):
        with open(path, "r") as f:
            for line in f:
                if line.startswith("MIN_BUY_SCORE"):
                    try:
                        return float(line.strip().split("=")[1])
                    except:
                        break
    return 0.5

SWITCH_THRESHOLD = get_switch_threshold()
MIN_BUY_SCORE = get_min_buy_score()

# === Kapitalallokering (100% av USD-saldo) ===
CAPITAL_ALLOC_PCT = 1.0

# === Minsta tillåtna handelsvolym ===
MIN_TRADE_VOLUME = 0.0001

# === Stop-loss (aktivera/deaktivera) ===
ENABLE_STOPLOSS = True
