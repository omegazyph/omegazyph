"""
Date: 2026-03-05
Script Name: market_scanner.py
Author: omegazyph
Updated: 2026-03-05

Description: 
This script scans the real-time Order Book (Market Depth) for 
BTC/USDT on the Crypto.com Exchange. It helps Wayne identify 
where the 'Buy Walls' and 'Sell Walls' are located.
"""

import ccxt
import os
from dotenv import load_dotenv

# Load the verified keys from your .env
load_dotenv()

def scan_order_book(symbol='BTC/USDT'):
    # Initialize the exchange connection
    exchange = ccxt.cryptocom({
        'apiKey': os.getenv('CRYPTO_COM_KEY'),
        'secret': os.getenv('CRYPTO_COM_SECRET'),
        'enableRateLimit': True,
    })

    try:
        print(f"--- Scanning Market Depth for {symbol} ---")
        
        # Fetch the order book (top 10 bids and asks)
        order_book = exchange.fetch_order_book(symbol, limit=10)
        
        bids = order_book['bids']  # People wanting to buy (support)
        asks = order_book['asks']  # People wanting to sell (resistance)

        print("\nTop 5 BUY Orders (Bids):")
        for i in range(5):
            print(f"Price: ${bids[i][0]:.2f} | Quantity: {bids[i][1]}")

        print("\nTop 5 SELL Orders (Asks):")
        for i in range(5):
            print(f"Price: ${asks[i][0]:.2f} | Quantity: {asks[i][1]}")

        # Calculate the "Spread" (The gap between the highest buy and lowest sell)
        spread = asks[0][0] - bids[0][0]
        print(f"\nMarket Spread: ${spread:.2f}")

    except Exception as error:
        print(f"Error scanning market: {error}")

if __name__ == "__main__":
    scan_order_book()