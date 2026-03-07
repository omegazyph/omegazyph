# 2026-03-06 | main_bot_loop.py | Author: omegazyph | Updated: 2026-03-06
# Description: Wayne's 15% Drop Re-Buy Bot with persistent Dashboard.
# Fixed for Systemd/SSH color support and US-compatible exchange data.
#
# make sure you update the server if you have one

import ccxt
import time
import os
import json
import csv
from pathlib import Path
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Initialize Colors: strip=False is CRITICAL for systemd/SSH color support
init(autoreset=True, strip=False)
load_dotenv()

# --- CONSTANTS ---
STARTING_BALANCE = 20.00
REBUY_DROP_PERCENT = 15.0
PROFIT_TARGET_PERCENT = 15.0
MAX_ACTIVITY_LOGS = 5

class Colors:
    HEADER = Fore.CYAN + Style.BRIGHT
    MONEY = Fore.GREEN + Style.BRIGHT
    PRICE = Fore.YELLOW
    SIGNAL = Fore.MAGENTA + Style.BRIGHT
    SELL = Fore.RED + Style.BRIGHT
    SYSTEM = Fore.BLUE + Style.DIM
    ERROR = Fore.RED + Style.BRIGHT
    RESET = Style.RESET_ALL

# Global list to hold recent activities for the persistent display
recent_activities = []
virtual_balance = STARTING_BALANCE  # Initialize with starting default

def clear_screen():
    """Clears the terminal screen for a clean dashboard look."""
    # When running as a service, we don't always want to clear, 
    # but for SSH 'bot' shortcut, it helps.
    if os.name == "nt":
        os.system("cls")
    else:
        # Only clear if we are in an interactive terminal
        if os.environ.get('TERM'):
            os.system("clear")

def get_paths():
    """Returns the project root and file paths."""
    script_path = Path(__file__).resolve()
    # Assuming script is in /scripts/ folder, go up one level to root
    project_root = script_path.parent.parent
    config_path = project_root / "config.json"
    log_path = project_root / "trading_log.csv"
    return project_root, config_path, log_path

def load_config():
    """Loads configuration from the JSON file."""
    project_root, config_path, log_path = get_paths()
    with open(config_path, mode="r", encoding="utf-8") as file:
        return json.load(file)

def log_trade(symbol, side, amount, price, wallet, note):
    """Records trade to CSV and adds to the dashboard activity log."""
    global recent_activities
    project_root, config_path, log_path = get_paths()
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
    """Rebuilds the trade state and activity log from the CSV file on startup."""
    global virtual_balance, recent_activities
    project_root, config_path, log_path = get_paths()
    trades = {}
    virtual_balance = STARTING_BALANCE

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
            
            # Restore visual log
            last_entries = csv_data[-MAX_ACTIVITY_LOGS:]
            recent_activities = []
            for row in reversed(last_entries):
                side_color = Colors.MONEY if "BUY" in row["Side"] else Colors.SELL
                time_only = row["Timestamp"].split(" ")[1]
                log_entry = f"[{time_only}] {side_color}{row['Side']:<10}{Colors.RESET} {row['Symbol']} at ${float(row['Price']):,.4f}"
                recent_activities.append(log_entry)
                
    except Exception as error:
        print(f"{Colors.ERROR}Recovery Warning: {error}")
    
    return trades

