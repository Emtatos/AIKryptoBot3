# =============================================================================
# signal_timing_analyzer.py – Utvärderar signalutfall beroende på tidpunkt
# =============================================================================

import os
import sys
import pandas as pd
from datetime import datetime

def analyze_signal_timing():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    outcome_path = os.path.join(project_root, "logs", "signal_outcome.csv")
    summary_path = os.path.join(project_root, "logs", "signal_timing_summary.csv")

    if not os.path.exists(outcome_path):
        print("[X] signal_outcome.csv saknas.")
        return

    try:
        df = pd.read_csv(outcome_path, parse_dates=["timestamp"])
    except Exception as e:
        print(f"[X] Fel vid läsning: {e}")
        return

    if df.empty:
        print("[INFO] Filen är tom.")
        return

    df["hour"] = df["timestamp"].dt.hour

    result = df.groupby("hour").agg(
        avg_return=("pct_change", "mean"),
        signal_count=("pct_change", "count")
    ).round(2)

    hit_rate = df.groupby("hour")["pct_change"].apply(lambda x: round((x > 0).sum() / len(x) * 100, 2))
    result["hit_rate"] = hit_rate

    print("\n=== Signalutfall per timme på dygnet ===")
    print(result.reset_index().to_string(index=False))

    result["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result.reset_index(inplace=True)
    header = not os.path.exists(summary_path)
    result.to_csv(summary_path, mode="a", header=header, index=False)
    print(f"[OK] Sammanfattning loggad till {summary_path}")

if __name__ == "__main__":
    analyze_signal_timing()
