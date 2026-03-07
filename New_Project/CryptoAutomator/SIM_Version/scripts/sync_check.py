"""
Date: 2026-03-06
Script Name: sync_check.py
Author: omegazyph
Updated: 2026-03-06

Description: 
A utility script to monitor the Exchange wallet and alert Wayne 
the moment funds transferred from the App become available 
for the API to use.
"""

import ccxt
import os
import time
from dotenv import load_dotenv

load_dotenv()

def watch_for_funds():
    exchange = ccxt.cryptocom({
        'apiKey': os.getenv('CRYPTO_COM_KEY'),
        'secret': os.getenv('CRYPTO_COM_SECRET'),
    })

    print("📡 Monitoring Exchange for incoming funds from App...")
    
    try:
        while True:
            balance = exchange.fetch_balance()
            # Look for any currency with a balance greater than 0
            funds = {coin: amt for coin, amt in balance['total'].items() if amt > 0}
            
            if funds:
                print("\n💰 FUNDS DETECTED!")
                for coin, amount in funds.items():
                    print(f" - {coin}: {amount}")
                print("\nYour Python bot is now fueled and ready to trade.")
                break
            else:
                # Print a dot every 10 seconds to show it's still working
                print(".", end="", flush=True)
                time.sleep(10)
                
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    watch_for_funds()