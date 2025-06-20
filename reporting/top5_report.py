# =============================================================================
# top5_report.py – Skickar Topp 5 coins till Telegram med score och dynamisk SL
# =============================================================================

import os
import sys
import pandas as pd
from reporting.telegram import send_telegram

# Robust projektrot
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Stop-loss param (version 10)
volatility_factor = 50
min_pct = 0.01
max_pct = 0.03

def calculate_stoploss(score):
    vol = abs(score) / 100
    return round(min(max(vol * volatility_factor, min_pct), max_pct), 4)

def send_top5():
    path = os.path.join(project_root, "data", "momentum_combined.csv")
    if not os.path.exists(path):
        send_telegram("⚠️ momentum_combined.csv saknas.")
        return

    df = pd.read_csv(path)
    if df.empty or "symbol" not in df.columns or "score" not in df.columns:
        send_telegram("⚠️ momentum_combined.csv är tom eller felaktig.")
        return

    df = df.sort_values("score", ascending=False).head(5)

    message = "📊 Topp 5 med dynamisk stop-loss (%):\n"
    for i, row in enumerate(df.itertuples(), 1):
        symbol = row.symbol
        score = round(row.score, 2)
        stop_pct = round(calculate_stoploss(row.score) * 100, 2)
        message += f"{i}. {symbol} (score: {score}) (stop loss: {stop_pct}%)\n"

    send_telegram(message)

# =============================================================================
# TEST
# =============================================================================
if __name__ == "__main__":
    send_top5()
