"""
Date: 2026-03-06
Script Name: main_bot_loop.py
Author: omegazyph
Updated: 2026-03-06

Description: 
Wayne's silent 24/7 Autonomous Bot. Reads from config.json.
Removed winsound alerts for a quieter background operation.
"""

import ccxt
import time
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load your API keys
load_dotenv()

def load_config():
    # Looks one level up from /scripts/ to find config.json in the root
    script_path = Path(__file__).resolve()
    project_root = script_path.parent.parent
    config_path = project_root / 'config.json'
    
    with open(config_path, 'r') as f:
        return json.load(f)

def run_bot():
    # Initialize the Crypto.com Exchange connection
    exchange = ccxt.cryptocom({
        'apiKey': os.getenv('CRYPTO_COM_KEY'),
        'secret': os.getenv('CRYPTO_COM_SECRET'),
        'enableRateLimit': True,
    })

    print(f"🚀 {time.strftime('%H:%M:%S')} | Autonomous Bot Started (Silent Mode).")
    print("Monitoring prices based on your config.json...")

    while True:
        try:
            # Reload config every loop so Wayne can change settings 'live'
            config = load_config()
            pairs = config['trading_pairs']
            interval = config['global_settings']['check_interval_seconds']
            
            # Check the "Trading Fuel"
            balance = exchange.fetch_balance()
            usdt_ready = balance['total'].get('USDT', 0.0)
            usd_ready = balance['total'].get('USD', 0.0)
            total_cash = usdt_ready + usd_ready
            
            print(f"\n--- Scan Start | Available Cash: ${total_cash:.2f} ---")

            for pair in pairs:
                if not pair['enabled']:
                    continue

                symbol = pair['symbol']
                ticker = exchange.fetch_ticker(symbol)
                price = ticker['last']
                threshold = pair['buy_threshold']

                # Visual Logic
                status_icon = "🟢" if price <= threshold else "⚪"
                print(f"{status_icon} {pair['name']}: ${price:,.2f} (Target: < ${threshold:,.2f})")

                if price <= threshold and total_cash >= 1.0:
                    print(f"   📊 SIGNAL: Price is favorable for {symbol}!")

            print(f"--- Sleeping {interval}s ---")
            time.sleep(interval)

        except Exception as e:
            # If the internet blips, wait a minute and try again
            print(f"\n[{time.strftime('%H:%M:%S')}] Connection Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    run_bot()