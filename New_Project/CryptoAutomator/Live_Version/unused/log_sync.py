#!/usr/bin/env python3
"""
Date: 2026-03-09
Script Name: log_sync.py
Author: omegazyph
Updated: 2026-03-09
Description: Synchronizes official exchange CSV data (OEX_ORDER.csv) 
             into the Sentinel Loop live trade log for dashboard accuracy.
"""

import pandas as pd
import os
import platform

def synchronize_exchange_data():
    # Detect the operating system to set the correct file paths
    # This ensures it works on your Legion laptop (Windows) and your server (Linux)
    if platform.system() == "Windows":
        # Adjust these paths to match your folder structure in VSCode
        exchange_file = "C:/Users/omega/Documents/omegazyph/New_Project/OEX_ORDER.csv"
        live_log_file = "C:/Users/omega/Documents/omegazyph/New_Project/logs/live_trade_log.csv"
    else:
        # Standard Linux/WSL paths
        exchange_file = "OEX_ORDER.csv"
        live_log_file = "/home/wayne1/Documents/CryptoAutomator/Live_Version/logs/live_trade_log.csv"

    print(f"Searching for exchange data at: {exchange_file}")

    # Check if the exchange file exists before trying to read it
    if not os.path.exists(exchange_file):
        print(f"Error: {exchange_file} was not found. Please export your CSV first.")
        return

    try:
        # Most exchange CSVs have a header on the 4th row (skip first 3 lines)
        df_exchange = pd.read_csv(exchange_file, skiprows=3)
        
        # Filter for only 'FILLED' orders so we don't log cancelled trades
        df_filled = df_exchange[df_exchange['Status'] == 'FILLED'].copy()
        
        if df_filled.empty:
            print("No new filled orders were found in the exchange file.")
            return

        # Prepare the data to match your Sentinel Loop dashboard format
        sync_list = []
        for index, row in df_filled.iterrows():
            # Convert 'XRP_USD' format to 'XRP/USD'
            clean_symbol = str(row['Pair']).replace('_', '/')
            
            sync_list.append({
                'Timestamp': row['Time (UTC)'],
                'Symbol': clean_symbol,
                'Action': f"LIVE_{row['Side'].upper()}",
                'Amount': row['Order Amount'],
                'Price': row['Average Price'],
                'Total': row['Total'],
                'Note': "Official Exchange Sync"
            })
            
        df_sync = pd.DataFrame(sync_list)
        
        # Ensure the logs directory exists
        log_directory = os.path.dirname(live_log_file)
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        # Append the new data to your existing live_trade_log.csv
        if os.path.exists(live_log_file):
            df_sync.to_csv(live_log_file, mode='a', header=False, index=False)
            print(f"Successfully synced {len(df_sync)} trades to your dashboard.")
        else:
            # Create a new file if one doesn't exist
            df_sync.to_csv(live_log_file, index=False)
            print("Created a new live log file with the synced data.")

    except Exception as error:
        print(f"An error occurred during synchronization: {error}")

if __name__ == "__main__":
    synchronize_exchange_data()