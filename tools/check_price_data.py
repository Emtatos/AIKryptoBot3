# =============================================================================
# check_price_data.py – Kontrollerar att alla ACTIVE_COINS har tillräckligt med data
# =============================================================================

import os
import sys
import pandas as pd

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.coin_config import ACTIVE_COINS

price_path = os.path.join(project_root, "data", "price_history.csv")

print("\n=== Datakontroll för price_history.csv ===")

if not os.path.exists(price_path):
    print("[X] price_history.csv saknas.")
    sys.exit()

# Läs in data
try:
    df = pd.read_csv(price_path, index_col=0, parse_dates=True)
except Exception as e:
    print(f"[X] Fel vid läsning: {e}")
    sys.exit()

# Kontrollera varje coin
min_required = 15
for coin in ACTIVE_COINS:
    if coin not in df.columns:
        print(f"[X] {coin}: saknas i filen")
    else:
        count = df[coin].dropna().shape[0]
        if count < min_required:
            print(f"[!] {coin}: endast {count} datapunkter (behöver minst {min_required})")
        else:
            print(f"[OK] {coin}: {count} datapunkter")

print("=== Kontroll klar ===")
