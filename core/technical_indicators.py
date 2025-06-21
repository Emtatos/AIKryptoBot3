import pandas as pd
import numpy as np

def calculate_rsi(prices, period=14):
    """Calculate RSI (Relative Strength Index)"""
    if len(prices) < period + 1:
        return pd.Series([50] * len(prices), index=prices.index)
    
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """Calculate MACD (Moving Average Convergence Divergence)"""
    if len(prices) < slow:
        empty_series = pd.Series([0] * len(prices), index=prices.index)
        return empty_series, empty_series, empty_series
    
    ema_fast = prices.ewm(span=fast).mean()
    ema_slow = prices.ewm(span=slow).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

def calculate_bollinger_bands(prices, period=20, std_dev=2):
    """Calculate Bollinger Bands"""
    if len(prices) < period:
        sma = pd.Series([prices.mean()] * len(prices), index=prices.index)
        std = pd.Series([prices.std()] * len(prices), index=prices.index)
    else:
        sma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
    
    upper_band = sma + (std * std_dev)
    lower_band = sma - (std * std_dev)
    return upper_band.fillna(sma), sma.fillna(prices.mean()), lower_band.fillna(sma)

def calculate_volatility(prices, period=14):
    """Calculate price volatility (standard deviation of returns)"""
    if len(prices) < 2:
        return pd.Series([0.1] * len(prices), index=prices.index)
    
    returns = prices.pct_change()
    if len(returns) < period:
        volatility = pd.Series([returns.std()] * len(returns), index=returns.index)
    else:
        volatility = returns.rolling(window=period).std() * np.sqrt(252)
    
    return volatility.fillna(0.1)

def calculate_volume_sma(volumes, period=20):
    """Calculate Simple Moving Average of volume"""
    if len(volumes) < period:
        return pd.Series([volumes.mean()] * len(volumes), index=volumes.index)
    
    return volumes.rolling(window=period).mean().fillna(volumes.mean())

def calculate_momentum_score(prices, lookbacks=[3, 7, 14], weights=[0.3, 0.3, 0.4]):
    """Calculate weighted momentum score"""
    if len(prices) < max(lookbacks):
        return 0
    
    total_score = 0
    for lookback, weight in zip(lookbacks, weights):
        if len(prices) >= lookback:
            pct_change = (prices.iloc[-1] - prices.iloc[-lookback]) / prices.iloc[-lookback] * 100
            total_score += pct_change * weight
    
    return total_score
