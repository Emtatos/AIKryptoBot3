# =============================================================================
# broker_interface.py – Gemensamt gränssnitt för alla broker-implementationer
# =============================================================================

class BrokerInterface:
    def get_portfolio(self):
        """Returnerar en dict med {symbol: mängd} för nuvarande innehav."""
        raise NotImplementedError("Måste implementeras av underklass")

    def get_price(self, symbol):
        """Returnerar senaste marknadspris för symbol (float) eller None."""
        raise NotImplementedError("Måste implementeras av underklass")

    def place_market_order(self, symbol, amount, side="buy"):
        """Lägger en market-order via API. side: 'buy' eller 'sell'."""
        raise NotImplementedError("Måste implementeras av underklass")
