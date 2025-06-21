# =============================================================================
# =============================================================================

import os
import sys
import pandas as pd
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from reporting.telegram import send_telegram
from core.broker_kraken import KrakenBroker

def send_daily_summary():
    today = datetime.now().date()
    broker = KrakenBroker()
    
    portfolio = broker.get_portfolio()
    total_value = 0
    for symbol, qty in portfolio.items():
        if symbol == "USD":
            total_value += qty
        else:
            price = broker.get_price(symbol)
            if price:
                total_value += qty * price

    signal_log_path = os.path.join(project_root, "logs", "signal_log.csv")
    signal_counts = {"BUY": 0, "SELL": 0, "HOLD": 0}
    
    if os.path.exists(signal_log_path):
        try:
            signal_df = pd.read_csv(signal_log_path, parse_dates=['timestamp'])
            today_signals = signal_df[signal_df['timestamp'].dt.date == today]
            signal_counts = today_signals['signal'].value_counts().to_dict()
        except Exception as e:
            print(f"[WARNING] Kunde inte läsa signal_log.csv: {e}")

    buy_log_path = os.path.join(project_root, "logs", "buy_log.csv")
    sell_log_path = os.path.join(project_root, "logs", "sell_log.csv")
    
    buy_total = 0
    sell_total = 0
    
    if os.path.exists(buy_log_path):
        try:
            buy_df = pd.read_csv(buy_log_path, parse_dates=['timestamp'])
            today_buys = buy_df[buy_df['timestamp'].dt.date == today]
            buy_total = today_buys['total_value'].sum() if 'total_value' in today_buys.columns else 0
        except Exception:
            pass
            
    if os.path.exists(sell_log_path):
        try:
            sell_df = pd.read_csv(sell_log_path, parse_dates=['timestamp'])
            today_sells = sell_df[sell_df['timestamp'].dt.date == today]
            sell_total = today_sells['total_value'].sum() if 'total_value' in today_sells.columns else 0
        except Exception:
            pass

    lines = [
        f"*Daglig sammanfattning ({today})*",
        "------------------------------",
        f"💰 Aktuellt portföljvärde: ${total_value:.2f}",
        "------------------------------",
        f"📊 Signaler idag:",
        f"  • KÖP: {signal_counts.get('BUY', 0)}",
        f"  • SÄLJ: {signal_counts.get('SELL', 0)}",
        f"  • HÅLL: {signal_counts.get('HOLD', 0)}",
        "------------------------------",
        f"💸 Transaktioner idag:",
        f"  • Köp: ${buy_total:.2f}",
        f"  • Sälj: ${sell_total:.2f}",
        f"  • Netto: ${sell_total - buy_total:.2f}"
    ]

    message = "\n".join(lines)
    send_telegram(message)

if __name__ == "__main__":
    send_daily_summary()
