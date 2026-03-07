"""
Date: 2026-03-04
Script Name: exchange_viewer.py
Author: omegazyph
Updated: 2026-03-04

Description: 
This script connects to specified crypto exchanges using CCXT to 
fetch and display current account balances and total value.
"""

import ccxt
import pandas as pd

def get_balance():
    # Initialize the exchange (Example: Binance or Coinbase)
    # You would repeat this for your second platform
    exchange = ccxt.binance({
        'apiKey': 'YOUR_API_KEY_HERE',
        'secret': 'YOUR_SECRET_KEY_HERE',
    })

    print(f"Connecting to {exchange.id}...")

    try:
        # Fetch account balance
        balance = exchange.fetch_balance()
        
        # Filter out assets with 0 balance
        owned_assets = {k: v for k, v in balance['total'].items() if v > 0}
        
        # Create a clean table for Wayne to read
        df = pd.DataFrame(list(owned_assets.items()), columns=['Asset', 'Amount'])
        print("\n--- Current Holdings ---")
        print(df)
        
    except Exception as e:
        print(f"Error connecting to exchange: {e}")

if __name__ == "__main__":
    get_balance()