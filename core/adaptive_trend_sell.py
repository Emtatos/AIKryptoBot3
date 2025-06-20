# =============================================================================
# adaptive_trend_sell.py – Justerar förtroendet för trendbaserade sälj
# =============================================================================

import os
import sys
import pandas as pd
from datetime import datetime, timedelta

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

log_path = os.path.join(project_root, "logs", "trend_sell_accuracy.csv")
out_path = os.path.join(project_root, "config", "trend_sell_confidence.txt")

from core.broker_kraken import KrakenBroker
broker = KrakenBroker()

MIN_SELL_VALUE = 1.0  # USD

def adjust_trend_sell_confidence():
    if not os.path.exists(log_path):
        print("[INFO] trend_sell_accuracy.csv saknas.")
        return

    df = pd.read_csv(log_path, parse_dates=["timestamp"])
    if df.empty or len(df) < 5:
        print("[INFO] För få datapunkter för att justera trend-sälj.")
        return

    df = df.sort_values("timestamp", ascending=False).head(20)  # Senaste 20
    sell_df = df[df["signal"] == "SELL"]
    if sell_df.empty:
        print("[INFO] Inga trend-säljposter att analysera.")
        return

    # Filtrera bort innehav som är mindre än $1 i värde vid sälj
    filtered = []
    for _, row in sell_df.iterrows():
        symbol = row.get("symbol")
        qty = row.get("amount", 0)
        price = broker.get_price(symbol)
        if symbol and price and qty * price >= MIN_SELL_VALUE:
            filtered.append(row)

    if not filtered:
        print("[INFO] Inga relevanta SELL-poster över $1.")
        return

    filtered_df = pd.DataFrame(filtered)
    hit_rate = filtered_df["hit_rate_%"].mean() / 100
    confidence = round(min(max(hit_rate, 0.1), 1.0), 2)

    with open(out_path, "w") as f:
        f.write(f"TREND_SELL_CONFIDENCE={confidence}\n")

    print(f"[AI] Nytt förtroende för trendbaserad sälj: {confidence:.2f}")
    print(f"[OK] Sparat till {out_path}")

if __name__ == "__main__":
    adjust_trend_sell_confidence()
