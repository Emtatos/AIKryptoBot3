# =============================================================================
# signal_accuracy_analyzer.py – Utvärderar träffsäkerhet för BUY/SELL-signaler
# Loggar även till signal_accuracy.csv för självlärande användning
# =============================================================================

import os
import sys
import pandas as pd
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

outcome_log_path = os.path.join(project_root, "logs", "signal_outcome.csv")
accuracy_log_path = os.path.join(project_root, "logs", "signal_accuracy.csv")

def analyze_signal_accuracy():
    if not os.path.exists(outcome_log_path):
        print("[X] signal_outcome.csv saknas.")
        return

    outcomes = pd.read_csv(outcome_log_path)
    summary = []

    for signal_type in outcomes["signal"].unique():
        subset = outcomes[outcomes["signal"] == signal_type]
        total = len(subset)
        if total == 0:
            continue

        positive = subset[subset["pct_change"] > 0].shape[0]
        hit_rate = round(positive / total * 100, 1)
        avg_return = round(subset["pct_change"].mean(), 2)
        summary.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "signal": signal_type,
            "total_signals": total,
            "positive_outcomes": positive,
            "hit_rate_%": hit_rate,
            "avg_return_%": avg_return
        })

    if summary:
        df = pd.DataFrame(summary)
        print("\n=== Träffsäkerhet per signaltyp ===")
        print(df.to_string(index=False))

        # Logga till CSV för självlärande analys
        header = not os.path.exists(accuracy_log_path)
        df.to_csv(accuracy_log_path, mode="a", header=header, index=False)
        print(f"[OK] Träffsäkerhet loggad till signal_accuracy.csv")
    else:
        print("[INFO] Inga signalutfall hittades för analys.")

if __name__ == "__main__":
    analyze_signal_accuracy()
