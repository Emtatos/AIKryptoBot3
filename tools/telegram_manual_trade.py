# =============================================================================
# telegram_manual_trade.py – Hanterar Telegram-knappar för manuell "Sälj allt" och "Köp"
# =============================================================================

import os
import sys
import pandas as pd
from datetime import datetime
from reporting.telegram import send_telegram, send_telegram_with_buttons

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.broker_kraken import KrakenBroker
from config.coin_config import ACTIVE_COINS
from config.telegram_config import TELEGRAM_TOKEN

MIN_SELL_VALUE = 1.0  # USD
SELL_LOG_PATH = os.path.join(project_root, "logs", "sell_log.csv")
BUY_LOG_PATH = os.path.join(project_root, "logs", "buy_log.csv")

broker = KrakenBroker()


def handle_callback(callback_data):
    if callback_data == "SELL_ALL_REQUEST":
        buttons = [("✅ Bekräfta", "SELL_ALL_CONFIRM"), ("❌ Avbryt", "SELL_ALL_CANCEL")]
        send_telegram_with_buttons("⚠️ Bekräfta att du vill sälja alla innehav:", buttons)
        return

    elif callback_data == "SELL_ALL_CONFIRM":
        portfolio = broker.get_portfolio()
        prices = {sym: broker.get_price(sym) for sym in portfolio.keys()}

        log_entries = []
        lines = []

        for sym, qty in portfolio.items():
            price = prices.get(sym)
            if price and qty * price > MIN_SELL_VALUE:
                res = broker.place_market_order(sym, qty, side="sell")
                if res and "error" in res and not res["error"]:
                    total = round(price * qty, 2)
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_entries.append({
                        "timestamp": timestamp,
                        "symbol": sym,
                        "amount": qty,
                        "price": price,
                        "total_value": total,
                        "reason": "manual_sell"
                    })
                    lines.append(f"✅ Sålt {sym}: {qty:.6f}")
                else:
                    lines.append(f"[X] Kunde inte sälja {sym}: {res}")

        if log_entries:
            df_log = pd.DataFrame(log_entries)
            header = not os.path.exists(SELL_LOG_PATH)
            df_log.to_csv(SELL_LOG_PATH, mode="a", header=header, index=False)

        if not lines:
            lines = ["⚠️ Inget att sälja (över $1)"]

        send_telegram("\n".join(lines))
        send_telegram("🔒 Försäljningsval har registrerats. Knappar inaktiverade.")

    elif callback_data == "SELL_ALL_CANCEL":
        send_telegram("❌ Försäljning avbruten.")
        send_telegram("🔒 Försäljningsval har registrerats. Knappar inaktiverade.")

    elif callback_data.startswith("BUY_REQUEST_"):
        coin = callback_data.replace("BUY_REQUEST_", "")
        buttons = [("✅ Bekräfta köp", f"BUY_CONFIRM_{coin}"), ("❌ Avbryt", "BUY_CANCEL")]
        send_telegram_with_buttons(f"⚠️ Bekräfta att du vill köpa {coin}:", buttons)

    elif callback_data.startswith("BUY_CONFIRM_"):
        coin = callback_data.replace("BUY_CONFIRM_", "")
        qty = broker.get_allocatable_amount(coin)
        price = broker.get_price(coin)
        if qty > 0 and price:
            res = broker.place_market_order(coin, qty, side="buy")
            if res and "error" in res and not res["error"]:
                total = round(qty * price, 2)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                df_log = pd.DataFrame([{ 
                    "timestamp": timestamp,
                    "symbol": coin,
                    "amount": qty,
                    "price": price,
                    "total_value": total,
                    "reason": "manual_buy"
                }])
                header = not os.path.exists(BUY_LOG_PATH)
                df_log.to_csv(BUY_LOG_PATH, mode="a", header=header, index=False)
                send_telegram(f"✅ Köpt {coin}: {qty:.6f} för totalt ${total:.2f}")
            else:
                send_telegram(f"[X] Kunde inte köpa {coin}: {res}")
        else:
            send_telegram(f"⚠️ Kan inte köpa {coin} – ogiltigt belopp eller pris")

    elif callback_data == "BUY_CANCEL":
        send_telegram("❌ Köp avbruten.")
        send_telegram("🔒 Köpval har registrerats. Knappar inaktiverade.")


# === Direkt testbar ===
if __name__ == "__main__":
    handle_callback("SELL_ALL_REQUEST")
