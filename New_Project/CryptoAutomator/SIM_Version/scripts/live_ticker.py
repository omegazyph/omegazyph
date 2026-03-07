"""
Date: 2026-03-06
Script Name: live_ticker.py
Author: omegazyph
Updated: 2026-03-06

Description: 
A real-time price tracker for BTC/USDT. This helps Wayne monitor 
market volatility from his VS Code terminal before launching 
automated trades.
"""

import ccxt
import time
import os
from dotenv import load_dotenv

# Load the keys
load_dotenv()

def start_ticker(symbol='BTC/USDT'):
    # Initialize the exchange
    exchange = ccxt.cryptocom({
        'apiKey': os.getenv('CRYPTO_COM_KEY'),
        'secret': os.getenv('CRYPTO_COM_SECRET'),
        'enableRateLimit': True,
    })

    print(f"--- Monitoring {symbol} Live ---")
    print("Press Ctrl+C to stop the tracker.\n")

    try:
        while True:
            # Fetch the latest price data
            ticker = exchange.fetch_ticker(symbol)
            current_price = ticker['last']
            high_24h = ticker['high']
            low_24h = ticker['low']

            # Clear line and print update
            print(f"Price: ${current_price:,.2f} | 24h High: ${high_24h:,.2f} | 24h Low: ${low_24h:,.2f}", end='\r')
            
            # Wait 5 seconds before next update
            time.sleep(5)

    except KeyboardInterrupt:
        print("\n\nTracker stopped. Have a productive day, Wayne!")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    start_ticker()