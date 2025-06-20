# =============================================================================
# trend_sell_analyzer.py – Utvärderar träffsäkerhet för trendbaserade sälj
# =============================================================================

import os
import sys
import pandas as pd
from datetime import datetime, timedelta

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

trend_log = os.path.join(project_root, "logs", "trend_sell_log.csv")
price_path = os.path.join(project_root, "data", "price_history.csv")
result_log = os.path.join(project_root, "logs", "trend_sell_accuracy.csv")

def evaluate_trend_sells():
    if not os.path.exists(trend_log) or not os.path.exists(price_path):
        print("[X] Kräver både trend_sell_log.csv och price_history.csv")
        return

    df_trend = pd.read_csv(trend_log, parse_dates=["timestamp"])
    df_price = pd.read_csv(price_path, index_col=0, parse_dates=True)

    results = []
    for _, row in df_trend.iterrows():
        symbol = row["symbol"]
        ts = row["timestamp"]
        sell_price = row["price"]

        future_day = (ts + timedelta(days=1)).date()
        future_row = df_price.loc[df_price.index.date == future_day]

        if future_row.empty or symbol not in df_price.columns:
            continue

        price_next_day = future_row[symbol].values[0]
        change_pct = round((sell_price - price_next_day) / sell_price * 100, 2)
        hit = change_pct > 0  # positivt om priset gick ner = rätt sälj

        results.append({
            "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "symbol": symbol,
            "sold_at": sell_price,
            "price_next_day": price_next_day,
            "change_%": change_pct,
            "hit": hit
        })

    if not results:
        print("[INFO] Inga träffar att utvärdera.")
        return

    df_out = pd.DataFrame(results)
    df_out.to_csv(result_log, index=False)

    hits = df_out["hit"].sum()
    total = len(df_out)
    accuracy = round(hits / total * 100, 2)

    print(f"=== Trend-sälj träffsäkerhet: {hits}/{total} = {accuracy}% ===")
    print("[OK] Resultat sparat till trend_sell_accuracy.csv")

if __name__ == "__main__":
    evaluate_trend_sells()
