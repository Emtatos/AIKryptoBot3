# =============================================================================
# recommendation_engine.py – Ger rekommendation: Sälj, Köp eller Gör inget
# Inkluderar peak, vinst/förlust, stop-loss-nivå och trendbaserad logik
# =============================================================================

import os
import sys
import pandas as pd
import io
from datetime import datetime
from reporting.telegram import send_telegram

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.portfolio_manager import PortfolioManager
from core.technical_indicators import calculate_volatility

from core.broker_kraken import KrakenBroker
from config.coin_config import ACTIVE_COINS

price_path = os.path.join(project_root, "data", "price_history.csv")
top_path = os.path.join(project_root, "data", "top_ranked_today.csv")
stoploss_path = os.path.join(project_root, "data", "stop_loss_profile.csv")
trend_conf_path = os.path.join(project_root, "config", "trend_sell_confidence.txt")

SWITCH_THRESHOLD = 0.5
TREND_CONFIDENCE = 1.0
MIN_SELL_VALUE = 1.0

# Läs förtroende för trendbaserad sälj
if os.path.exists(trend_conf_path):
    with open(trend_conf_path, "r") as f:
        for line in f:
            if line.startswith("TREND_SELL_CONFIDENCE"):
                try:
                    TREND_CONFIDENCE = float(line.strip().split("=")[1])
                except:
                    pass

broker = KrakenBroker()
raw_portfolio = broker.get_portfolio()
usd_balance = broker.get_cash_balance()

# === DEBUG: logga råportfölj ===
debug_lines = []
debug_lines.append("[DEBUG] Råportfölj:")
for sym, qty in raw_portfolio.items():
    debug_lines.append(f"- {sym}: {qty:.6f}")

# Filtrera innehav < $1
portfolio = {}
for sym, qty in raw_portfolio.items():
    if sym in ACTIVE_COINS:
        price = broker.get_price(sym)
        if price:
            value = qty * price
            if value >= MIN_SELL_VALUE:
                portfolio[sym] = qty
            else:
                debug_lines.append(f"[IGNORERAD] {sym} under $1 – värde: ${value:.2f}")
        else:
            debug_lines.append(f"[IGNORERAD] {sym} – pris saknas")

if not os.path.exists(price_path) or not os.path.exists(top_path):
    print("[X] Kräver både price_history.csv och top_ranked_today.csv.")
    sys.exit()

price_df = pd.read_csv(price_path, index_col=0, parse_dates=True)
latest_prices = price_df.iloc[-1].to_dict()

top_df = pd.read_csv(top_path).sort_values("score", ascending=False)
best = top_df.iloc[0]
best_coin = best.symbol
best_score = best.score

# Avbryt om bästa coin har negativ score
if best_score < 0:
    print("[INFO] Inget positivt toppval – inga rekommendationer.")
    msg = f"📊 Rekommendation:\n💵 Tillgängligt USD-saldo: ${usd_balance:.2f}\n```[GÖR INGET] Inget innehav och ingen stark kandidat```"
    send_telegram(msg)
    sys.exit()

stoploss_df = pd.read_csv(stoploss_path) if os.path.exists(stoploss_path) else pd.DataFrame()
stoploss_dict = stoploss_df.set_index("symbol").to_dict(orient="index") if not stoploss_df.empty else {}

output = io.StringIO()
print("📊 Rekommendation:", file=output)
print(f"💵 Tillgängligt USD-saldo: ${usd_balance:.2f}", file=output)
print("```", file=output)

buy_signal = False

if not portfolio:
    print(f"[KÖP] {best_coin} (score: {best_score:.2f}) – inget innehav", file=output)
    buy_signal = True
