# =============================================================================
# debug_momentum.py – Skriver ut W3, W7, W14 och score för varje coin
# Används för att felsöka momentumlogik och kontrollera prisrörelser
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

if not os.path.exists(price_path):
    print("[X] price_history.csv saknas.")
    sys.exit()

df = pd.read_csv(price_path, index_col=0, parse_dates=True)
df = df.select_dtypes(include=[np.number])  # Endast numeriska kolumner

if df.empty:
    print("[X] price_history.csv är tom.")
    sys.exit()

print("=== Score-debug: W3, W7, W14, score ===")
lookbacks = [3, 7, 14]

for coin in df.columns:
    prices = df[coin].dropna()
    if len(prices) < max(lookbacks) + 1:
        print(f"[SKIP] {coin}: för lite data ({len(prices)} dagar)")
        continue

    try:
        w3 = (prices.iloc[-1] - prices.iloc[-4]) / prices.iloc[-4] * 100
        w7 = (prices.iloc[-1] - prices.iloc[-8]) / prices.iloc[-8] * 100
        w14 = (prices.iloc[-1] - prices.iloc[-15]) / prices.iloc[-15] * 100
        score = round(w3 * 0.3 + w7 * 0.3 + w14 * 0.4, 2)
        print(f"{coin}: W3={w3:.2f}, W7={w7:.2f}, W14={w14:.2f} → score={score:.2f}")
    except Exception as e:
        print(f"[X] Fel vid beräkning för {coin}: {e}")
