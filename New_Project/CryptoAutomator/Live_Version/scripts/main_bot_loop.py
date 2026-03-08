"""
Date: 2026-03-07
Script Name: main_bot_loop.py
Author: omegazyph
Updated: 2026-03-07
Description: 
    Wayne's 15% Drop Re-Buy Bot - Laptop Edition.
    Uses "USD Bundle" balance from Crypto.com Exchange.
    Runs on Lenovo Legion (Windows 11) using local VSCode environment.
    Simulates trades based on real-time USD exchange data.
"""

import ccxt
import time
import os
import json
import csv
import ctypes
from pathlib import Path
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Initialize Colors for VSCode Terminal
init(autoreset=True, strip=False)

# --- WINDOWS STAY-AWAKE LOGIC ---
# Prevents the Legion laptop from sleeping while the script is active
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001

def prevent_sleep():
    """Tells Windows 11 not to put the system to sleep."""
    if os.name == 'nt':
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)

def allow_sleep():
    """Restores default Windows sleep settings."""
    if os.name == 'nt':
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)

# --- PATH LOGIC ---
# Points to the .env in your project folder on the laptop
script_path = Path(__file__).resolve()
project_root = script_path.parent.parent
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)

# --- CONSTANTS ---
REBUY_DROP_PERCENT = 15.0
PROFIT_TARGET_PERCENT = 15.0
MAX_ACTIVITY_LOGS = 5

class Colors:
    HEADER = Fore.CYAN + Style.BRIGHT
    MONEY = Fore.GREEN + Style.BRIGHT
    PRICE = Fore.YELLOW
    SIGNAL = Fore.MAGENTA + Style.BRIGHT
    SELL = Fore.RED + Style.BRIGHT
    SYSTEM = Fore.BLUE + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    RESET = Style.RESET_ALL

# Global state
recent_activities = []
virtual_balance = 0.00 

def clear_screen():
    """Clears the VSCode terminal for a clean dashboard view."""
    os.system("cls" if os.name == "nt" else "clear")

def get_paths():
    """Returns absolute paths for config and log files on your laptop."""
    return project_root, project_root / "config.json", project_root / "trading_log.csv"

def load_config():
    """Reads your trading pairs and settings from config.json."""
    _, config_path, _ = get_paths()
    with open(config_path, mode="r", encoding="utf-8") as file:
        return json.load(file)

