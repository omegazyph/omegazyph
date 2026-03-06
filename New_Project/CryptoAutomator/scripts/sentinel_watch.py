"""
Date: 2026-03-06
Script Name: sentinel_watch.py
Author: omegazyph
Updated: 2026-03-06

Description: 
A market 'Sentinel' that monitors Bitcoin price stability. 
This is step one of Wayne's trading logic: knowing when to buy.
"""

import ccxt
import time
import os
from dotenv import load_dotenv

load_dotenv()

def run_sentinel():
    exchange = ccxt.cryptocom({
        'apiKey': os.getenv('CRYPTO_COM_KEY'),
        'secret': os.getenv('CRYPTO_COM_SECRET'),
        'enableRateLimit': True,
    })

    print("🛡️ Sentinel Watch Active.")
    print("Wells Fargo is currently down, so we are monitoring prices only.")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            ticker = exchange.fetch_ticker('BTC/USDT')
            price = ticker['last']
            
            # Simple logic: If price is under 69k, it's a 'Buy Zone'
            zone = "📉 BUY ZONE" if price < 69000 else "📈 HOLD ZONE"
            
            print(f"[{time.strftime('%H:%M:%S')}] BTC: ${price:,.2f} | Status: {zone}")
            
            # Check every 60 seconds
            time.sleep(60)

    except KeyboardInterrupt:
        print("\nSentinel standing down. Good luck with the bank, Wayne!")

if __name__ == "__main__":
    run_sentinel()