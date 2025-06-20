# =============================================================================
# trend_shift_detector.py – Identifierar snabba trendvändningar inom 1 timme
# Loggar till trend_shift_signals.csv
# =============================================================================

import os
import sys
import pandas as pd
from datetime import datetime, timedelta

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.coin_config import ACTIVE_COINS
from reporting.telegram import send_telegram

live_path = os.path.join(project_root, "data", "price_history_live.csv")
trend_log_path = os.path.join(project_root, "logs", "trend_shift_signals.csv")

THRESHOLD_PCT = 2.0  # gräns för förändring (±)

def detect_trend_shifts():
    if not os.path.exists(live_path):
        print("[X] price_history_live.csv saknas.")
        return []

    df = pd.read_csv(live_path, parse_dates=["timestamp"])
    cutoff = datetime.now() - timedelta(minutes=60)
    df = df[df["timestamp"] >= cutoff]

    if df.empty:
        print("[X] Inga datapunkter från senaste timmen.")
        return []

    latest = df.iloc[-1]
    early = df.iloc[0]
    signals = []
    log_rows = []

    for coin in ACTIVE_COINS:
        if coin not in df.columns:
            continue

        try:
            pct_change = (latest[coin] - early[coin]) / early[coin] * 100
            pct_change = round(pct_change, 2)

            if pct_change >= THRESHOLD_PCT:
                signals.append(f"📈 {coin} har stigit {pct_change}% senaste timmen")
                log_rows.append({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "symbol": coin, "direction": "UP", "change_pct": pct_change})
            elif pct_change <= -THRESHOLD_PCT:
                signals.append(f"📉 {coin} har fallit {pct_change}% senaste timmen")
                log_rows.append({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "symbol": coin, "direction": "DOWN", "change_pct": pct_change})
        except:
            continue

    if log_rows:
        df_log = pd.DataFrame(log_rows)
        header = not os.path.exists(trend_log_path)
        df_log.to_csv(trend_log_path, mode="a", header=header, index=False)

    if signals:
        msg = "\n".join(["🔍 Trendvändningar upptäckta:"] + signals)
        print(msg)
        send_telegram(msg)
    else:
        print("[OK] Inga snabba trendvändningar just nu.")

    return signals

if __name__ == "__main__":
    detect_trend_shifts()
