# =============================================================================
# signal_outcome_tracker.py – Utvärderar tidigare signaler mot senare pris
# =============================================================================

import os
import sys
import pandas as pd
from datetime import datetime, timedelta

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

signal_log_path = os.path.join(project_root, "logs", "signal_log.csv")
price_path = os.path.join(project_root, "data", "price_history.csv")
outcome_log_path = os.path.join(project_root, "logs", "signal_outcome.csv")

def log_signal_outcomes():
    if not os.path.exists(signal_log_path) or not os.path.exists(price_path):
        print("[X] Kräver både signal_log och price_history.")
        return

    signal_df = pd.read_csv(signal_log_path, parse_dates=["timestamp"])
    price_df = pd.read_csv(price_path, index_col=0, parse_dates=True)

    rows = []
    latest_date = price_df.index[-1]

    for _, row in signal_df.iterrows():
        symbol = row["symbol"]
        signal_time = row["timestamp"]
        base_price = row["price"]

        if symbol not in price_df.columns:
            continue

        signal_day = signal_time.date()
        next_day = signal_day + timedelta(days=1)

        future_price = price_df.loc[price_df.index.date == next_day, symbol]

        if future_price.empty:
            continue

        price_after = future_price.values[0]
        change_pct = round((price_after - base_price) / base_price * 100, 2)

        rows.append({
            "timestamp": signal_time.strftime("%Y-%m-%d %H:%M:%S"),
            "symbol": symbol,
            "signal": row["signal"],
            "score": row["score"],
            "delta": row["delta"],
            "price_at_signal": base_price,
            "price_day_after": price_after,
            "pct_change": change_pct
        })

    if rows:
        df_out = pd.DataFrame(rows)
        header = not os.path.exists(outcome_log_path)
        df_out.to_csv(outcome_log_path, mode="a", header=header, index=False)
        print(f"[OK] {len(rows)} signalutfall loggade till signal_outcome.csv")
    else:
        print("[INFO] Inga signalutfall kunde beräknas ännu.")

if __name__ == "__main__":
    log_signal_outcomes()
