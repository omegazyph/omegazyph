"""
Date: 2026-05-17
Script Name: portfolio_analyzer.py
Author: omegazyph
Updated: 2026-05-17

Description:
This program automates the tracking of Vanguard financial assets. It dynamically 
scans a designated Windows directory for downloaded CSV files, isolates the active 
investment holdings table blocks to calculate asset allocations, parses historical 
transaction records to isolate and aggregate received dividend distributions, and 
exports a comprehensive multi-layer text report summary file to the local directory.
"""

import os
import glob
import pandas as pd

def clean_currency_value(value_string):
    """
    Cleans string-formatted currency values from the CSV file.
    Removes dollar signs, commas, and whitespace, converting them to floats.
    Handles negative numbers enclosed in dashes or parentheses safely.
    """
    if pd.isna(value_string):
        return 0.0
    
    processed_string = str(value_string).strip()
    processed_string = processed_string.replace("$", "").replace(",", "")
    
    # Handle explicit negative accounting representations if present
    if processed_string.startswith("(") and processed_string.endswith(")"):
        processed_string = "-" + processed_string[1:-1]
        
    try:
        return float(processed_string)
    except ValueError:
        return 0.0

def find_target_csv_file(data_directory):
    """
    Scans the targeted directory and returns the path of the CSV file.
    This accommodates files named with custom download date prefixes.
    If multiple CSV files exist, it returns the most recently modified one.
    """
    search_pattern = os.path.join(data_directory, "*.csv")
    csv_file_matches = glob.glob(search_pattern)
    
    if not csv_file_matches:
        return None
        
    # Sort files to pull the most recently modified CSV file if multiple exist
    csv_file_matches.sort(key=os.path.getmtime, reverse=True)
    return csv_file_matches[0]

def get_asset_class(ticker_symbol):
    """
    Categorizes individual ticker symbols into broad macro asset classes
    to allow for simplified high-level portfolio balance reviews.
    """
    us_equity_tickers = [
        "VFIAX", "VSMAX", "SPY", "MMM", "VOO", "MCO", "QQQ", "WFC", 
        "ABBV", "MA", "ABT", "NOBL", "V", "AXP", "AON", "AAPL", 
        "KO", "JNJ", "CVX", "USB", "SOLV", "BK", "PG", "VONG", 
        "BMY", "MRK", "BAC", "KR", "VZ", "SIRI", "KHC"
    ]
    
    international_equity_tickers = ["VEMAX", "VYMI"]
    bond_tickers = ["VBTLX"]
    cash_tickers = ["VMFXX"]
    blended_tickers = ["VTIVX"]
    cryptocurrency_tickers = ["ETHB"]
    
    if ticker_symbol in us_equity_tickers:
        return "US Equities (Stocks)"
    elif ticker_symbol in international_equity_tickers:
        return "International Equities"
    elif ticker_symbol in bond_tickers:
        return "Fixed Income (Bonds)"
    elif ticker_symbol in cash_tickers:
        return "Cash & Money Market"
    elif ticker_symbol in blended_tickers:
        return "Blended Allocation (Target Date)"
    elif ticker_symbol in cryptocurrency_tickers:
        return "Cryptocurrency / Alternative"
    else:
        return "Uncategorized Assets"

