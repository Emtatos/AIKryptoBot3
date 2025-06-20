# =============================================================================
# adaptive_buy_score.py – Justerar MIN_BUY_SCORE baserat på BUY-träffsäkerhet
# =============================================================================

import os
import sys
import pandas as pd
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

signal_stats_path = os.path.join(project_root, "logs", "signal_accuracy.csv")
threshold_file = os.path.join(project_root, "config", "adaptive_thresholds.txt")
history_log_path = os.path.join(project_root, "logs", "threshold_history.csv")

DEFAULT = 0.5
MIN_SCORE = 0.2
MAX_SCORE = 1.0


def adjust_min_buy_score():
    if not os.path.exists(signal_stats_path):
        print("[X] signal_accuracy.csv saknas.")
        return

    df = pd.read_csv(signal_stats_path)
    df = df[df["signal"] == "BUY"].sort_values("timestamp", ascending=False)

    if len(df) < 3:
        print("[INFO] För få BUY-träffar för att justera.")
        return

    recent = df.head(10)
    hitrate = recent["hit_rate_%"].mean() / 100

    profit_factor = 1.0
    if "avg_profit_%" in recent.columns:
        avg_profit = recent["avg_profit_%"].mean()
        profit_factor = 1 + (avg_profit / 100) * 0.5

    base_adjustment = (0.5 - hitrate) * 0.4
    profit_adjustment = (profit_factor - 1) * 0.3
    new_score = DEFAULT + base_adjustment + profit_adjustment
    new_score = round(max(MIN_SCORE, min(MAX_SCORE, new_score)), 2)

    # Läs in befintlig fil, uppdatera rad eller lägg till
    lines = []
    if os.path.exists(threshold_file):
        with open(threshold_file, "r") as f:
            lines = f.readlines()

    updated = False
    for i, line in enumerate(lines):
        if line.startswith("MIN_BUY_SCORE"):
            lines[i] = f"MIN_BUY_SCORE={new_score}\n"
            updated = True

    if not updated:
        lines.append(f"MIN_BUY_SCORE={new_score}\n")

    with open(threshold_file, "w") as f:
        f.writelines(lines)

    log_row = pd.DataFrame([{
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "parameter": "MIN_BUY_SCORE",
        "value": new_score
    }])
    header = not os.path.exists(history_log_path)
    log_row.to_csv(history_log_path, mode="a", header=header, index=False)

    print(f"[AI] Ny MIN_BUY_SCORE = {new_score} baserat på träffsäkerhet ({hitrate:.2%})")

if __name__ == "__main__":
    adjust_min_buy_score()
