# =============================================================================
# price_updater.py – Uppdaterar price_history.csv med aktuella priser för alla coins
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

price_path = os.path.join(project_root, "data", "price_history.csv")
broker = KrakenBroker()

def update_price_history():
    prices = {}
    for coin in ACTIVE_COINS:
        price = broker.get_price(coin)
        if price:
            prices[coin] = price

    today = datetime.now().strftime("%Y-%m-%d")

    if os.path.exists(price_path):
        df = pd.read_csv(price_path, index_col=0)
        df.index = pd.to_datetime(df.index, errors='coerce')
        df = df[~df.index.isna()]  # Ta bort ogiltiga rader
    else:
        df = pd.DataFrame()

    new_row = pd.DataFrame(prices, index=[pd.to_datetime(today)])
    if today in df.index.strftime("%Y-%m-%d"):
        df.loc[df.index.strftime("%Y-%m-%d") == today] = new_row.values
    else:
        df = pd.concat([df, new_row])

    df.sort_index(inplace=True)
    df.to_csv(price_path)
    print(f"[OK] price_history.csv uppdaterad ({today}) – {len(prices)} coins")

if __name__ == "__main__":
    update_price_history()
