# =============================================================================
# switch_logger.py – Loggar alla switchar (byten mellan coins) till switch_log.csv
# =============================================================================

import os
import sys
import pandas as pd
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

switch_log_path = os.path.join(project_root, "logs", "switch_log.csv")

def log_switch(from_coin, to_coin, score_diff, sell_price, buy_price):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = {
        "timestamp": timestamp,
        "from": from_coin,
        "to": to_coin,
        "score_diff": round(score_diff, 4),
        "sell_price": round(sell_price, 4),
        "buy_price": round(buy_price, 4),
        "outcome": "pending"
    }

    df = pd.DataFrame([row])
    header = not os.path.exists(switch_log_path)
    df.to_csv(switch_log_path, mode="a", header=header, index=False)
    print(f"[SWITCH-LOG] {from_coin} → {to_coin} loggad.")

if __name__ == "__main__":
    log_switch("ETH", "BTC", 1.23, 2540.55, 104200.00)