def log_trade(symbol, side, amount, price, wallet, note):
    """Records every simulated trade to a CSV file for your records."""
    global recent_activities
    _, _, log_path = get_paths()
    current_time_short = time.strftime("%H:%M:%S")
    current_time_full = time.strftime("%Y-%m-%d %H:%M:%S")
    
    file_exists = os.path.isfile(log_path)
    with open(log_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Symbol", "Side", "Amount", "Price", "Wallet", "Note"])
        writer.writerow([current_time_full, symbol, side, f"{amount:.8f}", f"{price:.8f}", f"{wallet:.2f}", note])
    
    side_color = Colors.MONEY if "BUY" in side else Colors.SELL
    activity_message = f"[{current_time_short}] {side_color}{side:<10}{Colors.RESET} {symbol} at ${price:,.4f} - {note}"
    recent_activities.insert(0, activity_message)
    if len(recent_activities) > MAX_ACTIVITY_LOGS:
        recent_activities.pop()

def recover_state_from_csv():
    """Checks the CSV to see if you were already holding coins before the script restarted."""
    global virtual_balance, recent_activities
    _, _, log_path = get_paths()
    trades = {}
    if not os.path.isfile(log_path):
        return trades

    try:
        with open(log_path, mode="r", encoding="utf-8") as file:
            csv_data = list(csv.DictReader(file))
            if not csv_data:
                return trades

            for row in csv_data:
                symbol = row["Symbol"]
                side = row["Side"]
                price = float(row["Price"])
                amount = float(row["Amount"])
                virtual_balance = float(row["Wallet"])

                if side == "SIM_BUY":
                    if symbol not in trades:
                        trades[symbol] = {"status": "HOLDING", "coins": 0.0, "total_cost": 0.0, "last_price": 0.0, "count": 0}
                    trades[symbol]["coins"] += amount
                    trades[symbol]["total_cost"] += (amount * price)
                    trades[symbol]["last_price"] = price
                    trades[symbol]["count"] += 1
                elif side == "SIM_SELL":
                    trades[symbol] = {"status": "WAITING", "coins": 0.0, "total_cost": 0.0, "last_price": 0.0, "count": 0}
            
            # Show the last few actions in the dashboard
            for row in reversed(csv_data[-MAX_ACTIVITY_LOGS:]):
                side_color = Colors.MONEY if "BUY" in row["Side"] else Colors.SELL
                recent_activities.append(f"[{row['Timestamp'].split(' ')[1]}] {side_color}{row['Side']:<10}{Colors.RESET} {row['Symbol']} at ${float(row['Price']):,.4f}")
                
    except Exception as error:
        print(f"{Colors.ERROR}Recovery Warning: {error}")
    return trades

def run_bot():
    """Main loop that runs on your laptop and checks prices every 30 seconds."""
    global virtual_balance
    prevent_sleep() # Keep the Legion awake while bot is active
    
    # Initialize the exchange connection
    exchange = ccxt.cryptocom({
        "apiKey": os.getenv("CRYPTO_COM_KEY"),
        "secret": os.getenv("CRYPTO_COM_SECRET"),
        "enableRateLimit": True
    })
    
    trade_state = recover_state_from_csv()
    
    try:
        while True:
            config_data = load_config()
            trading_pairs = config_data["trading_pairs"]
            check_interval = config_data.get("global_settings", {}).get("check_interval_seconds", 30)
            
            # Fetch the real USD balance you confirmed ($18.59)
            balance_data = exchange.fetch_balance()
            real_balance = balance_data.get('total', {}).get("USD", 0.0)
            virtual_balance = real_balance

            clear_screen()
            print(f"{Colors.HEADER}======================================================================")
            print(f" {Colors.HEADER}WAYNE'S LAPTOP BOT | {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f" {Colors.HEADER}REAL USD BALANCE: {Colors.RESET}${real_balance:.2f}")
            print(f"{Colors.HEADER}======================================================================")
            print(f"{'SYMBOL':<10} {'STATUS':<15} {'PRICE':<12} {'TARGET/AVG':<12} {'P/L %':<10} {'BUYS'}")
            print("-" * 75)

            for pair in trading_pairs:
                if not pair.get("enabled", True):
                    continue
                    
                # Auto-switch symbols to /USD to match your wallet
                symbol = pair["symbol"].replace("USDT", "USD")
                
                if symbol not in trade_state:
                    trade_state[symbol] = {"status": "WAITING", "coins": 0.0, "total_cost": 0.0, "last_price": 0.0, "count": 0}
                
                state = trade_state[symbol]
                ticker = exchange.fetch_ticker(symbol)
                current_price = ticker["last"]

                if state["status"] == "WAITING":
                    buy_target = pair["buy_threshold"]
                    print(f"{symbol:<10} {Colors.SYSTEM}{'SEARCHING':<15} ${current_price:<11,.4f} ${buy_target:<11,.4f} {'---':<10} {state['count']}/3")
                    
                    if current_price <= buy_target and virtual_balance >= 2.0:
                        virtual_balance -= 2.0
                        coins = 2.0 / current_price
                        state.update({"status": "HOLDING", "coins": coins, "total_cost": 2.0, "last_price": current_price, "count": 1})
                        log_trade(symbol, "SIM_BUY", coins, current_price, virtual_balance, "Initial Entry")

                elif state["status"] == "HOLDING":
                    avg_cost = state["total_cost"] / state["coins"]
                    profit_pct = ((current_price - avg_cost) / avg_cost) * 100
                    drop_pct = ((state["last_price"] - current_price) / state["last_price"]) * 100
                    
                    p_color = Colors.MONEY if profit_pct >= 0 else Colors.SELL
                    print(f"{symbol:<10} {Colors.MONEY}{'HOLDING':<15} ${current_price:<11,.4f} ${avg_cost:<11,.4f} {p_color}{profit_pct:>+6.2f}%{Colors.RESET}   {state['count']}/3")

                    # Logic for 15% drop re-buy
                    if drop_pct >= REBUY_DROP_PERCENT and state["count"] < 3 and virtual_balance >= 2.0:
                        virtual_balance -= 2.0
                        new_coins = 2.0 / current_price
                        state["coins"] += new_coins
                        state["total_cost"] += 2.0
                        state["last_price"] = current_price
                        state["count"] += 1
                        log_trade(symbol, "SIM_BUY", new_coins, current_price, virtual_balance, f"Re-buy #{state['count']}")
                    
                    # Logic for 15% profit sell
                    elif profit_pct >= PROFIT_TARGET_PERCENT:
                        virtual_balance += (state["coins"] * current_price)
                        log_trade(symbol, "SIM_SELL", state["coins"], current_price, virtual_balance, "Target Hit")
                        trade_state[symbol] = {"status": "WAITING", "coins": 0.0, "total_cost": 0.0, "last_price": 0.0, "count": 0}

            if recent_activities:
                print(f"\n{Colors.HEADER}RECENT ACTIVITY:")
                for activity in recent_activities[:MAX_ACTIVITY_LOGS]:
                    print(f" {activity}")

            print(f"\n{Colors.SYSTEM}Refreshing in {check_interval} seconds...")
            time.sleep(check_interval)
            
    except KeyboardInterrupt:
        print(f"\n{Colors.SYSTEM}Shutting down... Laptop can now sleep.")
        allow_sleep()
    except Exception as error:
        print(f"{Colors.ERROR}❌ Error: {error}")
        allow_sleep()
        time.sleep(10)

if __name__ == "__main__":
    run_bot()