else:
    for coin, qty in portfolio.items():
        current_price = latest_prices.get(coin, 0)
        current_score_row = top_df[top_df.symbol == coin]["score"]
        current_score = current_score_row.values[0] if not current_score_row.empty else -99

        sl = stoploss_dict.get(coin, {})
        stop_price = sl.get("stop_price")
        peak = sl.get("last_peak")
        buy_price = sl.get("buy_price")

        ref_peak = peak if peak and peak > buy_price else buy_price
        pnl = round((current_price - buy_price) * qty, 2) if buy_price else 0
        sl_trigger = round(stop_price * qty, 2) if stop_price else None

        print(f"{coin}: Pris ${current_price:.2f} | Score: {current_score:.2f}", file=output)
        if buy_price:
            print(f"- Inköpspris: ${buy_price:.2f}", file=output)
        if ref_peak:
            print(f"- Senaste peak: ${ref_peak:.2f}", file=output)
        if pnl:
            print(f"- Vinst/förlust: ${pnl:.2f}", file=output)
        if sl_trigger:
            print(f"- Stop-loss vid: ${sl_trigger:.2f}", file=output)

        if stop_price and current_price <= stop_price:
            print(f"[SÄLJ] Stop-loss utlöst! ({current_price:.2f} <= {stop_price:.2f})", file=output)
        elif coin == best_coin:
            print("[GÖR INGET] Du äger redan toppvalet", file=output)
        elif best_score - current_score >= SWITCH_THRESHOLD:
            print(f"[SÄLJ] Byt till {best_coin} (skillnad: {best_score - current_score:.2f})", file=output)
        elif TREND_CONFIDENCE >= 0.5:
            print(f"[SÄLJ] {coin} faller snabbt – trendförsäljning aktiverad (förtroende {TREND_CONFIDENCE:.2f})", file=output)
        else:
            print("[GÖR INGET] Ingen signifikant skillnad", file=output)
        print("", file=output)

print("```", file=output)
text = output.getvalue()
print(text)
for line in debug_lines:
    print(line)

portfolio_manager = PortfolioManager()
recommended_trades = portfolio_manager.get_recommended_trades(top_df)

if recommended_trades:
    for trade in recommended_trades:
        action = trade["action"]
        symbol = trade["symbol"]
        quantity = trade["quantity"]
        reason = trade["reason"]
        
        if action == "BUY":
            result = broker.place_market_order(symbol, quantity, side="buy")
            if result and "error" in result and not result["error"]:
                price = broker.get_price(symbol)
                value = quantity * price
                send_telegram(f"✅ *AUTOMATISKT KÖP*: `{symbol}`\n💰 Antal: {quantity:.6f}\n📈 Pris: ${price:.2f}\n💵 Värde: ${value:.2f}\n📝 Anledning: {reason}")
            else:
                send_telegram(f"❌ *Köp misslyckades* för `{symbol}`: {reason}\n```{result}```")
                
        elif action == "SELL":
            result = broker.place_market_order(symbol, quantity, side="sell")
            if result and "error" in result and not result["error"]:
                price = broker.get_price(symbol)
                value = quantity * price
                send_telegram(f"✅ *AUTOMATISK FÖRSÄLJNING*: `{symbol}`\n💰 Antal: {quantity:.6f}\n📈 Pris: ${price:.2f}\n💵 Värde: ${value:.2f}\n📝 Anledning: {reason}")
            else:
                send_telegram(f"❌ *Försäljning misslyckades* för `{symbol}`: {reason}\n```{result}```")

enhanced_text = f"""
📊 *AI Crypto Analys - Förbättrad Version*

🎯 **Topp 3 Rekommendationer:**
{chr(10).join([f"{i+1}. {row.symbol}: {row.score:.2f} (RSI: {getattr(row, 'rsi', 50):.1f}, Vol: {getattr(row, 'volatility', 0.1):.3f})" for i, row in top_df.head(3).iterrows()])}

📈 **Teknisk Analys:**
• RSI-signaler: {len([r for _, r in top_df.iterrows() if getattr(r, 'rsi', 50) < 30])} köp, {len([r for _, r in top_df.iterrows() if getattr(r, 'rsi', 50) > 70])} sälj
• MACD-signaler: {len([r for _, r in top_df.iterrows() if getattr(r, 'macd_signal', 'SELL') == "BUY"])} köp
• Bollinger Bands: {len([r for _, r in top_df.iterrows() if getattr(r, 'bb_position', 'MIDDLE') == "BELOW"])} under nedre band

⚖️ **Riskhantering:**
• Portföljdiversifiering: {len(recommended_trades)} positioner
• Genomsnittlig volatilitet: {top_df.get('volatility', pd.Series([0.1])).mean():.3f}
• Kapitalallokering: Dynamisk baserat på risk

🤖 **Autonomt läge**: Systemet handlar automatiskt baserat på teknisk analys
"""

send_telegram(enhanced_text)
