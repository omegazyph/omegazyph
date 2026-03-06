"""
Date: 2026-03-05
Script Name: verify_connection.py
Author: omegazyph
Updated: 2026-03-05

Description: 
This script performs a private 'Handshake' with the Crypto.com 
Exchange to ensure the API Key and Secret Key are valid.
"""

import ccxt
import os
from dotenv import load_dotenv

# Load variables from the .env file in the root project folder
load_dotenv()

def test_handshake():
    # Initialize the exchange with your credentials
    exchange = ccxt.cryptocom({
        'apiKey': os.getenv('CRYPTO_COM_KEY'),
        'secret': os.getenv('CRYPTO_COM_SECRET'),
        'enableRateLimit': True,
    })

    try:
        # Fetching markets is a public action, but fetch_balance is private.
        # This confirms the keys are actually working.
        print("Connecting to Crypto.com Exchange...")
        balance = exchange.fetch_balance()
        
        print("✅ Handshake Successful!")
        print(f"Connected as: {exchange.name}")
        print("Your Lenovo Legion is now communicating with the Exchange API.")
        
    except Exception as error:
        print(f"❌ Handshake Failed: {error}")
        print("Check for extra spaces in your .env or verify 'Can Read' is enabled.")

if __name__ == "__main__":
    test_handshake()