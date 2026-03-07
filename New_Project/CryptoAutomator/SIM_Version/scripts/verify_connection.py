"""
Date: 2026-03-05
Script Name: verify_connection.py
Author: omegazyph
Updated: 2026-03-05

Description: 
Performs a private 'Handshake' with the Crypto.com Exchange.
This version now uses the balance variable to display available
funds, clearing the linting warning.
"""

import ccxt
import os
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

def test_handshake():
    # Initialize the exchange with your verified credentials
    exchange = ccxt.cryptocom({
        'apiKey': os.getenv('CRYPTO_COM_KEY'),
        'secret': os.getenv('CRYPTO_COM_SECRET'),
        'enableRateLimit': True,
    })

    try:
        print("Connecting to Crypto.com Exchange...")
        
        # Now we fetch AND use the balance variable
        balance = exchange.fetch_balance()
        
        print("✅ Handshake Successful!")
        print(f"Connected as: {exchange.name}")

        # Filter for coins that actually have a balance
        # This uses the 'total' dictionary within the balance object
        active_funds = {coin: amt for coin, amt in balance['total'].items() if amt > 0}

        if active_funds:
            print("\n--- Current Exchange Funds ---")
            for coin, amount in active_funds.items():
                print(f"{coin}: {amount}")
        else:
            print("\nYour Exchange wallet is currently empty ($0.00).")
            print("Tip: Use the 'Transfer' button in your phone app to move funds to the Exchange.")
        
    except Exception as error:
        print(f"❌ Handshake Failed: {error}")
        print("Check for extra spaces in your .env or verify 'Can Read' is enabled.")

if __name__ == "__main__":
    test_handshake()