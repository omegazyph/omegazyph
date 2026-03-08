"""
Date: 2026-03-07
Script Name: check_exchange_balance.py
Author: omegazyph
Updated: 2026-03-07
Description: 
    Diagnostic tool to verify real-world connectivity and balance.
    Prints every asset found in the Crypto.com Exchange wallet.
"""

import ccxt
import os
from pathlib import Path
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Initialize Colors
init(autoreset=True)

# --- PATH LOGIC ---
script_path = Path(__file__).resolve()
project_root = script_path.parent.parent
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)

def run_diagnostic():
    print(f"{Fore.CYAN}{'='*50}")
    print(f"{Fore.CYAN}  WAYNE'S CONNECTION DIAGNOSTIC")
    print(f"{Fore.CYAN}{'='*50}\n")

    # Connect to exchange
    exchange = ccxt.cryptocom({
        "apiKey": os.getenv("CRYPTO_COM_KEY"),
        "secret": os.getenv("CRYPTO_COM_SECRET"),
        "enableRateLimit": True
    })

    try:
        print(f"{Fore.YELLOW}Testing API Keys...")
        balance_data = exchange.fetch_balance()
        
        # Filter out anything with 0 balance
        all_assets = balance_data.get('total', {})
        real_funds = {coin: amt for coin, amt in all_assets.items() if amt > 0}

        if not real_funds:
            print(f"\n{Fore.RED}RESULT: Connection Successful, but BALANCE IS EMPTY.")
            print(f"{Fore.WHITE}Possible Reasons:")
            print(" 1. Funds are in the 'App Wallet' and not 'Exchange Wallet'.")
            print(" 2. API Key does not have 'Spot Balance' permissions enabled.")
        else:
            print(f"\n{Fore.GREEN}RESULT: Connection Successful! Found the following:")
            print(f"{'-'*30}")
            for coin, amount in real_funds.items():
                print(f" {Fore.WHITE}{coin:<8}: {Fore.GREEN}{amount:.8f}")
            print(f"{'-'*30}")
            
            if "USDT" in real_funds:
                print(f"\n{Fore.CYAN}Ready for Live Trading: {Fore.GREEN}YES")
            else:
                print(f"\n{Fore.YELLOW}Ready for Live Trading: {Fore.RED}NO (USDT missing)")

    except Exception as error:
        print(f"\n{Fore.RED}CRITICAL ERROR: Could not connect to exchange.")
        print(f"{Fore.WHITE}Error Details: {error}")

if __name__ == "__main__":
    run_diagnostic()