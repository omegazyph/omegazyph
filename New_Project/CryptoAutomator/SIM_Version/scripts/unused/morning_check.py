"""
Date: 2026-03-06
Script Name: morning_check.py
Author: omegazyph
Updated: 2026-03-06

Description: 
Morning status check. Fetches the current Bitcoin price and 
Wayne's available trading balance on the Crypto.com Exchange.
"""

import ccxt
import os
from dotenv import load_dotenv

# Load those verified keys
load_dotenv()

def morning_report():
    # Setup connection
    exchange = ccxt.cryptocom({
        'apiKey': os.getenv('CRYPTO_COM_KEY'),
        'secret': os.getenv('CRYPTO_COM_SECRET'),
        'enableRateLimit': True,
    })

    try:
        # 1. Fetch current Bitcoin Price
        ticker = exchange.fetch_ticker('BTC/USDT')
        last_price = ticker['last']
        
        # 2. Fetch Account Balance
        balance = exchange.fetch_balance()
        usdt_balance = balance['total'].get('USDT', 0.0)

        print("\n--- Good Morning Report  ---")
        print(f"BTC Current Price: ${last_price:,.2f}")
        print(f"Available USDT: ${usdt_balance:,.2f}")
        
        if usdt_balance < 1.0:
            print("\n⚠️  Note: Your trading balance is low.")
            print("Move some USDT from your App to the Exchange to start testing.")
        else:
            print("\n✅ You have enough 'dry powder' to start micro-trading!")

    except Exception as e:
        print(f"Error fetching morning data: {e}")

if __name__ == "__main__":
    morning_report()