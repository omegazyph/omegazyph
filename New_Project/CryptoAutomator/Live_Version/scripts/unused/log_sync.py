#!/usr/bin/env python3
"""
Date: 2026-03-09
Script Name: log_sync.py
Author: omegazyph
Updated: 2026-03-09
Description: Synchronizes official exchange CSV data into the Sentinel Loop live trade log.
"""

import pandas as pd
import os
import platform

def synchronize_exchange_data():
    # Detect if we are on Windows (Laptop) or Linux (Server)
    if platform.system() == "Windows":
        exchange_file = "C:/Users/omega/Documents/omegazyph/New_Project/CryptoAutomator/Live_Version/OEX_ORDER.csv"
        live_log_file = "C:/Users/omega/Documents/omegazyph/New_Project/CryptoAutomator/Live_Version/logs/live_trade_log.csv"
    else:
        # Paths for your Wayne-Server
        exchange_file = "OEX_ORDER.csv"
        live_log_file = "/home/wayne1/Documents/CryptoAutomator/Live_Version/logs/live_trade_log.csv"

    if not os.path.exists(exchange_file):
        print(f"Error: {exchange_file} was not found.")
        return

    try:
        # Crypto.com CSVs usually have 3 lines of text before the header
        df_exchange = pd.read_csv(exchange_file, skiprows=3)
        
        # Only include FILLED trades
        df_filled = df_exchange[df_exchange['Status'] == 'FILLED'].copy()
        
        if df_filled.empty:
            print("No filled orders found in the exchange file.")
            return

        sync_data = []
        for index, row in df_filled.iterrows():
            clean_symbol = str(row['Pair']).replace('_', '/')
            
            sync_data.append({
                'Timestamp': row['Time (UTC)'],
                'Symbol': clean_symbol,
                'Action': f"LIVE_{row['Side']}",
                'Amount': row['Order Amount'],
                'Price': row['Average Price'],
                'Total': row['Total'],
                'Note': "Exchange Sync"
            })
            
        df_sync = pd.DataFrame(sync_data)
        
        # Ensure the logs folder exists
        log_dir = os.path.dirname(live_log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Append to your existing log file
        if os.path.exists(live_log_file):
            df_sync.to_csv(live_log_file, mode='a', header=False, index=False)
            print(f"Successfully synced {len(df_sync)} trades to your log.")
        else:
            df_sync.to_csv(live_log_file, index=False)
            print("Created a new live log file with synced data.")

    except Exception as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    synchronize_exchange_data()