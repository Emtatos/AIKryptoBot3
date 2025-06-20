# =============================================================================
# signal_logger.py – Loggar köp- och säljsignaler med score, delta och pris
# =============================================================================

import os
import sys
import pandas as pd
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.coin_config import ACTIVE_COINS

def log_signals():
    score_log_path = os.path.join(project_root, "logs", "score_log.csv")
    signal_log_path = os.path.join(project_root, "logs", "signal_log.csv")
    price_path = os.path.join(project_root, "data", "price_history.csv")

    if not os.path.exists(score_log_path) or not os.path.exists(price_path):
        print("[X] Saknar score_log eller price_history – avbryter.")
        return

    price_df = pd.read_csv(price_path, index_col=0, parse_dates=True)
    score_df = pd.read_csv(score_log_path)

    latest_scores = score_df[score_df["timestamp"] == score_df["timestamp"].max()]
    latest_price = price_df.iloc[-1]

    rows = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for _, row in latest_scores.iterrows():
        symbol = row["symbol"]
        score = row["score"]

        history = score_df[score_df["symbol"] == symbol].sort_values("timestamp")
        if len(history) < 2:
            continue

        prev_score = history.iloc[-2]["score"]
        delta = round(score - prev_score, 4)
        price = latest_price.get(symbol)

        if price and abs(delta) > 0.1:
            rows.append({
                "timestamp": timestamp,
                "symbol": symbol,
                "score": score,
                "delta": delta,
                "price": price,
                "signal": "BUY" if score > 0.5 and delta > 0.5 else ("SELL" if score < -0.5 and delta < -0.5 else "HOLD")
            })

    if rows:
        df_out = pd.DataFrame(rows)
        header = not os.path.exists(signal_log_path)
        df_out.to_csv(signal_log_path, mode="a", header=header, index=False)
        print(f"[OK] {len(rows)} signaler loggade till signal_log.csv")
    else:
        print("[INFO] Inga nya signaler att logga.")

if __name__ == "__main__":
    log_signals()
