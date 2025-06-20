# =============================================================================
# momentum_generator.py – AIKryptoBot3: Beräknar momentumscore för ACTIVE_COINS
# =============================================================================

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime

# Robust projektrot
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.coin_config import ACTIVE_COINS

price_path = os.path.join(project_root, "data", "price_history.csv")
output_path = os.path.join(project_root, "data", "momentum_combined.csv")
top_ranked_path = os.path.join(project_root, "data", "top_ranked_today.csv")

def generate_momentum():
    print("\n=== Startar momentum-generator (endast ACTIVE_COINS) ===")

    if not os.path.exists(price_path):
        print("[X] price_history.csv saknas.")
        return

    df = pd.read_csv(price_path, index_col=0, parse_dates=True)
    df = df.select_dtypes(include=[np.number])
    if df.empty:
        print("[X] price_history.csv är tom.")
        return

    print("[OK] price_history.csv laddad.")
    print(f"[INFO] Senaste datum: {df.index[-1].date()}")

    lookbacks = [3, 7, 14]
    results = []

    for coin in ACTIVE_COINS:
        if coin not in df.columns:
            continue

        prices = df[coin].dropna()
        if len(prices) < max(lookbacks) + 1:
            print(f"[SKIP] {coin}: för lite data ({len(prices)} dagar)")
            continue

        row = {"symbol": coin}
        for lb in lookbacks:
            try:
                pct = (prices.iloc[-1] - prices.iloc[-lb-1]) / prices.iloc[-lb-1] * 100
                row[f"W{lb}"] = pct
            except:
                row[f"W{lb}"] = 0

        row["score"] = row["W3"] * 0.3 + row["W7"] * 0.3 + row["W14"] * 0.4
        results.append(row)

    df_out = pd.DataFrame(results)

    if df_out.empty or "score" not in df_out.columns:
        print("[X] Ingen score kunde beräknas – kontrollera prisdata.")
        return

    df_out = df_out.sort_values(by="score", ascending=False)
    df_out.to_csv(output_path, index=False)
    print(f"[OK] momentum_combined.csv sparad ({len(df_out)} coins)")

    df_top5 = df_out.head(5)
    df_top5.to_csv(top_ranked_path, index=False)
    print(f"[OK] top_ranked_today.csv sparad (5 coins)")
    print("=== Momentum-generator färdig ===")

# =============================================================================
# TEST
# =============================================================================
if __name__ == "__main__":
    generate_momentum()
