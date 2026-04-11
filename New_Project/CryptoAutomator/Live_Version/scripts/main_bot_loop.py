"""
Date: 2026-01-05
Script Name: main_bot_loop.py
Author: omegazyph
Updated: 2026-03-23
Description: 
    Wayne's LIVE Trading Bot for Crypto.com.
    Strategy: Buy at Lower Bollinger Band, Sell at Upper Bollinger Band.
    Fixed: CSV logging bypasses system buffering to prevent data loss.
    Safety Net: Added check to prevent selling below average entry price.
"""

import ccxt
import time
import os
import json
import csv
import pandas as pd
import ctypes
from pathlib import Path
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Initialize Colorama for the terminal display
init(autoreset=True, strip=False)

# --- WINDOWS POWER MANAGEMENT ---
EXECUTION_STATE_CONTINUOUS = 0x80000000
EXECUTION_STATE_SYSTEM_REQUIRED = 0x00000001
def prevent_system_sleep():
    # ctypes.windll.kernel32.SetThreadExecutionState(EXECUTION_STATE_SYSTEM_REQUIRED | EXECUTION_STATE_CONTINUOUS)
    pass

def allow_system_sleep():
    if os.name == 'nt':
        try:
            ctypes.windll.kernel32.SetThreadExecutionState(EXECUTION_STATE_CONTINUOUS)
        except Exception:
            pass

