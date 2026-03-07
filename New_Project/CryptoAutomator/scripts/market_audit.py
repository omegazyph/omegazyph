# 2026-03-06 | market_audit.py | Author: omegazyph | Updated: 2026-03-06
# Description: US-compatible market audit reading from config.json.
# Uses Kraken for data to bypass regional restrictions. 
# Cleaned up unused imports to satisfy linter requirements.

import json
import os
import ccxt
import pandas as pd
from colorama import Fore, init

# Initialize colorama with autoreset to avoid manual Style.RESET_ALL
init(autoreset=True)

def load_config():
    """Loads trading pairs and settings from the local config.json file."""
    # Look for config.json in the parent directory relative to this script
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"{Fore.RED}Error: config.json not found at {config_path}")
        return None
    except json.JSONDecodeError:
        print(f"{Fore.RED}Error: config.json contains invalid JSON syntax.")
        return None

def get_bollinger_bands(symbol, timeframe='1h', window=20):
    """Calculates Bollinger Bands using Kraken data."""
    exchange = ccxt.cryptocom() 
    try:
        # Fetch 50 candles to ensure a stable 20-period moving average
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=50)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        
        # Calculation: Middle (SMA), Standard Deviation, and Bands
        df['sma'] = df['close'].rolling(window=window).mean()
        df['std'] = df['close'].rolling(window=window).std()
        df['upper'] = df['sma'] + (df['std'] * 2)
        df['lower'] = df['sma'] - (df['std'] * 2)
        
        latest = df.iloc[-1]
        return {
            "price": latest['close'],
            "upper": latest['upper'],
            "lower": latest['lower']
        }
    except Exception as error:
        return f"{Fore.RED}Error fetching {symbol}: {error}"

def main():
    """Main execution block to compare market bands with config thresholds."""
    config = load_config()
    if not config:
        return

    print(f"\n{Fore.CYAN}{'='*55}")
    print(f"{Fore.YELLOW}LIVE AUDIT: BANDS VS. YOUR CONFIG THRESHOLDS")
    print(f"{Fore.CYAN}{'='*55}\n")
    
    for pair in config.get('trading_pairs', []):
        symbol = pair.get('symbol')
        my_threshold = pair.get('buy_threshold', 0.0)
        
        data = get_bollinger_bands(symbol)
        if isinstance(data, dict):
            # Compare current config threshold to the real-time Lower Band
            is_safe = my_threshold <= data['lower']
            safety_status = f"{Fore.GREEN}[SAFE]" if is_safe else f"{Fore.RED}[AGGRESSIVE]"
            
            print(f"{Fore.MAGENTA}{symbol}:")
            print(f"  Current Price:  ${data['price']:,.4f}")
            print(f"  Lower Band:     ${data['lower']:,.4f}")
            print(f"  {Fore.YELLOW}Your Threshold: ${my_threshold:,.4f} {safety_status}")
            print(f"  Target Exit:    ${data['upper']:,.4f}")
            print("-" * 35)
        else:
            print(data)

if __name__ == "__main__":
    main()