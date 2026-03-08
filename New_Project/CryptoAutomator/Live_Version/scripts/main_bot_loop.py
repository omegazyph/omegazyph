"""
Date: 2026-01-05
Script Name: main_bot_loop.py
Author: omegazyph
Updated: 2026-03-08
Description: 
    Wayne's LIVE Trading Bot for Crypto.com Exchange.
    Restored Unrealized P/L calculation and Recent Trades display.
    Maintains auto-refreshing portfolio and config logic.
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

# Initialize Colorama for the terminal display on the Lenovo Legion laptop
init(autoreset=True, strip=False)

# --- WINDOWS POWER MANAGEMENT ---
EXECUTION_STATE_CONTINUOUS = 0x80000000
EXECUTION_STATE_SYSTEM_REQUIRED = 0x00000001

def prevent_system_sleep():
    if os.name == 'nt':
        ctypes.windll.kernel32.SetThreadExecutionState(EXECUTION_STATE_CONTINUOUS | EXECUTION_STATE_SYSTEM_REQUIRED)

def allow_system_sleep():
    if os.name == 'nt':
        ctypes.windll.kernel32.SetThreadExecutionState(EXECUTION_STATE_CONTINUOUS)

# --- DIRECTORY AND FILE PATHS ---
current_script_path = Path(__file__).resolve()
project_root_directory = current_script_path.parent.parent
environment_file_path = project_root_directory / ".env"
load_dotenv(dotenv_path=environment_file_path)

# Trading Strategy Constant
PROFIT_TARGET_PERCENTAGE = 15.0

class InterfaceColors:
    HEADER_CYAN = Fore.CYAN + Style.BRIGHT
    SUCCESS_GREEN = Fore.GREEN + Style.BRIGHT
    WARNING_YELLOW = Fore.YELLOW
    DANGER_RED = Fore.RED + Style.BRIGHT
    INFO_BLUE = Fore.BLUE + Style.BRIGHT
    RESET_STYLE = Style.RESET_ALL

def clear_terminal_screen():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")

def get_required_file_paths():
    configuration_file_path = project_root_directory / "config.json"
    trading_activity_log_path = project_root_directory / "live_trade_log.csv"
    return configuration_file_path, trading_activity_log_path

def load_trading_configuration():
    configuration_path, _ = get_required_file_paths()
    with open(configuration_path, mode="r", encoding="utf-8") as file:
        return json.load(file)

def record_successful_trade(symbol, side, amount, price, remaining_balance, note):
    _, log_path = get_required_file_paths()
    time_full = time.strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.isfile(log_path)
    with open(log_path, mode="a", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        if not file_exists:
            writer.writerow(["Timestamp", "Symbol", "Side", "Amount", "Price", "Wallet", "Note"])
        writer.writerow([time_full, symbol, side, f"{amount:.8f}", f"{price:.8f}", f"{remaining_balance:.2f}", note])

def get_recent_activity_from_csv():
    _, log_path = get_required_file_paths()
    recent_lines = []
    if not os.path.isfile(log_path):
        return recent_lines
    try:
        with open(log_path, mode="r", encoding="utf-8") as file:
            reader = list(csv.reader(file))
            data_rows = reader[1:]
            for row in data_rows[-5:]:
                timestamp = row[0].split(" ")[1]
                side = row[2]
                symbol = row[1]
                note = row[6]
                color = InterfaceColors.SUCCESS_GREEN if "BUY" in side else InterfaceColors.DANGER_RED
                recent_lines.insert(0, f"[{timestamp}] {color}{side:<10}{InterfaceColors.RESET_STYLE} {symbol} {note}")
    except Exception:
        pass
    return recent_lines

def restore_portfolio_from_log():
    _, log_path = get_required_file_paths()
    active_holdings = {}
    if not os.path.isfile(log_path):
        return active_holdings
    try:
        with open(log_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                symbol = row["Symbol"]
                side = row["Side"]
                price = float(row["Price"])
                amount = float(row["Amount"])
                if side == "LIVE_BUY":
                    if symbol not in active_holdings:
                        active_holdings[symbol] = {"status": "HOLDING", "coins": 0.0, "total_cost": 0.0}
                    active_holdings[symbol]["coins"] += amount
                    active_holdings[symbol]["total_cost"] += (amount * price)
                elif side == "LIVE_SELL":
                    active_holdings[symbol] = {"status": "WAITING", "coins": 0.0, "total_cost": 0.0}
    except Exception:
        pass
    return active_holdings

def run_trading_engine():
    prevent_system_sleep()
    exchange_client = ccxt.cryptocom({
        "apiKey": os.getenv("CRYPTO_COM_KEY"),
        "secret": os.getenv("CRYPTO_COM_SECRET"),
        "enableRateLimit": True
    })
    
    while True:
        try:
            # REFRESH FROM FILES
            current_portfolio = restore_portfolio_from_log()
            settings = load_trading_configuration()
            trading_pairs_list = settings["trading_pairs"]
            global_settings = settings.get("global_settings", {})
            trade_dollar_amount = global_settings.get("trade_dollar_amount", 2.0)
            check_interval_seconds = global_settings.get("check_interval_seconds", 30)
            
            balance_response = exchange_client.fetch_balance()
            free_balances_dictionary = balance_response.get('free', {})
            available_usd_cash = float(free_balances_dictionary.get("USD", 0.0))
            
            total_unrealized_profit_loss = 0.0
            dashboard_data_rows = []
            insufficient_funds_warning_active = False

            for pair_information in trading_pairs_list:
                if not pair_information.get("enabled", True):
                    continue
                
                base_asset_name = pair_information["symbol"].split('/')[0]
                active_trading_symbol = f"{base_asset_name}/USD"
                
                if active_trading_symbol not in current_portfolio:
                    current_portfolio[active_trading_symbol] = {"status": "WAITING", "coins": 0.0, "total_cost": 0.0}
                
                current_state = current_portfolio[active_trading_symbol]
                market_ticker_data = exchange_client.fetch_ticker(active_trading_symbol)
                current_market_price = market_ticker_data["last"]

                if current_state["status"] == "WAITING":
                    buy_threshold_price = pair_information["buy_threshold"]
                    dashboard_data_rows.append(f"{active_trading_symbol:<10} {InterfaceColors.INFO_BLUE}{'SEARCHING':<15}{InterfaceColors.RESET_STYLE} ${current_market_price:<11,.4f} ${buy_threshold_price:<11,.4f}")
                    
                    if current_market_price <= buy_threshold_price:
                        if available_usd_cash >= trade_dollar_amount:
                            try:
                                coin_quantity = trade_dollar_amount / current_market_price
                                buy_order = exchange_client.create_market_buy_order(active_trading_symbol, coin_quantity)
                                record_successful_trade(active_trading_symbol, "LIVE_BUY", buy_order['amount'], buy_order['price'], available_usd_cash - trade_dollar_amount, "Target Price Hit")
                            except Exception:
                                pass
                        else:
                            insufficient_funds_warning_active = True

                elif current_state["status"] == "HOLDING":
                    average_entry_price = current_state["total_cost"] / current_state["coins"]
                    current_market_value = current_state["coins"] * current_market_price
                    profit_loss_dollars = current_market_value - current_state["total_cost"]
                    
                    # RESTORED: Add to the Unrealized P/L total
                    total_unrealized_profit_loss += profit_loss_dollars
                    
                    profit_loss_percentage = (profit_loss_dollars / current_state["total_cost"]) * 100
                    percentage_color = InterfaceColors.SUCCESS_GREEN if profit_loss_percentage >= 0 else InterfaceColors.DANGER_RED
                    dashboard_data_rows.append(f"{active_trading_symbol:<10} {InterfaceColors.SUCCESS_GREEN}{'HOLDING':<15}{InterfaceColors.RESET_STYLE} ${current_market_price:<11,.4f} ${average_entry_price:<11,.4f} {percentage_color}{profit_loss_percentage:>+6.2f}%")

                    if profit_loss_percentage >= PROFIT_TARGET_PERCENTAGE:
                        try:
                            actual_wallet_balance = exchange_client.fetch_balance().get('free', {}).get(base_asset_name, 0.0)
                            sell_quantity = min(current_state["coins"], actual_wallet_balance)
                            sell_order = exchange_client.create_market_sell_order(active_trading_symbol, sell_quantity)
                            record_successful_trade(active_trading_symbol, "LIVE_SELL", sell_quantity, sell_order['price'], available_usd_cash + current_market_value, "Profit Target Reached")
                        except Exception:
                            pass

            clear_terminal_screen()
            unrealized_pnl_color = InterfaceColors.SUCCESS_GREEN if total_unrealized_profit_loss >= 0 else InterfaceColors.DANGER_RED
            
            # RESTORED: Header with Unrealized P/L
            print(f"{InterfaceColors.HEADER_CYAN}===========================================================================")
            print(f" {InterfaceColors.HEADER_CYAN}WAYNE'S LIVE COMMAND | {time.strftime('%H:%M:%S')}")
            print(f" {InterfaceColors.HEADER_CYAN}CASH: {InterfaceColors.RESET_STYLE}${available_usd_cash:.2f} | "
                  f"{InterfaceColors.HEADER_CYAN}UNREALIZED P/L: {unrealized_pnl_color}${total_unrealized_profit_loss:+.2f}{InterfaceColors.RESET_STYLE}")
            print(f"{InterfaceColors.HEADER_CYAN}===========================================================================")
            print(f"{'SYMBOL':<10} {'STATUS':<15} {'PRICE':<12} {'TARGET/AVG':<12} {'P/L %'}")
            print("-" * 65)
            for data_row in dashboard_data_rows:
                print(data_row)
            
            if insufficient_funds_warning_active:
                print(f"\n{InterfaceColors.WARNING_YELLOW}* ALERT: Market is at buy target, but USD balance is insufficient.")

            # RESTORED: Recent trades footer
            recent_activity = get_recent_activity_from_csv()
            if recent_activity:
                print(f"\n{InterfaceColors.HEADER_CYAN}RECENT TRADES (FROM LOG FILE):")
                for activity_line in recent_activity:
                    print(f" {activity_line}")

            time.sleep(check_interval_seconds)

        except KeyboardInterrupt:
            allow_system_sleep()
            break
        except Exception:
            time.sleep(10)

if __name__ == "__main__":
    run_trading_engine()