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
from core.technical_indicators import (
    calculate_rsi, calculate_macd, calculate_bollinger_bands, 
    calculate_volatility, calculate_momentum_score
)

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

    results = []

    for coin in ACTIVE_COINS:
        if coin not in df.columns:
            continue

        prices = df[coin].dropna()
        if len(prices) < 30:
            print(f"[SKIP] {coin}: för lite data ({len(prices)} dagar)")
            continue

        momentum_score = calculate_momentum_score(prices)
        
        rsi = calculate_rsi(prices)
        macd_line, signal_line, histogram = calculate_macd(prices)
        upper_bb, middle_bb, lower_bb = calculate_bollinger_bands(prices)
        volatility = calculate_volatility(prices)
        
        rsi_value = rsi.iloc[-1] if len(rsi) > 0 else 50
        histogram_value = histogram.iloc[-1] if len(histogram) > 0 else 0
        volatility_value = volatility.iloc[-1] if len(volatility) > 0 else 0.1
        
        rsi_score = 0
        if rsi_value < 30:
            rsi_score = (30 - rsi_value) / 30 * 50
        elif rsi_value > 70:
            rsi_score = (rsi_value - 70) / 30 * -50
            
        macd_score = 0
        if len(histogram) > 1:
            if histogram_value > histogram.iloc[-2]:
                macd_score = 25
            else:
                macd_score = -25
                
        bb_score = 0
        current_price = prices.iloc[-1]
        lower_bb_value = lower_bb.iloc[-1] if len(lower_bb) > 0 else current_price
        upper_bb_value = upper_bb.iloc[-1] if len(upper_bb) > 0 else current_price
        
        if current_price < lower_bb_value:
            bb_score = 30
        elif current_price > upper_bb_value:
            bb_score = -30
            
        vol_adjustment = min(volatility_value * -10, -5) if not np.isnan(volatility_value) else 0
        
        technical_score = (rsi_score + macd_score + bb_score + vol_adjustment) / 4
        final_score = (momentum_score * 0.6) + (technical_score * 0.4)
        
        row = {
            "symbol": coin,
            "momentum_score": round(momentum_score, 2),
            "rsi": round(rsi_value, 2),
            "macd_signal": "BUY" if macd_score > 0 else "SELL",
            "bb_position": "BELOW" if bb_score > 0 else "ABOVE" if bb_score < 0 else "MIDDLE",
            "volatility": round(volatility_value, 4),
            "technical_score": round(technical_score, 2),
            "score": round(final_score, 2),
            "W3": round((prices.iloc[-1] - prices.iloc[-4]) / prices.iloc[-4] * 100, 2) if len(prices) >= 4 else 0,
            "W7": round((prices.iloc[-1] - prices.iloc[-8]) / prices.iloc[-8] * 100, 2) if len(prices) >= 8 else 0,
            "W14": round((prices.iloc[-1] - prices.iloc[-15]) / prices.iloc[-15] * 100, 2) if len(prices) >= 15 else 0
        }
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
