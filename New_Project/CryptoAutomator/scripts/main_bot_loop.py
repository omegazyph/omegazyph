"""
Date: 2026-03-06
Script Name: main_bot_loop.py
Author: omegazyph
Updated: 2026-03-06

Description: 
Wayne's 24/7 Bot with CSV Logging. Records every buy 
transaction to a local file for permanent record keeping.
"""

import ccxt
import time
import os
import json
import csv # Added for Excel-compatible logging
from pathlib import Path
from dotenv import load_dotenv
from colorama import init, Fore, Style

init(autoreset=True)
load_dotenv()

class Colors:
    HEADER = Fore.CYAN + Style.BRIGHT
    MONEY = Fore.GREEN + Style.BRIGHT
    PRICE = Fore.YELLOW
    SIGNAL = Fore.MAGENTA + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    SYSTEM = Fore.BLUE + Style.DIM
    RESET = Style.RESET_ALL

def load_config():
    script_path = Path(__file__).resolve()
    project_root = script_path.parent.parent
    config_path = project_root / 'config.json'
    with open(config_path, 'r') as f:
        return json.load(f)

def log_transaction(symbol, side, amount, price):
    """Writes trade details to a CSV file in the project root."""
    script_path = Path(__file__).resolve()
    log_path = script_path.parent.parent / 'trading_log.csv'
    
    file_exists = os.path.isfile(log_path)
    
    with open(log_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Add header if the file is brand new
        if not file_exists:
            writer.writerow(['Timestamp', 'Symbol', 'Side', 'Amount', 'Price', 'Total_USD'])
        
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        total_usd = amount * price
        writer.writerow([timestamp, symbol, side, amount, f"{price:.2f}", f"{total_usd:.2f}"])
    
    print(f"{Colors.MONEY}📁 Transaction logged to trading_log.csv{Colors.RESET}")

def run_bot():
    exchange = ccxt.cryptocom({
        'apiKey': os.getenv('CRYPTO_COM_KEY'),
        'secret': os.getenv('CRYPTO_COM_SECRET'),
        'enableRateLimit': True,
    })

    print(f"{Colors.HEADER}🚀 Legion Bot: Transaction Logging Active")
    
    while True:
        try:
            config = load_config()
            pairs = config['trading_pairs']
            interval = config['global_settings']['check_interval_seconds']
            
            balance = exchange.fetch_balance()
            total_cash = balance['total'].get('USDT', 0.0) + balance['total'].get('USD', 0.0)
            
            print(f"\n{Colors.HEADER}--- Scan Start | Balance: ${total_cash:.2f} ---")

            for pair in pairs:
                if not pair['enabled']: 
                    continue

                symbol = pair['symbol']
                ticker = exchange.fetch_ticker(symbol)
                price = ticker['last']
                threshold = pair['buy_threshold']

                if price <= threshold and total_cash >= 1.0:
                    print(f"{Colors.SIGNAL}💰 SIGNAL MATCHED: Executing Simulated Buy for {symbol}...")
                    
                    # SIMULATED BUY FOR TESTING
                    # In a real trade, 'amount' would come from your order result
                    test_amount = 0.0001 
                    
                    # Log it!
                    log_transaction(symbol, "BUY", test_amount, price)
                else:
                    print(f"  {pair['name']}: ${price:,.2f} (Target: < ${threshold:,.2f})")

            time.sleep(interval)

        except Exception as e:
            print(f"{Colors.ERROR}❌ Error: {e}{Colors.RESET}")
            time.sleep(60)

if __name__ == "__main__":
    run_bot()