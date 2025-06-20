# =============================================================================
# debug_momentum_scores.py – Skriver ut score-beräkningarna för alla coins
# =============================================================================

import os
import sys
import pandas as pd
import numpy as np

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.coin_config import ACTIVE_COINS

price_path = os.path.join(project_root, "data", "price_history.csv")

lookbacks = [3, 7, 14]
print("=== Score-debug: W3, W7, W14, score ===")

if not os.path.exists(price_path):
    print("[X] price_history.csv saknas.")
    sys.exit()

# Läs prisdata
df = pd.read_csv(price_path, index_col=0, parse_dates=True)
df = df.select_dtypes(include=[np.number])

for coin in ACTIVE_COINS:
    if coin not in df.columns:
        print(f"[X] {coin} saknas i data")
        continue

    prices = df[coin].dropna()
    if len(prices) < max(lookbacks) + 1:
        print(f"[SKIP] {coin}: {len(prices)} datapunkter")
        continue

    try:
        w3  = (prices.iloc[-1] - prices.iloc[-4])  / prices.iloc[-4]  * 100
        w7  = (prices.iloc[-1] - prices.iloc[-8])  / prices.iloc[-8]  * 100
        w14 = (prices.iloc[-1] - prices.iloc[-15]) / prices.iloc[-15] * 100
        score = round(w3 * 0.3 + w7 * 0.3 + w14 * 0.4, 2)
        print(f"{coin}: W3={w3:.2f}, W7={w7:.2f}, W14={w14:.2f} → score={score:.2f}")
    except Exception as e:
        print(f"[X] Fel i {coin}: {e}")
