# =============================================================================
# log_status_checker.py – Visar status för loggfiler: antal rader, senaste datum
# =============================================================================

import os
import sys
import pandas as pd

from datetime import datetime
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

log_dir = os.path.join(project_root, "logs")
log_files = [
    "score_log.csv",
    "signal_log.csv",
    "signal_outcome.csv",
    "signal_accuracy.csv"
]

print("\n=== Loggstatus – Uppdateringskontroll ===")

for log in log_files:
    path = os.path.join(log_dir, log)
    if not os.path.exists(path):
        print(f"[ ] {log}: FIL SAKNAS")
        continue

    try:
        df = pd.read_csv(path, parse_dates=["timestamp"], low_memory=False)
        n_rows = len(df)
        latest = df["timestamp"].max() if "timestamp" in df.columns else "-"
        print(f"[✔] {log}: {n_rows} rader, senaste: {latest}")
    except Exception as e:
        print(f"[X] {log}: FEL – {e}")
