# =============================================================================
# kraken_history_fetcher.py – Hämtar 60 dagars historik för ACTIVE_COINS från Kraken
# Skapar price_history.csv i rätt format för momentum-generatorn
# =============================================================================

import os
import sys
import time
import pandas as pd
from datetime import datetime, timedelta
import krakenex

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.coin_config import ACTIVE_COINS

price_path = os.path.join(project_root, "data", "price_history.csv")

api = krakenex.API()
keyfile = os.path.join(project_root, "config", "kraken.key")
if os.path.exists(keyfile):
    api.load_key(keyfile)
else:
    print("[X] Ingen API-nyckel hittad. Endast publika anrop.")

interval = 1440  # 1 dag (i minuter)
days_back = 60
since_ts = int((datetime.utcnow() - timedelta(days=days_back)).timestamp())

all_data = {}

for symbol in ACTIVE_COINS:
    pair = f"{symbol}USD"
    print(f"[FETCH] Hämtar OHLC för {pair}...")
    try:
        res = api.query_public("OHLC", {"pair": pair, "interval": interval, "since": since_ts})
        result = res.get("result")
        if not result:
            print(f"[X] Inget resultat för {pair}")
            continue

        data_key = list(result.keys())[0]  # dynamiskt par-ID
        rows = result[data_key]
        df = pd.DataFrame(rows, columns=["time", "open", "high", "low", "close", "vwap", "volume", "count"])
        df["time"] = pd.to_datetime(df["time"], unit="s")
        df.set_index("time", inplace=True)
        df = df[["close"]].astype(float)
        df.rename(columns={"close": symbol}, inplace=True)
        all_data[symbol] = df
        time.sleep(1.2)  # Kraken rate limit
    except Exception as e:
        print(f"[X] Fel för {symbol}: {e}")

# Kombinera till en enda DataFrame
if all_data:
    df_combined = pd.concat(all_data.values(), axis=1)
    df_combined = df_combined.sort_index()
    df_combined.to_csv(price_path)
    print(f"[OK] price_history.csv sparad ({df_combined.shape[0]} rader, {df_combined.shape[1]} kolumner)")
else:
    print("[X] Ingen data kunde hämtas.")
