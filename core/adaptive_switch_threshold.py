# =============================================================================
# adaptive_switch_threshold.py – Justerar SWITCH_THRESHOLD utifrån switch_log.csv
# =============================================================================

import os
import sys
import pandas as pd
from datetime import datetime, timedelta

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

switch_log_path = os.path.join(project_root, "logs", "switch_log.csv")
price_path = os.path.join(project_root, "data", "price_history.csv")
threshold_file = os.path.join(project_root, "config", "adaptive_thresholds.txt")
history_log_path = os.path.join(project_root, "logs", "threshold_history.csv")

MIN_THRESHOLD = 0.3
MAX_THRESHOLD = 1.5
DEFAULT = 0.75


def adjust_switch_threshold():
    if not os.path.exists(switch_log_path) or not os.path.exists(price_path):
        print("[X] Kräver switch_log.csv och price_history.csv.")
        return

    df = pd.read_csv(switch_log_path, parse_dates=["timestamp"])
    price_df = pd.read_csv(price_path, index_col=0, parse_dates=True)

    recent = df[df["outcome"] == "pending"].copy()
    if recent.empty:
        print("[INFO] Inga pending-byten att utvärdera.")
        return

    evaluated = 0
    positive = 0
    updated_rows = []

    for i, row in recent.iterrows():
        ts = row["timestamp"]
        to_coin = row["to"]
        buy_price = row["buy_price"]
        future_day = (ts + timedelta(days=1)).date()

        if to_coin not in price_df.columns:
            continue

        match = price_df.loc[price_df.index.date == future_day]
        if match.empty:
            continue

        price_after = match[to_coin].values[0]
        change_pct = round((price_after - buy_price) / buy_price * 100, 2)

        evaluated += 1
        if change_pct > 0:
            positive += 1

        df.at[i, "outcome"] = "success" if change_pct > 0 else "fail"
        df.at[i, "return_%"] = change_pct
        updated_rows.append(i)

    if updated_rows:
        df.to_csv(switch_log_path, index=False)
        print(f"[OK] {len(updated_rows)} byten uppdaterade med utfall.")

    if evaluated >= 3:
        hitrate = positive / evaluated
        new_threshold = round(DEFAULT + (0.5 - hitrate), 2)
        new_threshold = max(MIN_THRESHOLD, min(MAX_THRESHOLD, new_threshold))

        with open(threshold_file, "w") as f:
            f.write(f"SWITCH_THRESHOLD={new_threshold}\n")

        log_row = pd.DataFrame([{
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "parameter": "SWITCH_THRESHOLD",
            "value": new_threshold
        }])
        header = not os.path.exists(history_log_path)
        log_row.to_csv(history_log_path, mode="a", header=header, index=False)

        print(f"[AI] Ny SWITCH_THRESHOLD = {new_threshold} baserat på träff: {positive}/{evaluated}")
    else:
        print("[INFO] För få byten för att justera tröskel.")

if __name__ == "__main__":
    adjust_switch_threshold()