def analyze_vanguard_portfolio():
    """
    Main execution logic to find, parse, analyze, and report Vanguard portfolio data,
    including active holdings configurations and cumulative historical dividends.
    """
    # Explicit definition of the data file path matching your Windows local repository structure
    base_project_directory = "C:/Users/omega/Documents/omegazyph/Vanguard_Tracker"
    data_directory = f"{base_project_directory}/data"
    
    # Validate that the targeted directory exists
    if not os.path.exists(data_directory):
        print(f"Error: The directory structure was not found at {data_directory}")
        return

    full_file_path = find_target_csv_file(data_directory)
    
    if not full_file_path:
        print(f"Error: No CSV data file was found inside {data_directory}")
        return

    # Extract target file name metadata to reuse in export naming conversions
    base_file_name = os.path.basename(full_file_path)
    file_prefix = base_file_name.split("_")[0] if "_" in base_file_name else "portfolio"
    export_report_name = f"{file_prefix}_analysis_report.txt"
    export_full_path = os.path.join(base_project_directory, export_report_name)

    valid_data_rows = []
    dividend_records = []
    
    in_holdings_section = False
    in_transaction_section = False
    
    # Line-by-line parsing engine to concurrently extract balance tables and transaction logs
    try:
        with open(full_file_path, "r", encoding="utf-8") as raw_file:
            for line in raw_file:
                split_row = [field.strip() for field in line.split(",")]
                row_length = len(split_row)
                
                # Context Boundary Detection Logic
                if row_length >= 6:
                    if split_row[0] == "Account Number" and split_row[2] == "Symbol":
                        in_holdings_section = True
                        in_transaction_section = False
                        continue
                    elif split_row[0] == "Account Number" and split_row[3] == "Transaction Type":
                        in_transaction_section = True
                        in_holdings_section = False
                        continue
                    elif (in_holdings_section or in_transaction_section) and split_row[0] == "Account Number":
                        # Reset section flags if a new unhandled table header repeats
                        in_holdings_section = False
                        in_transaction_section = False
                        continue
                        
                # Extract Rows from Active Holdings Block
                if in_holdings_section and row_length >= 6:
                    account_id = split_row[0]
                    ticker_symbol = split_row[2]
                    
                    if account_id.isdigit() and ticker_symbol.isalnum() and (1 <= len(ticker_symbol) <= 5):
                        valid_data_rows.append({
                            "Account Number": account_id,
                            "Investment Name": split_row[1],
                            "Symbol": ticker_symbol,
                            "Shares": split_row[3],
                            "Share Price": split_row[4],
                            "Total Value": split_row[5]
                        })
                        
                # Extract Rows from Historical Transaction Ledger Block
                if in_transaction_section and row_length >= 10:
                    transaction_type = split_row[3]
                    # Trap both liquid cash dividends and automatically reinvested corporate actions
                    if transaction_type in ["Dividend", "Reinvestment", "Dividend Received", "Dividend Reinvestment"]:
                        dividend_records.append({
                            "Symbol": split_row[6],
                            "Type": transaction_type,
                            "Description": split_row[4],
                            "Amount": split_row[9]  # Net Amount or Gross Amount column placement
                        })
                        
    except Exception as read_error:
        print(f"An error occurred while reading the raw file text: {read_error}")
        return

    if not valid_data_rows:
        print("[Error] Failed to extract active holding records from the target file.")
        return

    # Process Holdings Dataframe
    portfolio_dataframe = pd.DataFrame(valid_data_rows)
    portfolio_dataframe["Cleaned_Value"] = portfolio_dataframe["Total Value"].apply(clean_currency_value)
    portfolio_dataframe["Asset_Class"] = portfolio_dataframe["Symbol"].apply(get_asset_class)
    total_portfolio_worth = portfolio_dataframe["Cleaned_Value"].sum()
    
    if total_portfolio_worth == 0:
        print("[Error] Total calculated portfolio balance is zero. Verify CSV data rows.")
        return

    # Process Dividend Transactions Dataframe
    total_dividends_collected = 0.0
    dividend_summary_series = pd.Series(dtype=float)
    
    if dividend_records:
        dividend_dataframe = pd.DataFrame(dividend_records)
        # Apply string cleaning function to convert financial strings to math floats safely
        dividend_dataframe["Cleaned_Amount"] = dividend_dataframe["Amount"].apply(clean_currency_value)
        # Flip negative transaction indicators to absolute values for positive compounding totals
        dividend_dataframe["Cleaned_Amount"] = dividend_dataframe["Cleaned_Amount"].abs()
        
        total_dividends_collected = dividend_dataframe["Cleaned_Amount"].sum()
        dividend_summary_series = dividend_dataframe.groupby("Symbol")["Cleaned_Amount"].sum().sort_values(ascending=False)

    # Open a text report block to write console feedback and save the log concurrently
    try:
        with open(export_full_path, "w", encoding="utf-8") as report_file:
            
            def log_and_write(output_string):
                print(output_string)
                report_file.write(output_string + "\n")

            log_and_write("==================================================")
            log_and_write("VANGUARD AUTOMATION SYSTEM - PORTFOLIO ASSESSMENT")
            log_and_write(f"Source Data File : {base_file_name}")
            log_and_write(f"Report Generated : {file_prefix}")
            log_and_write("==================================================")
            
            log_and_write(f"\nTotal Portfolio Value: ${total_portfolio_worth:,.2f}")
            log_and_write("=" * 50)

            log_and_write("\n[HIGH-LEVEL ASSET CLASS ALLOCATION]")
            class_groupings = portfolio_dataframe.groupby("Asset_Class")["Cleaned_Value"].sum().sort_values(ascending=False)
            for class_name, class_sum in class_groupings.items():
                class_percentage = (class_sum / total_portfolio_worth) * 100
                log_and_write(f" * {class_name:<35} : ${class_sum:>11,.2f} ({class_percentage:.2f}%)")

            log_and_write("\n" + "-" * 50)
            log_and_write("\n[CUMULATIVE RECEIVED DIVIDEND SUMMARY]")
            log_and_write(f"Total Historical Dividend Income Collected: ${total_dividends_collected:,.2f}")
            log_and_write("-" * 50)
            if not dividend_summary_series.empty:
                for ticker_symbol, dividend_total in dividend_summary_series.items():
                    log_and_write(f" * {ticker_symbol:<10} Cumulative Income Produced: ${dividend_total:>10,.2f}")
            else:
                log_and_write(" * No historical dividend distributions found in the current file log.")

            log_and_write("\n" + "-" * 50)
            log_and_write("\n[ALLOCATION ANALYSIS BY ACCOUNT ID]")
            account_groupings = portfolio_dataframe.groupby("Account Number")["Cleaned_Value"].sum()
            for account_name, account_sum in account_groupings.items():
                allocation_percentage = (account_sum / total_portfolio_worth) * 100
                log_and_write(f" * Account ID: {account_name:<15} : ${account_sum:>11,.2f} ({allocation_percentage:.2f}%)")

            log_and_write("\n" + "-" * 50)
            log_and_write("\n[DETAILED INDIVIDUAL HOLDINGS BREAKDOWN]")
            ticker_groupings = portfolio_dataframe.groupby("Symbol")["Cleaned_Value"].sum().sort_values(ascending=False)
            for ticker_name, ticker_sum in ticker_groupings.items():
                holding_percentage = (ticker_sum / total_portfolio_worth) * 100
                log_and_write(f" * {ticker_name:<10} Allocation Value: ${ticker_sum:>11,.2f} ({holding_percentage:.2f}%)")
                    
            log_and_write("\n==================================================")
            log_and_write("Analysis Task Completed and Report File Exported.")
            log_and_write("==================================================")
            
        print(f"\n[System Success] A permanent report file was saved to:\n -> {export_full_path}\n")

    except Exception as export_error:
        print(f"An error occurred while creating the exported report file: {export_error}")

if __name__ == "__main__":
    analyze_vanguard_portfolio()