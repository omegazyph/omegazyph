"""
Date: 2026-03-06
Script Name: main_bot_loop.py
Author: omegazyph
Updated: 2026-03-06

Description: 
Wayne's 24/7 Autonomous Bot with full color terminal support.
Uses Colorama for status highlighting and easy readability.
"""

import ccxt
import time
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Initialize Colorama for Windows 11 compatibility
init(autoreset=True)

load_dotenv()

class Colors:
    HEADER = Fore.CYAN + Style.BRIGHT
    MONEY = Fore.GREEN + Style.BRIGHT
    PRICE = Fore.YELLOW
    SIGNAL = Fore.MAGENTA + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    RESET = Style.RESET_ALL

def load_config():
    script_path = Path(__file__).resolve()
    project_root = script_path.parent.parent
    config_path = project_root / 'config.json'
    with open(config_path, 'r') as f:
        return json.load(f)

def run_bot():
    exchange = ccxt.cryptocom({
        'apiKey': os.getenv('CRYPTO_COM_KEY'),
        'secret': os.getenv('CRYPTO_COM_SECRET'),
        'enableRateLimit': True,
    })

    print(f"{Colors.HEADER}🚀 Legion Bot: Autonomous Dashboard Engaged")
    print(f"{Colors.HEADER}System: Windows 11 | Mode: Silent Color{Colors.RESET}\n")

    while True:
        try:
            config = load_config()
            pairs = config['trading_pairs']
            interval = config['global_settings']['check_interval_seconds']
            
            balance = exchange.fetch_balance()
            usdt_ready = balance['total'].get('USDT', 0.0)
            usd_ready = balance['total'].get('USD', 0.0)
            total_cash = usdt_ready + usd_ready
            
            # Header with current balance
            timestamp = time.strftime('%H:%M:%S')
            print(f"{Colors.HEADER}[{timestamp}] {Colors.MONEY}Balance: ${total_cash:.2f}{Colors.RESET}")

            for pair in pairs:
                if not pair['enabled']:
                    continue

                symbol = pair['symbol']
                ticker = exchange.fetch_ticker(symbol)
                price = ticker['last']
                threshold = pair['buy_threshold']

                # Price Comparison Color
                price_color = Colors.MONEY if price <= threshold else Colors.PRICE
                
                print(f"  {pair['name']}: {price_color}${price:,.2f} {Colors.RESET}(Target: < ${threshold:,.2f})")

                if price <= threshold and total_cash >= 1.0:
                    print(f"  {Colors.SIGNAL}>> ENTRY SIGNAL DETECTED FOR {symbol} <<")

            print(f"{Style.DIM}--- Waiting {interval}s ---{Colors.RESET}")
            time.sleep(interval)

        except Exception as e:
            print(f"{Colors.ERROR}❌ Connection Error: {e}{Colors.RESET}")
            time.sleep(60)

if __name__ == "__main__":
    run_bot()