def run_bot():
    """Main execution loop for the trading bot."""
    global virtual_balance
    # Using Kraken for better US compatibility as discussed
    exchange = ccxt.cryptocom({"enableRateLimit": True})
    trade_state = recover_state_from_csv()
    
    while True:
        try:
            config_data = load_config()
            trading_pairs = config_data["trading_pairs"]
            settings = config_data.get("global_settings", {"check_interval_seconds": 30})
            check_interval = settings["check_interval_seconds"]
            
            clear_screen()
            
            total_profit_loss = virtual_balance - STARTING_BALANCE
            profit_color = Colors.MONEY if total_profit_loss >= 0 else Colors.SELL
            current_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"{Colors.HEADER}======================================================================")
            print(f" {Colors.HEADER}WAYNE'S CRYPTO AUTOMATOR | {current_timestamp}")
            print(f" {Colors.HEADER}WALLET: {Colors.RESET}${virtual_balance:.2f} | {Colors.HEADER}TOTAL PROFIT: {profit_color}${total_profit_loss:.2f}")
            print(f"{Colors.HEADER}======================================================================")
            print(f"{'SYMBOL':<10} {'STATUS':<15} {'PRICE':<12} {'AVG/TARGET':<12} {'P/L %':<10} {'BUYS'}")
            print("-" * 70)

            for pair in trading_pairs:
                if not pair.get("enabled", True):
                    continue
                    
                symbol = pair["symbol"]
                if symbol not in trade_state:
                    trade_state[symbol] = {"status": "WAITING", "coins": 0.0, "total_cost": 0.0, "last_price": 0.0, "count": 0}
                
                state = trade_state[symbol]
                ticker = exchange.fetch_ticker(symbol)
                current_price = ticker["last"]

                # Logic: Waiting to Enter
                if state["status"] == "WAITING":
                    buy_target = pair["buy_threshold"]
                    status_label = f"{Colors.SYSTEM}SEARCHING"
                    print(f"{symbol:<10} {status_label:<24} ${current_price:<11,.2f} ${buy_target:<11,.2f} {'---':<10} {state['count']}/3")
                    
                    if current_price <= buy_target and virtual_balance >= 2.0:
                        buy_amount_usd = 2.0
                        virtual_balance -= buy_amount_usd
                        coins_purchased = buy_amount_usd / current_price
                        state.update({"status": "HOLDING", "coins": coins_purchased, "total_cost": buy_amount_usd, "last_price": current_price, "count": 1})
                        log_trade(symbol, "SIM_BUY", coins_purchased, current_price, virtual_balance, "Initial Entry")

                # Logic: Holding Position
                elif state["status"] == "HOLDING":
                    average_cost = state["total_cost"] / state["coins"]
                    current_profit_percent = ((current_price - average_cost) / average_cost) * 100
                    drop_since_last_buy = ((state["last_price"] - current_price) / state["last_price"]) * 100
                    
                    percent_color = Colors.MONEY if current_profit_percent >= 0 else Colors.SELL
                    status_label = f"{Colors.MONEY}HOLDING"
                    print(f"{symbol:<10} {status_label:<24} ${current_price:<11,.2f} ${average_cost:<11,.2f} {percent_color}{current_profit_percent:>+6.2f}%{Colors.RESET}   {state['count']}/3")

                    # 15% Drop Re-buy
                    if drop_since_last_buy >= REBUY_DROP_PERCENT and state["count"] < 3 and virtual_balance >= 2.0:
                        rebuy_amount_usd = 2.0
                        virtual_balance -= rebuy_amount_usd
                        new_coins = rebuy_amount_usd / current_price
                        state["coins"] += new_coins
                        state["total_cost"] += rebuy_amount_usd
                        state["last_price"] = current_price
                        state["count"] += 1
                        log_trade(symbol, "SIM_BUY", new_coins, current_price, virtual_balance, f"Re-buy #{state['count']}")

                    # 15% Profit Target Sell
                    elif current_profit_percent >= PROFIT_TARGET_PERCENT:
                        total_sell_value = state["coins"] * current_price
                        virtual_balance += total_sell_value
                        log_trade(symbol, "SIM_SELL", state["coins"], current_price, virtual_balance, "Target Hit")
                        trade_state[symbol] = {"status": "WAITING", "coins": 0.0, "total_cost": 0.0, "last_price": 0.0, "count": 0}

            if recent_activities:
                print(f"\n{Colors.HEADER}RECENT ACTIVITY:")
                for activity in recent_activities:
                    print(f" {activity}")

            print(f"\n{Colors.SYSTEM}Refreshing in {check_interval} seconds...")
            time.sleep(check_interval)
            
        except Exception as error:
            print(f"{Colors.ERROR}❌ Error: {error}")
            time.sleep(10)

if __name__ == "__main__":
    run_bot()