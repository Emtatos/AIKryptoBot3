# =============================================================================
# coin_config.py – Definierar vilka coins som analyseras av AIKryptoBot3
# =============================================================================

# Lista över hårdkodade coins med bra analysunderlag
ACTIVE_COINS = [
    "BTC",  # Bitcoin
    "ETH",  # Ethereum
    "ADA",  # Cardano
    "BNB",  # Binance Coin
    "XRP",  # Ripple
    "SOL",  # Solana
    "DOT",  # Polkadot
    "LTC"   # Litecoin
]

# Hjälpfunktion
def is_valid_coin(symbol):
    return symbol in ACTIVE_COINS
