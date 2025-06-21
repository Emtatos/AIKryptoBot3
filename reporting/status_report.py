# =============================================================================
# status_report.py – Skickar Telegramstatus med verkliga innehav från Kraken
# =============================================================================

import os
import sys
import pandas as pd
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.broker_kraken import KrakenBroker
from reporting.telegram import send_telegram
from config.telegram_config import MIN_USD_DISPLAY

def send_status_report():
    broker = KrakenBroker()
    portfolio = broker.get_portfolio()
    
    if not portfolio:
        send_telegram("💼 Inga innehav hittades – portföljen är tom.")
        return

    stoploss_path = os.path.join(project_root, "data", "stop_loss_profile.csv")
    stoploss_data = {}
    if os.path.exists(stoploss_path):
        try:
            stoploss_df = pd.read_csv(stoploss_path)
            stoploss_data = stoploss_df.set_index("symbol").to_dict(orient="index")
        except Exception as e:
            print(f"[WARNING] Kunde inte läsa stop_loss_profile.csv: {e}")

    lines = ["📊 *AI Crypto Portföljstatus – Verkliga innehav*", "```"]
    total_value = 0
    shown_any = False

    for symbol, qty in portfolio.items():
        if symbol == "USD":
            continue
            
        price = broker.get_price(symbol)
        if price is None:
            continue

        value = qty * price
        if value < MIN_USD_DISPLAY:
            continue

        total_value += value
        
        entry_data = stoploss_data.get(symbol, {})
        entry_price = entry_data.get("entry_price")
        peak = entry_data.get("last_peak")
        sl = entry_data.get("stop_price")

        change_str = ""
        if entry_price and entry_price > 0:
            diff = price - entry_price
            pct = diff / entry_price * 100
            change_str = f"\n📈 Avkastning: {'+' if diff>=0 else ''}${diff:.2f} ({pct:.2f}%) sedan köp på ${entry_price:.2f}"

        peak_str = f"\n🔼 Peak: ${peak:.2f}" if peak else ""
        sl_str = f" 🛑 SL: ${sl:.2f}" if sl else ""
        lines.append(f"{symbol}: {qty:.6f} × ${price:.2f} = ${value:.2f}{change_str}{peak_str}{sl_str}")
        shown_any = True

    lines.append("-" * 26)
    lines.append(f"💰 Totalt värde: ${total_value:.2f}")
    lines.append("```")

    message = "\n".join(lines) if shown_any else f"💼 Inga innehav över ${MIN_USD_DISPLAY} att visa."
    send_telegram(message)

if __name__ == "__main__":
    send_status_report()
