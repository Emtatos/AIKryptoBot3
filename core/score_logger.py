# =============================================================================
# score_logger.py – Loggar momentumscore (W3, W7, W14, score) per coin per körning
# =============================================================================

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.coin_config import ACTIVE_COINS

def log_top_scores():
    price_path = os.path.join(project_root, "data", "price_history.csv")
    log_path = os.path.join(project_root, "logs", "score_log.csv")

    if not os.path.exists(price_path):
        print("[X] price_history.csv saknas.")
        return

    df = pd.read_csv(price_path, index_col=0, parse_dates=True)
    df = df.select_dtypes(include=[np.number])

    if df.empty:
        print("[X] price_history.csv är tom.")
        return

    lookbacks = [3, 7, 14]
    rows = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for coin in df.columns:
        prices = df[coin].dropna()
        if len(prices) < max(lookbacks) + 1:
            continue
        try:
            w3 = (prices.iloc[-1] - prices.iloc[-4]) / prices.iloc[-4] * 100
            w7 = (prices.iloc[-1] - prices.iloc[-8]) / prices.iloc[-8] * 100
            w14 = (prices.iloc[-1] - prices.iloc[-15]) / prices.iloc[-15] * 100
            score = round(w3 * 0.3 + w7 * 0.3 + w14 * 0.4, 4)
            rows.append({
                "timestamp": timestamp,
                "symbol": coin,
                "W3": round(w3, 4),
                "W7": round(w7, 4),
                "W14": round(w14, 4),
                "score": score
            })
        except:
            continue

    if rows:
        df_log = pd.DataFrame(rows)
        header = not os.path.exists(log_path)
        df_log.to_csv(log_path, mode="a", header=header, index=False)
        print(f"[OK] {len(rows)} rader loggade till score_log.csv")
    else:
        print("[INFO] Inget att logga.")

# Direkt körbar
if __name__ == "__main__":
    log_top_scores()
