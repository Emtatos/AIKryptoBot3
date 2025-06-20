# =============================================================================
# broker_kraken.py – Implementation av KrakenBroker för AIKryptoBot3
# =============================================================================

import os
import krakenex
from core.broker_interface import BrokerInterface
from config.config import CAPITAL_ALLOC_PCT, MIN_TRADE_VOLUME  # ✅ Korrekt import

class KrakenBroker(BrokerInterface):
    def __init__(self):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        keyfile = os.path.join(project_root, "config", "kraken.key")
        self.api = krakenex.API()
        if os.path.exists(keyfile):
            self.api.load_key(keyfile)
        else:
            print("[WARN] Ingen kraken.key hittad – endast publika anrop fungerar.")

    def get_portfolio(self):
        try:
            res = self.api.query_private("Balance")
            balances = res.get("result", {})

            symbol_map = {
                "XBT.F": "BTC",
                "ETH.F": "ETH",
                "ADA.F": "ADA",
                "DOT.F": "DOT",
                "SOL.F": "SOL",
                "ZUSD": None,
                "MATIC": None,
                "POL.F": None,
                "XLTC": "LTC"
            }

            portfolio = {}
            for sym, qty in balances.items():
                std_sym = symbol_map.get(sym, sym)
                if std_sym and float(qty) > 0:
                    portfolio[std_sym] = portfolio.get(std_sym, 0) + float(qty)
            return portfolio
        except Exception as e:
            print(f"[X] Kunde inte hämta portfölj: {e}")
            return {}

    def get_price(self, symbol):
        symbol_clean = symbol.replace(".F", "")
        pair = f"{symbol_clean}USD"
        try:
            res = self.api.query_public("Ticker", {"pair": pair})
            result = res.get("result")
            if not result:
                raise KeyError("result saknas")
            ticker = next(iter(result.values()))
            return float(ticker["c"][0])
        except Exception as e:
            print(f"[X] Kunde inte hämta pris för {symbol}: {e}")
            return None

    def place_market_order(self, symbol, amount, side="buy"):
        pair = f"{symbol}USD"
        try:
            return self.api.query_private("AddOrder", {
                "pair": pair,
                "type": side,
                "ordertype": "market",
                "volume": amount
            })
        except Exception as e:
            print(f"[X] Fel vid {side}-order för {symbol}: {e}")
            return {"error": [str(e)]}

    def get_cash_balance(self):
        try:
            res = self.api.query_private("Balance")
            balances = res.get("result", {})
            return float(balances.get("ZUSD", 0))
        except Exception as e:
            print(f"[X] Kunde inte hämta USD-saldo: {e}")
            return 0

    def get_allocatable_amount(self, symbol):
        usd_balance = self.get_cash_balance()
        price = self.get_price(symbol)
        if not price or price <= 0:
            return 0
        # Använd 98% av tillgängligt kapital som buffert för avgift
        alloc_usd = usd_balance * CAPITAL_ALLOC_PCT * 0.98
        qty = round(alloc_usd / price, 8)
        return qty if qty >= MIN_TRADE_VOLUME else 0
