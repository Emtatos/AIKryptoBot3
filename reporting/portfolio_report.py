# =============================================================================
# portfolio_report.py – Skickar aktuella innehav till Telegram (> $1)
# =============================================================================

import os
import sys
import pandas as pd

# Sätt sys.path tidigt
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.broker_kraken import KrakenBroker
from reporting.telegram import send_telegram

MIN_DISPLAY_VALUE = 1.00  # USD

def send_portfolio_report():
    broker = KrakenBroker()
    portfolio = broker.get_portfolio()
    if not portfolio:
        send_telegram("💼 Inget innehav att visa.")
        return

    prices = {sym: broker.get_price(sym) for sym in portfolio.keys()}
    lines = ["📦 *Aktuella innehav (>$1)*", "```"]
    total_value = 0

    for symbol, qty in portfolio.items():
        price = prices.get(symbol)
        if price is None:
            continue
        value = qty * price
        if value < MIN_DISPLAY_VALUE:
            continue
        total_value += value
        lines.append(f"{symbol}: {qty:.6f} × ${price:.2f} = ${value:.2f}")

    if total_value > 0:
        lines.append("--------------------------")
        lines.append(f"Totalt värde: ${total_value:.2f}")
        lines.append("```")
        send_telegram("\n".join(lines))
    else:
        send_telegram("💼 Inget innehav över $1.00 att visa.")

# =============================================================================
# TEST
# =============================================================================
if __name__ == "__main__":
    send_portfolio_report()
