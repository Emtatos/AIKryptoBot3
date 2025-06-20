# =============================================================================
# adaptive_thresholds.py – Justerar MIN_BUY_SCORE baserat på signalhistorik
# =============================================================================

import os
import sys
import pandas as pd

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

accuracy_log_path = os.path.join(project_root, "logs", "signal_accuracy.csv")
adaptive_path = os.path.join(project_root, "config", "adaptive_thresholds.txt")

if not os.path.exists(accuracy_log_path):
    print("[X] signal_accuracy.csv saknas.")
    sys.exit()

acc_df = pd.read_csv(accuracy_log_path)

# Filtrera på BUY-signal
buy_stats = acc_df[acc_df["signal"] == "BUY"]

if len(buy_stats) < 3:
    print("[INFO] För få datapunkter för att anpassa tröskel.")
    sys.exit()

# Använd de senaste 5 mätningarna (om de finns)
last_n = buy_stats.tail(5)
mean_hit = last_n["hit_rate_%"].mean()
mean_return = last_n["avg_return_%"].mean()

# Anpassa MIN_BUY_SCORE dynamiskt
if mean_hit > 70:
    min_score = 0.5
elif mean_hit > 50:
    min_score = 1.0
else:
    min_score = 1.5

with open(adaptive_path, "w") as f:
    f.write(f"MIN_BUY_SCORE={min_score}\n")
    f.write(f"# Baserat på snitt träff: {mean_hit:.1f}%, avkastning: {mean_return:.2f}%\n")

print(f"[OK] MIN_BUY_SCORE satt till {min_score} baserat på senaste träffsäkerhet.")
