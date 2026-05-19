#!/usr/bin/env python3
"""
Script Name: mmm_trap_analyzer.py
Author: omegazyph
Date Created: May 17, 2026
Last Updated: May 17, 2026

Description:
    This program automatically calculates the Year-To-Date (YTD) low floor for 
    3M Company (MMM) using real-time market data. It takes the user's available
    settlement fund balance, verifies if a 2 or 3-share limit order trap can be
    placed, and outputs the exact execution parameters required for Vanguard.
"""

import sys
from datetime import datetime

# Verify that the yfinance library is installed for pulling real-time data
try:
    import yfinance as yf
except ImportError:
    print("[ERROR] The 'yfinance' library is missing.")
    print("[HELP] Please open your terminal and run: pip install yfinance")
    sys.exit(1)

def calculate_mmm_trap(available_cash):
    """
    Pulls YTD data for MMM, finds the lowest trading floor, and determines
    how many shares can be safely bought with the current cash reserve.
    """
    ticker_symbol = "MMM"
    current_year = datetime.now().year
    start_date = f"{current_year}-01-01"

    print(f"[*] Accessing market data for {ticker_symbol} since {start_date}...")
    
    # Fetch historical daily data for the current calendar year
    stock_data = yf.Ticker(ticker_symbol)
    historical_df = stock_data.history(start=start_date, interval="1d")

    if historical_df.empty:
        print(f"[ERROR] Could not retrieve historical data for {ticker_symbol}.")
        return

    # Calculate the exact historical low price for the current year
    ytd_low = historical_df["Low"].min()
    current_price = historical_df["Close"].iloc[-1]

    print("\n" + "="*50)
    print(f" MARKET METRICS FOR {ticker_symbol} (As of {datetime.now().strftime('%Y-%m-%d')})")
    print("="*50)
    print(f"Current Market Closing Price:   ${current_price:.2f}")
    print(f"Target Year-To-Date Low Floor:  ${ytd_low:.2f}")
    print(f"Your Available Settlement Cash: ${available_cash:.2f}")
    print("-"*50)

    # Evaluate trap parameters for the target 2 and 3-share milestones
    for target_shares in [2, 3]:
        required_capital = target_shares * ytd_low
        print(f"\n[Evaluating {target_shares}-Share Trap]")
        print(f" -> Total Estimated Cost:        ${required_capital:.2f}")

        if available_cash >= required_capital:
            remaining_cash = available_cash - required_capital
            print(" -> [STATUS] AVAILABLE")
            print(f" -> [VANGUARD BLUEPRINT] Buy {target_shares} shares of {ticker_symbol} with a Limit Price of ${ytd_low:.2f} set to a 60-Day Duration (GTC).")
            print(f" -> Remaining Cash Reserve:     ${remaining_cash:.2f}")
        else:
            shortfall = required_capital - available_cash
            print(" -> [STATUS] LOCKED (Insufficient Cash Pool)")
            print(f" -> [ACTION REQUIRED] Transfer an extra ${shortfall:.2f} from checking to arm this trap.")

    print("="*50)

if __name__ == "__main__":
    # Input your available cash balance directly here to analyze the current target allocation
    # Currently set to evaluate fresh scenarios beyond your initial $285.64 setup
    my_settlement_balance = 285.64
    
    calculate_mmm_trap(my_settlement_balance)