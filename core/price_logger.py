# =============================================================================
# price_logger.py – Loggar varje körning med tidsstämpel till price_history_live.csv
# =============================================================================

import os
import sys
import pandas as pd
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.coin_config import ACTIVE_COINS
from core.broker_kraken import KrakenBroker

live_log_path = os.path.join(project_root, "data", "price_history_live.csv")
broker = KrakenBroker()

def log_live_prices():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prices = {}
    for coin in ACTIVE_COINS:
        price = broker.get_price(coin)
        if price:
            prices[coin] = price

    if not prices:
        print("[X] Inga priser kunde loggas.")
        return

    row = pd.DataFrame([{"timestamp": timestamp, **prices}])
    header = not os.path.exists(live_log_path)
    row.to_csv(live_log_path, mode="a", header=header, index=False)
    print(f"[OK] price_history_live.csv uppdaterad ({timestamp}) – {len(prices)} coins")

if __name__ == "__main__":
    log_live_prices()
