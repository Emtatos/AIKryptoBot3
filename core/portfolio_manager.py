import os
import sys
import pandas as pd
import numpy as np

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.broker_kraken import KrakenBroker
from config.config import CAPITAL_ALLOC_PCT

class PortfolioManager:
    def __init__(self):
        self.broker = KrakenBroker()
        self.max_positions = 3
        self.min_allocation = 0.15
        self.max_allocation = 0.50
        
    def calculate_position_sizes(self, top_coins_df):
        """Calculate optimal position sizes based on scores and volatility"""
        if len(top_coins_df) == 0:
            return {}
            
        portfolio = self.broker.get_portfolio()
        usd_balance = portfolio.get("USD", 0)
        available_capital = usd_balance * CAPITAL_ALLOC_PCT
        
        if available_capital <= 0:
            return {}
        
        selected_coins = top_coins_df.head(self.max_positions)
        
        weights = {}
        total_weight = 0
        
        for _, row in selected_coins.iterrows():
            coin = row["symbol"]
            score = row["score"]
            volatility = row.get("volatility", 0.1)
            
            risk_adjusted_score = score / (1 + volatility * 2)
            weight = max(risk_adjusted_score, 0.1)
            weights[coin] = weight
            total_weight += weight
            
        position_sizes = {}
        for coin, weight in weights.items():
            normalized_weight = weight / total_weight if total_weight > 0 else 1.0 / len(weights)
            constrained_weight = max(self.min_allocation, 
                                   min(self.max_allocation, normalized_weight))
            position_sizes[coin] = available_capital * constrained_weight
            
        return position_sizes
        
    def get_recommended_trades(self, top_coins_df):
        """Get recommended trades based on current portfolio and targets"""
        current_portfolio = self.broker.get_portfolio()
        target_positions = self.calculate_position_sizes(top_coins_df)
        
        trades = []
        
        for coin, qty in current_portfolio.items():
            if coin == "USD":
                continue
                
            current_price = self.broker.get_price(coin)
            if not current_price:
                continue
                
            current_value = qty * current_price
            target_value = target_positions.get(coin, 0)
            
            if target_value == 0 or current_value > target_value * 1.1:
                trades.append({
                    "action": "SELL",
                    "symbol": coin,
                    "quantity": qty,
                    "reason": "Not in target portfolio" if target_value == 0 else "Overweight"
                })
                
        for coin, target_value in target_positions.items():
            current_qty = current_portfolio.get(coin, 0)
            current_price = self.broker.get_price(coin)
            if not current_price:
                continue
                
            current_value = current_qty * current_price
            
            if current_value < target_value * 0.9:
                buy_value = target_value - current_value
                buy_qty = buy_value / current_price
                
                trades.append({
                    "action": "BUY",
                    "symbol": coin,
                    "quantity": buy_qty,
                    "value": buy_value,
                    "reason": "New position" if current_qty == 0 else "Underweight"
                })
                
        return trades