# --- DIRECTORY AND FILE PATHS ---
# Using .resolve() to ensure absolute paths regardless of where the script is launched
current_script_path = Path(__file__).resolve()
project_root_directory = current_script_path.parent.parent
environment_file_path = project_root_directory / ".env"
load_dotenv(dotenv_path=environment_file_path)

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
    """
    Logs every trade to the CSV file. 
    Uses flush and fsync to ensure data is written immediately to disk.
    """
    _, log_path = get_required_file_paths()
    time_full = time.strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.isfile(log_path)
    
    # Opening with buffering=0 is only allowed in binary mode, 
    # so we use manual flush and fsync instead for text mode.
    with open(log_path, mode="a", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        if not file_exists:
            writer.writerow(["Timestamp", "Symbol", "Side", "Amount", "Price", "Wallet", "Note"])
        
        writer.writerow([
            time_full, 
            symbol, 
            side, 
            f"{amount:.8f}", 
            f"{price:.8f}", 
            f"{remaining_balance:.2f}", 
            note
        ])
        
        # --- CRITICAL FIX: FORCE DATA TO DISK ---
        csv_file.flush()            # Push from Python buffer to OS buffer
        os.fsync(csv_file.fileno()) # Push from OS buffer to physical Disk

def get_recent_activity_from_csv():
    """Reads the last 5 trades from your log to show on the dashboard."""
    _, log_path = get_required_file_paths()
    recent_lines = []
    if not os.path.isfile(log_path):
        return recent_lines
    try:
        with open(log_path, mode="r", encoding="utf-8") as file:
            reader = list(csv.reader(file))
            if len(reader) <= 1:
                return recent_lines
            data_rows = reader[1:]
            for row in data_rows[-10:]:
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
    """Checks your CSV to see what coins you are currently holding."""
    _, log_path = get_required_file_paths()
    active_holdings = {}
    if not os.path.isfile(log_path):
        return active_holdings
    try:
        with open(log_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                symbol = row["Symbol"].strip()
                side = row["Side"].strip()
                price = float(row["Price"])
                amount = float(row["Amount"])

                if side == "LIVE_BUY":
                    if symbol not in active_holdings:
                        active_holdings[symbol] = {"status": "HOLDING", "coins": 0.0, "total_cost": 0.0}
                    
                    # Always force status to HOLDING when buy is found
                    active_holdings[symbol]["status"] = "HOLDING"
                    active_holdings[symbol]["coins"] += amount
                    active_holdings[symbol]["total_cost"] += (amount * price)

                elif side == "LIVE_SELL":
                    # Mark as WAITING and reset the bag
                    active_holdings[symbol] = {"status": "WAITING", "coins": 0.0, "total_cost": 0.0}
    except Exception:
        pass
    return active_holdings

def calculate_bollinger_bands(exchange, symbol, timeframe='1h', window=20):
    """
    Fetches OHLCV data and calculates the Upper and Lower bands.
    Adjust the 'timeframe' parameter to change trading frequency.
    Common options: '1m', '5m', '15m', '1h', '4h', '1d'
    """
    try:
        # Fetch candles from the exchange
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe)

        # Create the DataFrame
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        
        # Calculate moving average and standard deviation
        df['sma'] = df['close'].rolling(window=window).mean()
        df['std'] = df['close'].rolling(window=window).std()

        # Calculate Upper and Lower Bands
        df['upper'] = df['sma'] + (df['std'] * 2)
        df['lower'] = df['sma'] - (df['std'] * 2)

        # Pull the latest row
        latest = df.iloc[-1]

        return latest['lower'], latest['upper'], latest['close']
    
    except Exception:
        # Simple error catch to keep the loop running
        return None, None, None

def run_trading_engine():
    """Main loop for the Sentinel bot."""
    prevent_system_sleep()
    exchange_client = ccxt.cryptocom({
        "apiKey": os.getenv("CRYPTO_COM_KEY"),
        "secret": os.getenv("CRYPTO_COM_SECRET"),
        "enableRateLimit": True
    })
    
    while True:
        try:
            current_portfolio = restore_portfolio_from_log()
            settings = load_trading_configuration()
            trading_pairs_list = settings["trading_pairs"]
            global_settings = settings.get("global_settings", {})
            trade_dollar_amount = global_settings.get("trade_dollar_amount", 2.0)
            check_interval_seconds = global_settings.get("check_interval_seconds", 30)
            
            balance_response = exchange_client.fetch_balance()

            # Get the standard USD and thr Instant Deposit Credit
            settled_usd = balance_response.get('total', {}).get("USD", 0.0)
            instant_credit = balance_response.get('total', {}).get("USD-CREDIT", 0.0)

            # Add them together to see the buying power
            available_usd_cash = float(settled_usd + instant_credit)
            
            total_unrealized_profit_loss = 0.0
            dashboard_data_rows = []
            insufficient_funds_warning_active = False

            for pair_info in trading_pairs_list:
                if not pair_info.get("enabled", True):
                    continue
                
                symbol = pair_info["symbol"]
                base_asset = symbol.split('/')[0]
                active_symbol = f"{base_asset}/USD"
                
                lower_band, upper_band, current_price = calculate_bollinger_bands(exchange_client, active_symbol)
                
                if lower_band is None:
                    continue

                if active_symbol not in current_portfolio:
                    current_portfolio[active_symbol] = {"status": "WAITING", "coins": 0.0, "total_cost": 0.0}
                
                state = current_portfolio[active_symbol]

                if state["status"] == "WAITING":
                    dashboard_data_rows.append(
                        f"{active_symbol:<10} "
                        f"{InterfaceColors.INFO_BLUE}{'SEARCHING':<15}{InterfaceColors.RESET_STYLE} "
                        f"${current_price:<11,.4f} "
                        f"BUY AT: ${lower_band:<10,.4f}"
                    )
                    
                    if current_price <= lower_band:
                        if available_usd_cash >= trade_dollar_amount:
                            try:
                                qty = trade_dollar_amount / current_price
                                order = exchange_client.create_market_buy_order(active_symbol, qty)
                                # Fetch actual price from order response if available
                                exec_price = order.get('price') if order.get('price') else current_price
                                exec_qty = order.get('amount') if order.get('amount') else qty
                                
                                record_successful_trade(
                                    active_symbol, 
                                    "LIVE_BUY", 
                                    exec_qty, 
                                    exec_price, 
                                    available_usd_cash - trade_dollar_amount, 
                                    "Lower Band Hit"
                                )
                            except Exception:
                                pass
                        else:
                            insufficient_funds_warning_active = True

                elif state["status"] == "HOLDING":
                    average_entry = state["total_cost"] / state["coins"]
                    current_value = state["coins"] * current_price
                    pnl_dollars = current_value - state["total_cost"]
                    total_unrealized_profit_loss += pnl_dollars
                    pnl_pct = (pnl_dollars / state["total_cost"]) * 100
                    
                    color = InterfaceColors.SUCCESS_GREEN if pnl_pct >= 0 else InterfaceColors.DANGER_RED
                    dashboard_data_rows.append(
                        f"{active_symbol:<10} "
                        f"{InterfaceColors.SUCCESS_GREEN}{'HOLDING':<15}{InterfaceColors.RESET_STYLE} "
                        f"AVG: ${average_entry:<10,.4f} "
                        f"SELL AT: ${upper_band:<10,.4f} "
                        f"{color}{pnl_pct:>+6.2f}%"
                    )

                    # --- SAFETY NET: ONLY SELL IF PRICE IS ABOVE ENTRY COST ---
                    if current_price >= upper_band and current_price >= (average_entry * 1.0005):
                        try:
                            wallet_bal = exchange_client.fetch_balance().get('free', {}).get(base_asset, 0.0)
                            sell_qty = min(state["coins"], wallet_bal)
                            order = exchange_client.create_market_sell_order(active_symbol, sell_qty)
                            
                            exec_price = order.get('price') if order.get('price') else current_price
                            
                            record_successful_trade(
                                active_symbol, 
                                "LIVE_SELL", 
                                sell_qty, 
                                exec_price, 
                                available_usd_cash + current_value, 
                                "Upper Band Hit (0.05% Profit)"
                            )
                        except Exception:
                            pass

            clear_terminal_screen()
            pnl_color = InterfaceColors.SUCCESS_GREEN if total_unrealized_profit_loss >= 0 else InterfaceColors.DANGER_RED
            print(f"{InterfaceColors.HEADER_CYAN}===========================================================================")
            print(f" {InterfaceColors.HEADER_CYAN}WAYNE'S SENTINEL LOOP | {time.strftime('%H:%M:%S')}")
            print(f" {InterfaceColors.HEADER_CYAN}CASH: {InterfaceColors.RESET_STYLE}${available_usd_cash:.2f} | "
                  f"{InterfaceColors.HEADER_CYAN}UNREALIZED P/L: {pnl_color}${total_unrealized_profit_loss:+.2f}{InterfaceColors.RESET_STYLE}")
            print(f"{InterfaceColors.HEADER_CYAN}===========================================================================")
            print(f"{'SYMBOL':<10} {'STATUS':<15} {'DETAILS':<32} {'P/L %'}")
            print("-" * 75)
            for row in dashboard_data_rows:
                print(row)
            
            if insufficient_funds_warning_active:
                print(f"\n{InterfaceColors.WARNING_YELLOW}* ALERT: USD balance insufficient for trade.")

            recent = get_recent_activity_from_csv()
            if recent:
                print(f"\n{InterfaceColors.HEADER_CYAN}RECENT TRADES (FROM LOG FILE):")
                for line in recent:
                    print(f" {line}")

            time.sleep(check_interval_seconds)

        except KeyboardInterrupt:
            allow_system_sleep()
            break
        except Exception:
            time.sleep(10)

if __name__ == "__main__":
    run_trading_engine()