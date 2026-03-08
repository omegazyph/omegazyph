"""
Date: 2026-03-07
Script Name: main_bot_loop.py
Author: omegazyph
Updated: 2026-03-07
Description: 
    Wayne's LIVE Trading Bot for Crypto.com Exchange.
    This script executes REAL market orders using the USD Bundle.
    Strictly uses full-word variables and non-shorthand logic.
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

# Initialize Colorama for the VSCode terminal
init(autoreset=True, strip=False)

# --- WINDOWS STAY-AWAKE ---
# Prevents the Lenovo Legion from sleeping during live trading
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001

def prevent_sleep():
    """ Prevents the Windows system from entering sleep mode """
    if os.name == 'nt':
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)

def allow_sleep():
    """ Restores default Windows power settings """
    if os.name == 'nt':
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)

# --- PATHS & CONFIG ---
script_path = Path(__file__).resolve()
project_root = script_path.parent.parent
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)

# Trading logic constants
REBUY_DROP_PERCENT = 15.0
PROFIT_TARGET_PERCENT = 15.0
MAX_ACTIVITY_LOGS = 5
TRADE_AMOUNT_USD = 2.0

class Colors:
    """ ANSI Color codes for the terminal dashboard """
    HEADER = Fore.CYAN + Style.BRIGHT
    MONEY = Fore.GREEN + Style.BRIGHT
    PRICE = Fore.YELLOW
    SELL = Fore.RED + Style.BRIGHT
    SYSTEM = Fore.BLUE + Style.BRIGHT
    RESET = Style.RESET_ALL

# List to store the most recent trade events
recent_activities = []

def clear_screen():
    """ Clears the terminal screen for a fresh dashboard update """
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")

def get_paths():
    """ Defines the file paths for configuration and logging """
    config_path = project_root / "config.json"
    log_path = project_root / "live_trade_log.csv"
    return project_root, config_path, log_path

def load_config():
    """ Loads the trading pair settings from the JSON file """
    paths = get_paths()
    config_path = paths[1]
    with open(config_path, mode="r", encoding="utf-8") as file:
        config_data = json.load(file)
        return config_data

def log_trade(symbol, side, amount, price, wallet, note):
    """ Records actual live trade execution data to a CSV file """
    global recent_activities
    paths = get_paths()
    log_path = paths[2]
    current_time_short = time.strftime("%H:%M:%S")
    current_time_full = time.strftime("%Y-%m-%d %H:%M:%S")
    
    file_exists = os.path.isfile(log_path)
    with open(log_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if file_exists is False:
            writer.writerow(["Timestamp", "Symbol", "Side", "Amount", "Price", "Wallet", "Note"])
        
        writer.writerow([current_time_full, symbol, side, f"{amount:.8f}", f"{price:.8f}", f"{wallet:.2f}", note])
    
    # Determine the color based on the trade side
    if "SELL" in side:
        side_color = Colors.SELL
    else:
        side_color = Colors.MONEY
        
    activity_entry = f"[{current_time_short}] {side_color}{side:<10}{Colors.RESET} {symbol} at ${price:,.4f}"
    recent_activities.insert(0, activity_entry)
    
    # Keep the activity list from growing too large
    activity_count = len(recent_activities)
    if activity_count > MAX_ACTIVITY_LOGS:
        recent_activities.pop()

def recover_state_from_csv():
    """ Reads the log file to restore active holdings upon restart """
    paths = get_paths()
    log_path = paths[2]
    trades = {}

    if os.path.isfile(log_path) is False:
        return trades

    try:
        with open(log_path, mode="r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                symbol = row["Symbol"]
                side = row["Side"]
                price = float(row["Price"])
                amount = float(row["Amount"])

                if side == "LIVE_BUY":
                    if symbol not in trades:
                        trades[symbol] = {
                            "status": "HOLDING", 
                            "coins": 0.0, 
                            "total_cost": 0.0, 
                            "last_price": 0.0, 
                            "count": 0
                        }
                    # Non-shorthand math operations
                    trades[symbol]["coins"] = trades[symbol]["coins"] + amount
                    trades[symbol]["total_cost"] = trades[symbol]["total_cost"] + (amount * price)
                    trades[symbol]["last_price"] = price
                    trades[symbol]["count"] = trades[symbol]["count"] + 1
                elif side == "LIVE_SELL":
                    trades[symbol] = {
                        "status": "WAITING", 
                        "coins": 0.0, 
                        "total_cost": 0.0, 
                        "last_price": 0.0, 
                        "count": 0
                    }
    except Exception as error:
        print(f"Recovery Error: {error}")
        
    return trades

def run_bot():
    """ Main execution loop for real money trading on the laptop """
    prevent_sleep()
    
    # Initialize the exchange with your API keys
    exchange = ccxt.cryptocom({
        "apiKey": os.getenv("CRYPTO_COM_KEY"),
        "secret": os.getenv("CRYPTO_COM_SECRET"),
        "enableRateLimit": True
    })
    
    # Restore the current trade state from the log file
    trade_state = recover_state_from_csv()
    
    while True:
        try:
            config_data = load_config()
            trading_pairs = config_data["trading_pairs"]
            
            # Extract settings safely
            global_settings = config_data.get("global_settings", {})
            check_interval = global_settings.get("check_interval_seconds", 30)
            
            # Fetch the actual real-time balance from the exchange
            balance_info = exchange.fetch_balance()
            total_balance_data = balance_info.get('total', {})
            real_usd_balance = total_balance_data.get("USD", 0.0)
            
            total_unrealized_profit = 0.0
            table_rows = []

            for pair in trading_pairs:
                enabled_status = pair.get("enabled", True)
                if enabled_status is False:
                    continue
                
                # Convert USDT symbols to USD for the exchange bundle
                raw_symbol = pair["symbol"]
                symbol = raw_symbol.replace("USDT", "USD")
                
                if symbol not in trade_state:
                    trade_state[symbol] = {
                        "status": "WAITING", 
                        "coins": 0.0, 
                        "total_cost": 0.0, 
                        "last_price": 0.0, 
                        "count": 0
                    }
                
                state = trade_state[symbol]
                ticker_data = exchange.fetch_ticker(symbol)
                current_price = ticker_data["last"]

                # --- LIVE BUY LOGIC (SEARCHING) ---
                if state["status"] == "WAITING":
                    buy_target = pair["buy_threshold"]
                    search_row = f"{symbol:<10} {Colors.SYSTEM}{'SEARCHING':<15} ${current_price:<11,.4f} ${buy_target:<11,.4f} {'---':<10} {state['count']}/3"
                    table_rows.append(search_row)
                    
                    if current_price <= buy_target:
                        if real_usd_balance >= TRADE_AMOUNT_USD:
                            # EXECUTE REAL MARKET BUY ORDER
                            order_data = exchange.create_market_buy_order(symbol, TRADE_AMOUNT_USD)
                            filled_price = order_data['price']
                            coins_received = order_data['amount']
                            
                            state["status"] = "HOLDING"
                            state["coins"] = coins_received
                            state["total_cost"] = TRADE_AMOUNT_USD
                            state["last_price"] = filled_price
                            state["count"] = 1
                            
                            remaining_wallet = real_usd_balance - TRADE_AMOUNT_USD
                            log_trade(symbol, "LIVE_BUY", coins_received, filled_price, remaining_wallet, "Real Entry")

                # --- LIVE SELL/REBUY LOGIC (HOLDING) ---
                elif state["status"] == "HOLDING":
                    average_cost = state["total_cost"] / state["coins"]
                    current_position_value = state["coins"] * current_price
                    dollar_difference = current_position_value - state["total_cost"]
                    
                    # Track total account profit for the header
                    total_unrealized_profit = total_unrealized_profit + dollar_difference
                    
                    profit_percentage = (dollar_difference / state["total_cost"]) * 100
                    
                    if profit_percentage >= 0:
                        percent_color = Colors.MONEY
                    else:
                        percent_color = Colors.SELL
                    
                    holding_row = f"{symbol:<10} {Colors.MONEY}{'HOLDING':<15} ${current_price:<11,.4f} ${average_cost:<11,.4f} {percent_color}{profit_percentage:>+6.2f}%{Colors.RESET}   {state['count']}/3"
                    table_rows.append(holding_row)

                    # Logic for 15% drop re-buy
                    last_entry_price = state["last_price"]
                    price_drop_pct = ((last_entry_price - current_price) / last_entry_price) * 100
                    
                    if price_drop_pct >= REBUY_DROP_PERCENT:
                        if state["count"] < 3:
                            if real_usd_balance >= TRADE_AMOUNT_USD:
                                # EXECUTE REAL RE-BUY
                                re_order = exchange.create_market_buy_order(symbol, TRADE_AMOUNT_USD)
                                state["coins"] = state["coins"] + re_order['amount']
                                state["total_cost"] = state["total_cost"] + TRADE_AMOUNT_USD
                                state["last_price"] = re_order['price']
                                state["count"] = state["count"] + 1
                                
                                current_wallet = real_usd_balance - TRADE_AMOUNT_USD
                                log_trade(symbol, "LIVE_BUY", re_order['amount'], re_order['price'], current_wallet, f"Re-buy #{state['count']}")

                    # Logic for 15% profit sell
                    elif profit_percentage >= PROFIT_TARGET_PERCENT:
                        # EXECUTE REAL MARKET SELL ORDER
                        sell_order = exchange.create_market_sell_order(symbol, state["coins"])
                        sell_price = sell_order['price']
                        
                        final_wallet_est = real_usd_balance + current_position_value
                        log_trade(symbol, "LIVE_SELL", state["coins"], sell_price, final_wallet_est, "Profit Taken")
                        
                        # Reset the symbol state back to searching
                        trade_state[symbol] = {
                            "status": "WAITING", 
                            "coins": 0.0, 
                            "total_cost": 0.0, 
                            "last_price": 0.0, 
                            "count": 0
                        }

            # --- RENDER DASHBOARD ---
            clear_screen()
            
            # Set color for the total profit in the header
            if total_unrealized_profit >= 0:
                header_p_color = Colors.MONEY
            else:
                header_p_color = Colors.SELL
            
            current_timestamp = time.strftime('%H:%M:%S')
            
            print(f"{Colors.HEADER}======================================================================")
            print(f" {Colors.HEADER}WAYNE'S LIVE COMMAND | {current_timestamp}")
            print(f" {Colors.HEADER}CASH: {Colors.RESET}${real_usd_balance:.2f} | "
                  f"{Colors.HEADER}UNREALIZED P/L: {header_p_color}${total_unrealized_profit:+.2f}{Colors.RESET}")
            
            print(f"{Colors.HEADER}======================================================================")
            print(f"{'SYMBOL':<10} {'STATUS':<15} {'PRICE':<12} {'TARGET/AVG':<12} {'P/L %':<10} {'BUYS'}")
            print("-" * 75)
            
            # Print each data row for the table
            for data_row in table_rows:
                print(data_row)
                
            # Display the log of recent events at the bottom
            if recent_activities:
                print(f"\n{Colors.HEADER}RECENT ACTIVITY:")
                for activity_text in recent_activities:
                    print(f" {activity_text}")
            
            # Refresh interval
            time.sleep(check_interval)
            
        except KeyboardInterrupt:
            # Re-enable laptop sleep settings on exit
            allow_sleep()
            break
        except Exception as runtime_error:
            print(f"{Colors.SELL}Live Trading Error: {runtime_error}")
            time.sleep(10)

if __name__ == "__main__":
    run_bot()