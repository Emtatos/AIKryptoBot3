# =============================================================================
# signal_log_simulator.py – Skapar testposter i signal_log.csv för utvärdering
# =============================================================================

import os
import sys
import pandas as pd
from datetime import datetime, timedelta

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

signal_log_path = os.path.join(project_root, "logs", "signal_log.csv")

# Datum 2 dagar tillbaka, så att utvärdering kan ske
signal_time = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")

# Exempelposter (anpassa till dina faktiska aktiva coins om du vill)
test_rows = [
    {"timestamp": signal_time, "symbol": "BTC", "score": 1.2, "delta": 0.8, "price": 10300.00, "signal": "BUY"},
    {"timestamp": signal_time, "symbol": "ETH", "score": -1.1, "delta": -0.9, "price": 2500.00, "signal": "SELL"},
]

df = pd.DataFrame(test_rows)
header = not os.path.exists(signal_log_path)
df.to_csv(signal_log_path, mode="a", header=header, index=False)
print(f"[OK] Testsignaler loggade till {signal_log_path}")
